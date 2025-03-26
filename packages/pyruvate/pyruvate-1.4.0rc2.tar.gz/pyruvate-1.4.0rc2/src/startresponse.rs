use cpython::{
    PyClone, PyDict, PyDrop, PyErr, PyList, PyObject, PyResult, PyTuple, PyType, Python,
    PythonObject, PythonObjectDowncastError, PythonObjectWithCheckedDowncast,
    PythonObjectWithTypeObject,
};
use log::error;
use pyo3_ffi as ffi;
use std::boxed::Box;
use std::cell::{Cell, RefCell};
use std::mem;
use std::ptr::addr_of_mut;
use std::{cmp, ptr};

use crate::pyutils::{build_tp_name, data_offset, AbortOnDrop, PyTypeObject_INIT, PY_OBJECT_SIZE};
use crate::request::CONTENT_LENGTH_HEADER;

type WSGIHeaders = Vec<(String, Vec<(String, String)>)>;

pub struct StartResponse {
    _unsafe_inner: PyObject,
}
impl PythonObject for StartResponse {
    #[inline]
    fn as_object(&self) -> &PyObject {
        &self._unsafe_inner
    }
    #[inline]
    fn into_object(self) -> PyObject {
        self._unsafe_inner
    }
    /// Unchecked downcast from PyObject to Self.
    /// Undefined behavior if the input object does not have the expected type.
    #[inline]
    unsafe fn unchecked_downcast_from(obj: PyObject) -> Self {
        StartResponse { _unsafe_inner: obj }
    }
}
impl PythonObjectWithCheckedDowncast for StartResponse {
    #[inline]
    fn downcast_from(
        py: Python<'_>,
        obj: PyObject,
    ) -> Result<StartResponse, PythonObjectDowncastError<'_>> {
        if py.get_type::<StartResponse>().is_instance(py, &obj) {
            Ok(StartResponse { _unsafe_inner: obj })
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "StartResponse",
                obj.get_type(py),
            ))
        }
    }
    #[inline]
    fn downcast_borrow_from<'a, 'p>(
        py: Python<'p>,
        obj: &'a PyObject,
    ) -> Result<&'a StartResponse, PythonObjectDowncastError<'p>> {
        if py.get_type::<StartResponse>().is_instance(py, obj) {
            unsafe { Ok(std::mem::transmute::<&PyObject, &StartResponse>(obj)) }
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "StartResponse",
                obj.get_type(py),
            ))
        }
    }
}
impl StartResponse {
    const ENVIRON_OFFSET: usize = data_offset::<PyDict>(PY_OBJECT_SIZE);
    const HEADERS_SET_OFFSET: usize =
        data_offset::<RefCell<WSGIHeaders>>(Self::ENVIRON_OFFSET + mem::size_of::<PyDict>());
    const HEADERS_SENT_OFFSET: usize = data_offset::<RefCell<WSGIHeaders>>(
        Self::HEADERS_SET_OFFSET + mem::size_of::<RefCell<WSGIHeaders>>(),
    );
    const CONTENT_LENGTH_OFFSET: usize = data_offset::<Cell<Option<usize>>>(
        Self::HEADERS_SENT_OFFSET + mem::size_of::<RefCell<WSGIHeaders>>(),
    );
    const CONTENT_BYTES_WRITTEN_OFFSET: usize = data_offset::<Cell<usize>>(
        Self::CONTENT_LENGTH_OFFSET + mem::size_of::<Cell<Option<usize>>>(),
    );

    fn environ(&self) -> &PyDict {
        unsafe {
            let ptr = (self._unsafe_inner.as_ptr() as *const u8).add(Self::ENVIRON_OFFSET)
                as *const PyDict;
            &*ptr
        }
    }

    fn headers_set(&self) -> &RefCell<WSGIHeaders> {
        unsafe {
            let ptr = (self._unsafe_inner.as_ptr() as *const u8).add(Self::HEADERS_SET_OFFSET)
                as *const RefCell<WSGIHeaders>;
            &*ptr
        }
    }

    fn headers_sent(&self) -> &RefCell<WSGIHeaders> {
        unsafe {
            let ptr = (self._unsafe_inner.as_ptr() as *const u8).add(Self::HEADERS_SENT_OFFSET)
                as *const RefCell<WSGIHeaders>;
            &*ptr
        }
    }

    fn content_length(&self) -> &Cell<Option<usize>> {
        unsafe {
            let ptr = (self._unsafe_inner.as_ptr() as *const u8).add(Self::CONTENT_LENGTH_OFFSET)
                as *const Cell<Option<usize>>;
            &*ptr
        }
    }

    fn content_bytes_written(&self) -> &Cell<usize> {
        unsafe {
            let ptr = (self._unsafe_inner.as_ptr() as *const u8)
                .add(Self::CONTENT_BYTES_WRITTEN_OFFSET)
                as *const Cell<usize>;
            &*ptr
        }
    }

    #[inline]
    fn size() -> usize {
        Self::CONTENT_BYTES_WRITTEN_OFFSET + mem::size_of::<Cell<usize>>()
    }
    #[allow(clippy::type_complexity)]
    unsafe fn alloc(
        py: Python,
        ty: &PyType,
        (environ, headers_set, headers_sent, content_length, content_bytes_written): (
            PyDict,
            RefCell<WSGIHeaders>,
            RefCell<WSGIHeaders>,
            Cell<Option<usize>>,
            Cell<usize>,
        ),
    ) -> PyResult<PyObject> {
        let obj = PyObject::alloc(py, ty, ())?;
        let ptr = (obj.as_ptr() as *mut u8).add(Self::ENVIRON_OFFSET) as *mut PyDict;
        ptr::write(ptr, environ);
        let ptr =
            (obj.as_ptr() as *mut u8).add(Self::HEADERS_SET_OFFSET) as *mut RefCell<WSGIHeaders>;
        ptr::write(ptr, headers_set);
        let ptr =
            (obj.as_ptr() as *mut u8).add(Self::HEADERS_SENT_OFFSET) as *mut RefCell<WSGIHeaders>;
        ptr::write(ptr, headers_sent);
        let ptr =
            (obj.as_ptr() as *mut u8).add(Self::CONTENT_LENGTH_OFFSET) as *mut Cell<Option<usize>>;
        ptr::write(ptr, content_length);
        let ptr =
            (obj.as_ptr() as *mut u8).add(Self::CONTENT_BYTES_WRITTEN_OFFSET) as *mut Cell<usize>;
        ptr::write(ptr, content_bytes_written);
        Ok(obj)
    }
    unsafe fn dealloc(py: Python, obj: *mut ffi::PyObject) {
        let ptr = (obj as *mut u8).add(Self::ENVIRON_OFFSET) as *mut PyDict;
        ptr::drop_in_place(ptr);
        let ptr = (obj as *mut u8).add(Self::HEADERS_SET_OFFSET) as *mut RefCell<WSGIHeaders>;
        ptr::drop_in_place(ptr);
        let ptr = (obj as *mut u8).add(Self::HEADERS_SENT_OFFSET) as *mut RefCell<WSGIHeaders>;
        ptr::drop_in_place(ptr);
        let ptr = (obj as *mut u8).add(Self::HEADERS_SET_OFFSET) as *mut Cell<Option<usize>>;
        ptr::drop_in_place(ptr);
        let ptr = (obj as *mut u8).add(Self::CONTENT_LENGTH_OFFSET) as *mut Cell<usize>;
        ptr::drop_in_place(ptr);
        PyObject::dealloc(py, obj);
    }

    pub unsafe extern "C" fn tp_dealloc_callback(obj: *mut ffi::PyObject) {
        let guard = AbortOnDrop("tp_dealloc");
        let py = Python::assume_gil_acquired();
        Self::dealloc(py, obj);
        mem::forget(guard);
    }

    pub fn initialize(py: Python, module_name: Option<&str>) -> PyResult<PyType> {
        unsafe {
            if (TYPE_OBJECT.tp_flags & ffi::Py_TPFLAGS_READY) != 0 {
                return Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)));
            }
            if INIT_ACTIVE {
                {
                    panic!("Reentrancy detected: already initializing class StartResponse",);
                }
            }
            INIT_ACTIVE = true;

            TYPE_OBJECT.ob_base.ob_base.ob_type = addr_of_mut!(ffi::PyType_Type);
            TYPE_OBJECT.tp_name = build_tp_name(module_name, "StartResponse");
            TYPE_OBJECT.tp_basicsize = StartResponse::size() as ffi::Py_ssize_t;
            TYPE_OBJECT.tp_as_sequence = ptr::null_mut::<ffi::PySequenceMethods>();
            TYPE_OBJECT.tp_as_number = ptr::null_mut::<ffi::PyNumberMethods>();
            TYPE_OBJECT.tp_getset = ptr::null_mut::<ffi::PyGetSetDef>();

            let res = if ffi::PyType_Ready(addr_of_mut!(TYPE_OBJECT)) == 0 {
                Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)))
            } else {
                Err(PyErr::fetch(py))
            };

            INIT_ACTIVE = false;
            res
        }
    }

    pub fn __call__(
        &self,
        py: Python,
        status: PyObject,
        headers: PyObject,
        exc_info: Option<PyObject>,
    ) -> PyResult<PyObject> {
        let response_headers: &PyList = headers.extract(py)?;
        if exc_info.is_some() {
            error!("exc_info from application: {0:?}", exc_info);
        }
        let mut rh = Vec::<(String, String)>::new();
        for ob in response_headers.iter(py) {
            let tp = ob.extract::<PyTuple>(py)?;
            rh.push((
                tp.get_item(py, 0).to_string(),
                tp.get_item(py, 1).to_string(),
            ));
        }
        self.headers_set()
            .replace(<[_]>::into_vec(Box::new([(status.to_string(), rh)])));
        Ok(py.None())
    }

    pub fn create_instance(
        py: Python,
        environ: PyDict,
        headers_set: RefCell<WSGIHeaders>,
        headers_sent: RefCell<WSGIHeaders>,
        content_length: Cell<Option<usize>>,
        content_bytes_written: Cell<usize>,
    ) -> PyResult<StartResponse> {
        let obj = unsafe {
            StartResponse::alloc(
                py,
                &py.get_type::<StartResponse>(),
                (
                    environ,
                    headers_set,
                    headers_sent,
                    content_length,
                    content_bytes_written,
                ),
            )
        }?;
        Ok(StartResponse { _unsafe_inner: obj })
    }
}
static mut TYPE_OBJECT: ffi::PyTypeObject = ffi::PyTypeObject {
    tp_call: {
        unsafe extern "C" fn wrap_call(
            slf: *mut ffi::PyObject,
            args: *mut ffi::PyObject,
            kwargs: *mut ffi::PyObject,
        ) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            // Defaults
            let status: *mut ffi::PyObject = ptr::null_mut();
            let headers: *mut ffi::PyObject = ptr::null_mut();
            let exc_info: *mut ffi::PyObject = ptr::null_mut();

            // Keyword parameters
            if !kwargs.is_null() {
                // See https://peps.python.org/pep-3333/#the-start-response-callable:
                // "As with all WSGI callables, the arguments must be supplied positionally, not by
                // keyword."
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("__call__ expects only positional arguments").as_ptr(),
                );
                return ptr::null_mut();
            }
            // Positional parameters
            if ffi::PyArg_ParseTuple(
                args,
                ffi::c_str!("OO|O").as_ptr(),
                &status,
                &headers,
                &exc_info,
            ) == 0
            {
                return ptr::null_mut();
            }
            let exc_info = if exc_info.is_null() {
                None
            } else {
                Some(PyObject::from_borrowed_ptr(py, exc_info))
            };
            let slf = PyObject::from_borrowed_ptr(py, slf).unchecked_cast_into::<StartResponse>();
            let ret = slf.__call__(
                py,
                PyObject::from_borrowed_ptr(py, status),
                PyObject::from_borrowed_ptr(py, headers),
                exc_info,
            );
            PyDrop::release_ref(slf, py);
            match ret {
                Ok(obj) => obj.as_ptr(),
                Err(_) => ptr::null_mut(),
            }
        }
        Some(wrap_call)
    },
    tp_dealloc: Some(StartResponse::tp_dealloc_callback),
    tp_flags: ffi::Py_TPFLAGS_DEFAULT,
    tp_traverse: None,
    ..PyTypeObject_INIT
};
static mut INIT_ACTIVE: bool = false;

impl PythonObjectWithTypeObject for StartResponse {
    fn type_object(py: Python) -> PyType {
        StartResponse::initialize(py, None)
            .expect("An error occurred while initializing class StartResponse")
    }
}

pub trait WriteResponse {
    // Put this in a trait for more flexibility.
    // rust-cpython can't handle some types we are using here.
    #[allow(clippy::new_ret_no_self)]
    fn new(environ: PyDict, headers_set: WSGIHeaders, py: Python) -> PyResult<StartResponse>;
    fn content_complete(&self) -> bool;
    fn write(
        &mut self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_tranfer: bool,
    );
    fn environ(&self, py: Python) -> PyDict;
    fn content_length(&self) -> Option<usize>;
    fn content_bytes_written(&self) -> usize;
    fn headers_not_sent(&self) -> bool;
}

impl WriteResponse for StartResponse {
    fn new(environ: PyDict, headers_set: WSGIHeaders, py: Python) -> PyResult<StartResponse> {
        StartResponse::create_instance(
            py,
            environ,
            RefCell::new(headers_set),
            RefCell::new(Vec::new()),
            Cell::new(None),
            Cell::new(0),
        )
    }

    fn content_complete(&self) -> bool {
        if let Some(length) = self.content_length().get() {
            self.content_bytes_written().get() >= length
        } else {
            false
        }
    }

    fn write(
        &mut self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_transfer: bool,
    ) {
        if self.headers_sent().borrow().is_empty() {
            if self.headers_set().borrow().is_empty() {
                error!("write() before start_response()")
            }
            // Before the first output, send the stored headers
            self.headers_sent()
                .replace(self.headers_set().borrow().clone());
            let respinfo = self.headers_set().borrow_mut().pop(); // headers_sent|set should have only one element
            match respinfo {
                Some(respinfo) => {
                    let response_headers: Vec<(String, String)> = respinfo.1;
                    let status: String = respinfo.0;
                    output.extend(b"HTTP/1.1 ");
                    output.extend(status.as_bytes());
                    output.extend(b"\r\n");
                    let mut maybe_chunked = true;
                    for header in response_headers.iter() {
                        let headername = &header.0;
                        output.extend(headername.as_bytes());
                        output.extend(b": ");
                        output.extend(header.1.as_bytes());
                        output.extend(b"\r\n");
                        if headername.to_ascii_uppercase() == CONTENT_LENGTH_HEADER {
                            match header.1.parse::<usize>() {
                                Ok(length) => {
                                    self.content_length().set(Some(length));
                                    // no need to use chunked transfer encoding if we have a valid content length header,
                                    // see e.g. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding#Chunked_encoding
                                    maybe_chunked = false;
                                }
                                Err(e) => error!("Could not parse Content-Length header: {:?}", e),
                            }
                        }
                    }
                    output.extend(b"Via: pyruvate\r\n");
                    if close_connection {
                        output.extend(b"Connection: close\r\n");
                    } else {
                        output.extend(b"Connection: keep-alive\r\n");
                    }
                    if maybe_chunked && chunked_transfer {
                        output.extend(b"Transfer-Encoding: chunked\r\n");
                    }
                }
                None => {
                    error!("write(): No respinfo!");
                }
            }
            output.extend(b"\r\n");
        }
        match self.content_length().get() {
            Some(length) => {
                let cbw = self.content_bytes_written().get();
                if length > cbw {
                    let num = cmp::min(length - cbw, data.len());
                    if num > 0 {
                        output.extend(&data[..num]);
                        self.content_bytes_written().set(cbw + num);
                    }
                }
            }
            None => {
                // no content length header, use
                // chunked transfer encoding if specified
                let cbw = self.content_bytes_written().get();
                let length = data.len();
                if length > 0 {
                    if chunked_transfer {
                        output.extend(format!("{length:X}").as_bytes());
                        output.extend(b"\r\n");
                        output.extend(data);
                        output.extend(b"\r\n");
                    } else {
                        output.extend(data);
                    }
                    self.content_bytes_written().set(cbw + length);
                }
            }
        }
    }

    fn environ(&self, py: Python) -> PyDict {
        self.environ().clone_ref(py)
    }

    fn content_length(&self) -> Option<usize> {
        self.content_length().get()
    }

    fn content_bytes_written(&self) -> usize {
        self.content_bytes_written().get()
    }

    fn headers_not_sent(&self) -> bool {
        self.headers_sent().borrow().is_empty()
    }
}

#[cfg(test)]
mod tests {
    use cpython::{ObjectProtocol, PyClone, PyDict, PyTuple, Python, PythonObject, ToPyObject};
    use log::LevelFilter;
    use simplelog::{Config, WriteLogger};
    use std::env::temp_dir;
    use std::fs::File;
    use std::io::Read;

    use crate::startresponse::{StartResponse, WriteResponse};

    #[test]
    fn test_write() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let data = b"Hello world!\n";
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        assert_eq!(sr.content_length().get(), None);
        assert_eq!(WriteResponse::content_length(&sr), None);
        assert!(!sr.content_complete());
        let mut output: Vec<u8> = Vec::new();
        sr.write(data, &mut output, true, false);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello world!\n";
        assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
        assert!(!sr.content_complete());
        // chunked transfer requested and no content length header
        // The final chunk will be missing; it's written in WSGIResponse::write_chunk
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n\r\nD\r\nHello world!\n";
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        assert!(!sr.content_complete());
        sr.write(data, &mut output, true, true);
        assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
        assert!(!sr.content_complete());
    }

    #[test]
    fn test_honour_content_length_header() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete());
        sr.write(data, &mut output, true, false);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
        assert_eq!(sr.content_length().get(), Some(5));
        assert_eq!(WriteResponse::content_length(&sr), Some(5));
        assert_eq!(sr.content_bytes_written().get(), 5);
        assert!(sr.content_complete());
        assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
        // chunked transfer set - ignored if content length header available
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        assert!(!sr.content_complete());
        sr.write(data, &mut output, true, true);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
        assert_eq!(sr.content_length().get(), Some(5));
        assert_eq!(sr.content_bytes_written().get(), 5);
        assert!(sr.content_complete());
        assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_exc_info_is_none() {
        // do not display an error message when exc_info passed
        // by application is None
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let pycode = py.run(
            r#"
status = '200 OK'
response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
exc_info = 'Foo'
"#,
            None,
            Some(&locals),
        );
        match pycode {
            Ok(_) => {
                let status = locals.get_item(py, "status").unwrap();
                let headers = locals.get_item(py, "response_headers").unwrap();
                let exc_info = locals.get_item(py, "exc_info").unwrap();
                let environ = PyDict::new(py);
                // create logger
                let mut path = temp_dir();
                path.push("foo42.log");
                let path = path.into_os_string();
                WriteLogger::init(
                    LevelFilter::Info,
                    Config::default(),
                    File::create(&path).unwrap(),
                )
                .unwrap();

                let sr = StartResponse::new(environ, Vec::new(), py).unwrap();
                match sr.__call__(py, status.clone_ref(py), headers.clone_ref(py), None) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(!got.contains("exc_info"));
                        assert!(!got.contains("Foo"));
                    }
                    _ => assert!(false),
                }
                match sr.__call__(py, status, headers, Some(exc_info)) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(got.len() > 0);
                        assert!(got.contains("exc_info"));
                        assert!(got.contains("Foo"));
                    }
                    _ => assert!(false),
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_call_nargs_headers_missing() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let sr = StartResponse::new(environ, headers, py).unwrap();
        match sr.as_object().call(
            py,
            PyTuple::new(py, &["200 OK".to_py_object(py).into_object()]),
            None,
        ) {
            Ok(_) => assert!(false),
            Err(_) => (),
        }
    }

    #[test]
    fn test_call_with_kwargs() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let sr = StartResponse::new(environ, headers, py).unwrap();
        let kwargs = PyDict::new(py);
        kwargs.set_item(py, "environ", PyDict::new(py)).unwrap();
        kwargs
            .set_item(py, "headers", PyTuple::new(py, &[]))
            .unwrap();
        match sr
            .as_object()
            .call(py, PyTuple::new(py, &[]), Some(&kwargs))
        {
            Ok(_) => assert!(false),
            Err(_) => (),
        }
    }
}
