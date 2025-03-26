#![allow(non_upper_case_globals)]
use cpython::{
    NoArgs, ObjectProtocol, PyDict, PyErr, PyObject, PyResult, Python, TypeError, ValueError,
};
use crossbeam_channel::{unbounded, Receiver, Sender};
use libc::c_char;
use log::{self, set_boxed_logger, set_max_level, Level, LevelFilter, Log, Record};
use pyo3_ffi as ffi;
use pyo3_ffi::{PyEval_RestoreThread, PyEval_SaveThread};
pub use pyo3_ffi::{PyGILState_Ensure, PyGILState_Release, PyThreadState};
use std::cell::RefCell;
use std::ffi::CString;
use std::io;
use std::mem;
use std::thread::spawn;

pub fn with_python_thread<'a, F, R>(mut code: F) -> R
where
    F: FnMut(Python<'a>) -> R,
{
    let (gilstate, py) = unsafe { (PyGILState_Ensure(), Python::assume_gil_acquired()) };
    let result = code(py);
    unsafe { PyGILState_Release(gilstate) };
    result
}

pub fn with_released_gil<F, R>(mut code: F) -> R
where
    F: FnMut(*mut PyThreadState) -> R,
{
    let py_thread_state = unsafe { PyEval_SaveThread() };
    let result = code(py_thread_state);
    unsafe { PyEval_RestoreThread(py_thread_state) };
    result
}

pub fn with_acquired_gil<F, R>(py_thread_state: *mut PyThreadState, mut code: F) -> R
where
    F: FnMut() -> R,
{
    unsafe { PyEval_RestoreThread(py_thread_state) };
    let result = code();
    unsafe { PyEval_SaveThread() };
    result
}

pub fn close_pyobject(ob: &PyObject, py: Python) -> PyResult<()> {
    if ob.getattr(py, "close").is_ok() {
        ob.call_method(py, "close", NoArgs, None)?;
    }
    Ok(())
}

fn clear_pyerr<F, R>(mut code: F, py: Python)
where
    F: FnMut() -> PyResult<R>,
{
    if code().is_err() {
        PyErr::fetch(py);
    }
}

// We want thread names available for Python logging.
// Therefore we store the worker name in Rust thread local storage
// and update the Python logging thread name from it
thread_local!(static PY_THREAD_NAME: RefCell<String> = RefCell::new(String::from("pyruvate-main")));

fn set_python_threadinfo(py: Python, thread_name: &str) {
    if let Ok(threading) = py.import("threading") {
        let locals = PyDict::new(py);
        if locals.set_item(py, "threading", threading).is_ok() {
            let pycode = format!("threading.current_thread().name = '{thread_name}'");
            clear_pyerr(|| py.run(&pycode, None, Some(&locals)), py);
        }
    };
}

pub fn init_python_threadinfo(py: Python, thread_name: String) {
    set_python_threadinfo(py, &thread_name);
    PY_THREAD_NAME.with(|name| {
        *name.borrow_mut() = thread_name;
    });
}

// Notes:
//
// * Not all Python logging levels are available, only
//   those corresponding to available levels
//   in the log crate
//
// * The Rust log crate expects a global logger set *once*,
//   so it's necessary/helpful to be able to change
//   the underlying Python logger in use
fn setup_python_logger(
    py: Python,
    name: &str,
) -> PyResult<(u8, u8, u8, u8, PyObject, LevelFilter)> {
    let locals = PyDict::new(py);
    let pylogging = py.import("logging")?;
    let debug = pylogging.get(py, "DEBUG")?.extract(py)?;
    let error = pylogging.get(py, "ERROR")?.extract(py)?;
    let info = pylogging.get(py, "INFO")?.extract(py)?;
    let warn = pylogging.get(py, "WARN")?.extract(py)?;
    locals.set_item(py, "logging", pylogging)?;
    let logger: PyObject = py
        .eval(&format!("logging.getLogger('{name}')"), None, Some(&locals))?
        .extract(py)?;
    let level = logger.call_method(py, "getEffectiveLevel", NoArgs, None)?;
    match level.extract::<u8>(py) {
        Ok(u8lvl) => {
            let filter = match u8lvl {
                lvl if lvl == debug => LevelFilter::Trace,
                lvl if lvl >= error => LevelFilter::Error,
                lvl if lvl == info => LevelFilter::Info,
                lvl if lvl == warn => LevelFilter::Warn,
                _ => LevelFilter::Off,
            };
            set_max_level(filter);
            Ok((debug, error, info, warn, logger, filter))
        }
        Err(_) => Err(PyErr::new::<TypeError, _>(
            py,
            format!("Expected u8, got {level:?}"),
        )),
    }
}

pub struct SyncPythonLogger {
    logger: PyObject,
    debug: u8,
    error: u8,
    info: u8,
    warn: u8,
    level: Option<Level>,
}

impl SyncPythonLogger {
    pub fn new(py: Python, name: &str) -> PyResult<Self> {
        match setup_python_logger(py, name) {
            Ok((debug, error, info, warn, logger, filter)) => Ok(Self {
                logger,
                debug,
                error,
                info,
                warn,
                level: filter.to_level(),
            }),
            Err(e) => Err(e),
        }
    }

    fn python_level(&self, level: Level) -> u8 {
        match level {
            Level::Error => self.error,
            Level::Warn => self.warn,
            Level::Info => self.info,
            Level::Debug => self.debug,
            Level::Trace => self.debug,
        }
    }
}

impl Log for SyncPythonLogger {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        self.level.is_some_and(|lvl| metadata.level() <= lvl)
    }

    fn log(&self, record: &Record) {
        with_python_thread(|py| {
            PY_THREAD_NAME.with(|name| set_python_threadinfo(py, &name.borrow()));
            clear_pyerr(
                || {
                    self.logger.call_method(
                        py,
                        "log",
                        (
                            self.python_level(record.level()),
                            format!("{}", record.args()),
                        ),
                        None,
                    )
                },
                py,
            );
        });
    }

    fn flush(&self) {}
}

type LogRecordData = ((u8, String), String);

pub struct AsyncPythonLogger {
    records: Sender<LogRecordData>,
    debug: u8,
    error: u8,
    info: u8,
    warn: u8,
    level: Option<Level>,
}

impl AsyncPythonLogger {
    const STOPMARKER: LogRecordData = ((99, String::new()), String::new());

    pub fn new(py: Python, name: &str) -> PyResult<Self> {
        match setup_python_logger(py, name) {
            Ok((debug, error, info, warn, logger, filter)) => {
                let records = Self::create_logging_thread(logger);
                Ok(Self {
                    records,
                    debug,
                    error,
                    info,
                    warn,
                    level: filter.to_level(),
                })
            }
            Err(e) => Err(e),
        }
    }

    fn python_level(&self, level: Level) -> u8 {
        match level {
            Level::Error => self.error,
            Level::Warn => self.warn,
            Level::Info => self.info,
            Level::Debug => self.debug,
            Level::Trace => self.debug,
        }
    }

    fn create_logging_thread(pylog: PyObject) -> Sender<LogRecordData> {
        let (tx, rx): (Sender<LogRecordData>, Receiver<LogRecordData>) = unbounded();
        spawn(move || {
            with_python_thread(|py| {
                with_released_gil(|threadstate| {
                    while let Ok(record) = rx.recv() {
                        if record == Self::STOPMARKER {
                            break;
                        }
                        with_acquired_gil(threadstate, || {
                            set_python_threadinfo(py, &record.1);
                            clear_pyerr(|| pylog.call_method(py, "log", &record.0, None), py);
                        });
                    }
                });
            });
        });
        tx
    }
}

impl Log for AsyncPythonLogger {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        self.level.is_some_and(|lvl| metadata.level() <= lvl)
    }

    fn log(&self, record: &Record) {
        let thread_name = PY_THREAD_NAME.with(|name| String::from(&(*name.borrow())));
        self.records
            .send((
                (
                    self.python_level(record.level()),
                    format!("{}", record.args()),
                ),
                thread_name,
            ))
            .unwrap_or(());
    }

    fn flush(&self) {}
}

impl Drop for AsyncPythonLogger {
    fn drop(&mut self) {
        if self.records.send(Self::STOPMARKER).is_err() {}
    }
}

macro_rules! set_global_python_logger {
    ($L: ident, $py: ident, $name: ident) => {
        match $L::new($py, $name) {
            Ok(logging) => match set_boxed_logger(Box::new(logging)) {
                Ok(_) => Ok(()),
                Err(_) => Err(PyErr::new::<ValueError, _>(
                    $py,
                    format!("Logging already initialized"),
                )),
            },
            Err(e) => Err(e),
        }
    };
}

pub fn async_logger(py: Python, name: &str) -> PyResult<()> {
    set_global_python_logger!(AsyncPythonLogger, py, name)
}

pub fn sync_logger(py: Python, name: &str) -> PyResult<()> {
    set_global_python_logger!(SyncPythonLogger, py, name)
}

// copied from rust-cpython::python3_sys
macro_rules! as_expr {
    ($e:expr) => {
        $e
    };
}

macro_rules! py_type_object_init {
    ($($tail:tt)*) => {
        as_expr! {
            ffi::PyTypeObject {
                ob_base: ffi::PyVarObject {
                    ob_base: ffi::PyObject_HEAD_INIT,
                    ob_size: 0
                },
                tp_name: 0 as *const c_char,
                tp_basicsize: 0,
                tp_itemsize: 0,
                tp_dealloc: None,
                tp_getattr: None,
                tp_setattr: None,
                tp_repr: None,
                tp_as_number: 0 as *mut ffi::PyNumberMethods,
                tp_as_sequence: 0 as *mut ffi::PySequenceMethods,
                tp_as_mapping: 0 as *mut ffi::PyMappingMethods,
                tp_hash: None,
                tp_call: None,
                tp_str: None,
                tp_getattro: None,
                tp_setattro: None,
                tp_as_buffer: 0 as *mut ffi::PyBufferProcs,
                tp_flags: ffi::Py_TPFLAGS_DEFAULT,
                tp_doc: 0 as *const c_char,
                tp_traverse: None,
                tp_clear: None,
                tp_richcompare: None,
                tp_weaklistoffset: 0,
                tp_iter: None,
                tp_iternext: None,
                tp_methods: 0 as *mut ffi::PyMethodDef,
                tp_members: 0 as *mut ffi::PyMemberDef,
                tp_getset: 0 as *mut ffi::PyGetSetDef,
                tp_base: 0 as *mut ffi::PyTypeObject,
                tp_dict: 0 as *mut ffi::PyObject,
                tp_descr_get: None,
                tp_descr_set: None,
                tp_dictoffset: 0,
                tp_init: None,
                tp_alloc: None,
                tp_new: None,
                tp_free: None,
                tp_is_gc: None,
                tp_bases: 0 as *mut ffi::PyObject,
                tp_mro: 0 as *mut ffi::PyObject,
                tp_cache: 0 as *mut ffi::PyObject,
                tp_subclasses: 0 as *mut ffi::PyObject,
                tp_weaklist: 0 as *mut ffi::PyObject,
                tp_del: None,
                tp_version_tag: 0,
                $($tail)*
            }
        }
    }
}

#[cfg(py_sys_config = "COUNT_ALLOCS")]
macro_rules! py_type_object_init_with_count_allocs {
    ($($tail:tt)*) => {
        py_type_object_init!(
            $($tail)*
            tp_allocs: 0,
            tp_frees: 0,
            tp_maxalloc: 0,
            tp_prev: 0 as *mut ffi::PyTypeObject,
            tp_next: 0 as *mut ffi::PyTypeObject,
        )
    }
}

#[cfg(not(py_sys_config = "COUNT_ALLOCS"))]
macro_rules! py_type_object_init_with_count_allocs {
    ($($tail:tt)*) => {
        py_type_object_init!($($tail)*)
    }
}

#[cfg(Py_3_12)]
pub const PyTypeObject_INIT: ffi::PyTypeObject = py_type_object_init_with_count_allocs!(
    tp_as_async: 0 as *mut ffi::PyAsyncMethods,
    tp_vectorcall_offset: 0,
    tp_vectorcall: None,
    tp_finalize: None,
    tp_watched: 0,
);

#[cfg(all(Py_3_9, not(Py_3_12)))]
pub const PyTypeObject_INIT: ffi::PyTypeObject = py_type_object_init_with_count_allocs!(
    tp_as_async: 0 as *mut ffi::PyAsyncMethods,
    tp_vectorcall_offset: 0,
    tp_vectorcall: None,
    tp_finalize: None,
);

// for convenience
pub const PY_OBJECT_SIZE: usize = mem::size_of::<ffi::PyObject>();

pub fn build_tp_name(module_name: Option<&str>, type_name: &str) -> *mut c_char {
    let name = match module_name {
        Some(module_name) => CString::new(format!("{}.{}", module_name, type_name)),
        None => CString::new(type_name),
    };
    name.expect("Module name/type name must not contain NUL byte")
        .into_raw()
}

pub struct AbortOnDrop<'a>(pub &'a str);

impl Drop for AbortOnDrop<'_> {
    fn drop(&mut self) {
        use std::io::Write;
        let _ = writeln!(&mut io::stderr(), "Cannot unwind out of {}", self.0);
        unsafe { libc::abort() }
    }
}

#[inline]
pub const fn data_offset<T>(base_size: usize) -> usize {
    let align = mem::align_of::<T>();
    // round base_size up to next multiple of align
    base_size.div_ceil(align) * align
}

#[cfg(test)]
mod tests {
    use cpython::{ObjectProtocol, PyClone, PyDict, PyObject, Python};
    use log::{max_level, Level, LevelFilter, Log, Record};
    use pyo3_ffi::{PyEval_RestoreThread, PyEval_SaveThread, PyThreadState_Get};
    use std::fs::{remove_file, File};
    use std::io::Read;
    use std::sync::mpsc::channel;
    use std::{thread, time};

    use crate::pyutils::{
        clear_pyerr, init_python_threadinfo, with_python_thread, with_released_gil,
        AsyncPythonLogger, SyncPythonLogger,
    };

    #[test]
    fn test_async_logging() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
import logging
from tempfile import mkstemp

_, logfilename = mkstemp()

# create logger
logger = logging.getLogger('foo_async')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler = logging.FileHandler(logfilename)
handler.setFormatter(fmt)
logger.addHandler(handler)"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => match AsyncPythonLogger::new(py, "foo_async") {
                Ok(logger) => {
                    assert_eq!(max_level(), LevelFilter::Trace);
                    let py_thread_state = unsafe { PyEval_SaveThread() };
                    with_python_thread(|_py| {
                        let record = Record::builder()
                            .args(format_args!("debug: foo"))
                            .level(Level::Debug)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("Foo error encountered"))
                            .level(Level::Error)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("bar baz info"))
                            .level(Level::Info)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("tracing foo async ..."))
                            .level(Level::Trace)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("there's a foo!"))
                            .level(Level::Warn)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                    });
                    // yield
                    thread::sleep(time::Duration::from_millis(50));
                    unsafe { PyEval_RestoreThread(py_thread_state) };
                    let logfilename: String = locals
                        .get_item(py, "logfilename")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let mut logfile = File::open(&logfilename).unwrap();
                    let mut contents = String::new();
                    logfile.read_to_string(&mut contents).unwrap();
                    assert_eq!("DEBUG:foo_async:debug: foo\nERROR:foo_async:Foo error encountered\nINFO:foo_async:bar baz info\nDEBUG:foo_async:tracing foo async ...\nWARNING:foo_async:there's a foo!\n", contents);
                    remove_file(logfilename).unwrap();
                }
                Err(_) => assert!(false),
            },
            Err(_) => {
                assert!(false);
            }
        }
    }

    #[test]
    fn test_sync_logging() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
import logging
from tempfile import mkstemp

_, logfilename = mkstemp()

# create logger
logger = logging.getLogger('foo_sync')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler = logging.FileHandler(logfilename)
handler.setFormatter(fmt)
logger.addHandler(handler)"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => match SyncPythonLogger::new(py, "foo_sync") {
                Ok(logger) => {
                    assert_eq!(max_level(), LevelFilter::Trace);
                    let py_thread_state = unsafe { PyEval_SaveThread() };
                    let record = Record::builder()
                        .args(format_args!("debug: foo"))
                        .level(Level::Debug)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("Foo error encountered"))
                        .level(Level::Error)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("bar baz info"))
                        .level(Level::Info)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("tracing foo sync ..."))
                        .level(Level::Trace)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("there's a foo!"))
                        .level(Level::Warn)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    unsafe { PyEval_RestoreThread(py_thread_state) };
                    let logfilename: String = locals
                        .get_item(py, "logfilename")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let mut logfile = File::open(&logfilename).unwrap();
                    let mut contents = String::new();
                    logfile.read_to_string(&mut contents).unwrap();
                    assert_eq!("DEBUG:foo_sync:debug: foo\nERROR:foo_sync:Foo error encountered\nINFO:foo_sync:bar baz info\nDEBUG:foo_sync:tracing foo sync ...\nWARNING:foo_sync:there's a foo!\n", contents);
                    remove_file(logfilename).unwrap();
                }
                Err(_) => assert!(false),
            },
            Err(_) => {
                assert!(false);
            }
        }
    }

    #[test]
    fn test_with_python_thread() {
        // test whether nesting of with_python_thread
        // leads to undesired invalidation
        // of thread state
        let (tx, rx) = channel();
        let _gil = Python::acquire_gil();
        with_released_gil(|_thread_state| {
            let tx = tx.clone();
            let t = thread::spawn(move || {
                with_python_thread(|py| {
                    let thread_state = unsafe { PyThreadState_Get() };
                    assert_eq!(thread_state, unsafe { PyThreadState_Get() });
                    let threading = py.import("threading").unwrap();
                    let locals = PyDict::new(py);
                    locals.set_item(py, "threading", threading).unwrap();
                    // s. https://docs.python.org/3/library/threading.html#thread-local-data
                    let local: PyObject = py
                        .eval("threading.local()", None, Some(&locals))
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let expected = "bar".to_string();
                    local.setattr(py, "foo", expected.clone()).unwrap();
                    locals
                        .set_item(py, "thread_local", local.clone_ref(py))
                        .unwrap();
                    // the next line will in fact create another local object different from the
                    // first one
                    let another_local: PyObject = py
                        .eval("threading.local()", None, Some(&locals))
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    assert!(local != another_local);
                    let got: bool = another_local.hasattr(py, "foo").unwrap();
                    assert_eq!(got, false);
                    with_python_thread(|py| {
                        assert_eq!(thread_state, unsafe { PyThreadState_Get() });
                        let local_nested: PyObject = locals
                            .get_item(py, "thread_local")
                            .unwrap()
                            .extract(py)
                            .unwrap();
                        let got: String = local_nested
                            .getattr(py, "foo")
                            .unwrap()
                            .extract(py)
                            .unwrap();
                        assert_eq!(expected, got);
                    });
                    assert_eq!(thread_state, unsafe { PyThreadState_Get() });
                    let local_restored: PyObject = locals
                        .get_item(py, "thread_local")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let got: String = local_restored
                        .getattr(py, "foo")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    assert_eq!(expected, got);
                    let got: String = local.getattr(py, "foo").unwrap().extract(py).unwrap();
                    assert_eq!(expected, got);
                });
                tx.send(()).unwrap();
            });
            rx.recv().unwrap();
            t.join().unwrap();
        });
    }

    #[test]
    fn test_python_threadinfo() {
        let _gil = Python::acquire_gil();
        with_python_thread(|py| {
            let expected = "foo42";
            init_python_threadinfo(py, String::from(expected));
            let threading = py.import("threading").unwrap();
            let locals = PyDict::new(py);
            locals.set_item(py, "threading", threading).unwrap();
            let got: String = py
                .eval("threading.current_thread().name", None, Some(&locals))
                .unwrap()
                .extract(py)
                .unwrap();
            assert_eq!(expected, &got);
        });
    }

    #[test]
    fn test_clear_pyerr() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        clear_pyerr(|| py.run("raise ValueError", None, Some(&locals)), py);
    }
}
