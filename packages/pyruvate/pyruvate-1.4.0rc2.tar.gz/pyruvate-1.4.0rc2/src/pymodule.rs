use cfg_if::cfg_if;
use cpython::{IOError, PyErr, PyObject, PyResult, Python, PythonObject, ValueError};
use mio::net::{TcpListener, UnixListener};
use pyo3_ffi as ffi;
use std::ffi::{c_char, CStr};
use std::ptr;
use std::time::Duration;

use crate::filewrapper::FileWrapper;
use crate::globals::{shared_wsgi_options, ServerOptions};
use crate::pyutils::{async_logger, sync_logger};
use crate::server::Server;
use crate::startresponse::StartResponse;
use crate::transport::{parse_server_info, shared_connection_options};

#[cfg(target_os = "linux")]
use crate::transport::SocketActivation;

macro_rules! server_loop {
    ($L:ty, $application: ident, $listener: ident, $server_options: ident, $async_logging: ident, $py: ident) => {
        match Server::<$L>::new($application, $listener, $server_options, $py) {
            Ok(mut server) => {
                let res = if $async_logging {
                    async_logger($py, "pyruvate")
                } else {
                    sync_logger($py, "pyruvate")
                };
                match res {
                    Ok(_) => match server.serve() {
                        Ok(_) => Ok($py.None()),
                        Err(_) => Err(PyErr::new::<IOError, _>(
                            $py,
                            "Error encountered during event loop",
                        )),
                    },
                    Err(_) => Err(PyErr::new::<IOError, _>($py, "Could not setup logging")),
                }
            }
            Err(e) => Err(PyErr::new::<IOError, _>(
                $py,
                format!("Could not create server: {e:?}"),
            )),
        }
    };
}

#[allow(clippy::too_many_arguments)]
pub fn serve(
    py: Python,
    application: PyObject,
    addr: Option<String>,
    num_workers: usize,
    max_number_headers: usize,
    async_logging: bool,
    chunked_transfer: bool,
    max_reuse_count: u8,
    keepalive_timeout: u8,
    qmon_warn_threshold: Option<usize>,
    send_timeout: u8,
) -> PyResult<PyObject> {
    if num_workers < 1 {
        return Err(PyErr::new::<ValueError, _>(py, "Need at least 1 worker"));
    }
    // addr can be a TCP or Unix domain socket address
    // or None when using a systemd socket.
    let (sockaddr, server_name, server_port) = parse_server_info(addr.clone());
    let server_options = ServerOptions {
        num_workers,
        max_number_headers,
        connection_options: shared_connection_options(
            max_reuse_count,
            Duration::from_secs(keepalive_timeout.into()),
        ),
        wsgi_options: shared_wsgi_options(
            server_name.clone(),
            server_port,
            String::new(),
            chunked_transfer,
            qmon_warn_threshold,
            Duration::from_secs(send_timeout.into()),
            py,
        ),
    };
    match addr {
        Some(_) => {
            match sockaddr {
                Some(sockaddr) => match TcpListener::bind(sockaddr) {
                    Ok(listener) => server_loop!(
                        TcpListener,
                        application,
                        listener,
                        server_options,
                        async_logging,
                        py
                    ),
                    Err(e) => Err(PyErr::new::<IOError, _>(
                        py,
                        format!("Could not bind socket: {e:?}"),
                    )),
                },
                None => {
                    // fallback to UnixListener
                    match UnixListener::bind(server_name) {
                        Ok(listener) => server_loop!(
                            UnixListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(e) => Err(PyErr::new::<IOError, _>(
                            py,
                            format!("Could not bind unix domain socket: {e:?}"),
                        )),
                    }
                }
            }
        }
        None => {
            cfg_if! {
                if #[cfg(target_os = "linux")] {
                    // try systemd socket activation
                    match TcpListener::from_active_socket() {
                        Ok(listener) => server_loop!(
                            TcpListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(_) => {
                            // fall back to UnixListener
                            match UnixListener::from_active_socket() {
                                Ok(listener) => server_loop!(
                                    UnixListener,
                                    application,
                                    listener,
                                    server_options,
                                    async_logging,
                                    py
                                ),
                                Err(e) => Err(PyErr::new::<IOError, _>(
                                    py,
                                    format!("Socket activation: {e}"),
                                )),
                            }
                        }
                    }
                } else {
                    Err(PyErr::new::<IOError, _>(
                        py,
                        "Could not bind socket.",
                    ))
                }
            }
        }
    }
}

// begin plain pyo3-ffi
static mut MODULE_DEF: ffi::PyModuleDef = ffi::PyModuleDef {
    m_base: ffi::PyModuleDef_HEAD_INIT,
    m_name: ffi::c_str!("pyruvate").as_ptr(),
    m_doc: ffi::c_str!("Pyruvate WSGI server").as_ptr(),
    m_size: 0,
    #[allow(static_mut_refs)]
    m_methods: unsafe { METHODS.as_mut_ptr().cast() },
    m_slots: std::ptr::null_mut(),
    m_traverse: None,
    m_clear: None,
    m_free: None,
};

static mut METHODS: [ffi::PyMethodDef; 2] = [
    ffi::PyMethodDef {
        ml_name: ffi::c_str!("serve").as_ptr(),
        ml_meth: ffi::PyMethodDefPointer {
            PyCFunctionWithKeywords: wrap,
        },
        ml_flags: ffi::METH_VARARGS | ffi::METH_KEYWORDS,
        ml_doc: ffi::c_str!("Serve WSGI application").as_ptr(),
    },
    // A zeroed PyMethodDef to mark the end of the array.
    ffi::PyMethodDef::zeroed(),
];

// The module initialization function, which must be named `PyInit_<your_module>`.
#[allow(non_snake_case)]
#[no_mangle]
pub unsafe extern "C" fn PyInit_pyruvate() -> *mut ffi::PyObject {
    let py = Python::assume_gil_acquired();
    let pymod = ffi::PyModule_Create(ptr::addr_of_mut!(MODULE_DEF));
    let ty = StartResponse::initialize(py, Some("pyruvate")).unwrap();
    let di = ffi::PyModule_GetDict(pymod);
    ffi::PyDict_SetItemString(
        di,
        ffi::c_str!("StartResponse").as_ptr(),
        ty.as_object().as_ptr(),
    );
    let ty = FileWrapper::initialize(py, Some("pyruvate")).unwrap();
    ffi::PyDict_SetItemString(
        di,
        ffi::c_str!("FileWrapper").as_ptr(),
        ty.as_object().as_ptr(),
    );
    pymod
}

unsafe extern "C" fn wrap(
    slf: *mut ffi::PyObject,
    args: *mut ffi::PyObject,
    kwargs: *mut ffi::PyObject,
) -> *mut ffi::PyObject {
    let kwlist: &[*mut c_char] = &[
        ffi::c_str!("application").as_ptr() as *mut c_char,
        ffi::c_str!("addr").as_ptr() as *mut c_char,
        ffi::c_str!("num_workers").as_ptr() as *mut c_char,
        ffi::c_str!("max_number_headers").as_ptr() as *mut c_char,
        ffi::c_str!("async_logging").as_ptr() as *mut c_char,
        ffi::c_str!("chunked_transfer").as_ptr() as *mut c_char,
        ffi::c_str!("max_reuse_count").as_ptr() as *mut c_char,
        ffi::c_str!("keepalive_timeout").as_ptr() as *mut c_char,
        ffi::c_str!("qmon_warn_threshold").as_ptr() as *mut c_char,
        ffi::c_str!("send_timeout").as_ptr() as *mut c_char,
        ptr::null_mut() as *mut c_char,
    ];
    // Defaults
    let application: *mut ffi::PyObject = ptr::null_mut();
    let addr: *mut c_char = ptr::null_mut();
    let num_workers: usize = 2;
    let max_number_headers: usize = 32;
    let async_logging = true;
    let chunked_transfer = false;
    let max_reuse_count: u8 = 0;
    let keepalive_timeout: u8 = 60;
    let qmon_warn_threshold = -1;
    let send_timeout: u8 = 60;

    #[cfg(not(Py_3_13))]
    if ffi::PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        ffi::c_str!("O|sHHppbbib").as_ptr() as *mut c_char,
        kwlist.as_ptr() as *mut *mut c_char,
        &application,
        &addr,
        &num_workers,
        &max_number_headers,
        &async_logging,
        &chunked_transfer,
        &max_reuse_count,
        &keepalive_timeout,
        &qmon_warn_threshold,
        &send_timeout,
    ) == 0
    {
        return ptr::null_mut();
    }
    #[cfg(Py_3_13)]
    if ffi::PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        ffi::c_str!("O|sHHppbbib").as_ptr() as *mut c_char,
        kwlist.as_ptr() as *const *const c_char,
        &application,
        &addr,
        &num_workers,
        &max_number_headers,
        &async_logging,
        &chunked_transfer,
        &max_reuse_count,
        &keepalive_timeout,
        &qmon_warn_threshold,
        &send_timeout,
    ) == 0
    {
        return ptr::null_mut();
    }

    let application = unsafe {
        let py = Python::assume_gil_acquired();
        PyObject::from_borrowed_ptr(py, application)
    };
    let addr = if addr.is_null() {
        None
    } else {
        match CStr::from_ptr(addr).to_str() {
            Ok(stri) => Some(String::from(stri)),
            Err(_) => None,
        }
    };

    let qmon_warn_threshold = if qmon_warn_threshold < 0 {
        None
    } else {
        Some(qmon_warn_threshold as usize)
    };

    let py = Python::assume_gil_acquired();
    match serve(
        py,
        application,
        addr,
        num_workers,
        max_number_headers,
        async_logging,
        chunked_transfer,
        max_reuse_count,
        keepalive_timeout,
        qmon_warn_threshold,
        send_timeout,
    ) {
        Ok(_) => {
            ffi::Py_INCREF(slf);
            slf
        }
        Err(e) => {
            e.restore(py);
            ptr::null_mut()
        }
    }
}
