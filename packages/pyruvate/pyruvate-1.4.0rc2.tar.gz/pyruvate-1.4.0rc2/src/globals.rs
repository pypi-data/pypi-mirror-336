use cpython::{PyDict, PyErr, PyModule, PyResult, PyString, Python};
use log::{debug, error};
use std::sync::Arc;
use std::time::Duration;

use crate::transport::SharedConnectionOptions;

pub struct WSGIOptions {
    pub io_module: PyModule,
    pub wsgi_environ: PyDict,
    pub peer_addr_key: PyString,
    pub content_length_key: PyString,
    pub wsgi_input_key: PyString,
    pub chunked_transfer: bool,
    pub qmon_warn_threshold: Option<usize>,
    pub send_timeout: Duration,
}

impl WSGIOptions {
    pub fn new(
        server_name: String,
        server_port: String,
        script_name: String,
        chunked_transfer: bool,
        qmon_warn_threshold: Option<usize>,
        send_timeout: Duration,
        py: Python,
    ) -> WSGIOptions {
        // XXX work around not being able to import wsgi module from tests
        let wsgi_module = match py.import("pyruvate") {
            Ok(pyruvate) => Some(pyruvate),
            Err(_) => {
                error!("Could not import WSGI module, so no FileWrapper");
                PyErr::fetch(py);
                None
            }
        };
        let sys_module = py.import("sys").expect("Could not import module sys");
        let wsgi_environ = Self::prepare_wsgi_environ(
            &server_name,
            &server_port,
            &script_name,
            &sys_module,
            wsgi_module.as_ref(),
            py,
        )
        .expect("Could not create wsgi environ template");
        WSGIOptions {
            io_module: py.import("io").expect("Could not import module io"),
            wsgi_environ,
            peer_addr_key: PyString::new(py, "REMOTE_ADDR"),
            content_length_key: PyString::new(py, "CONTENT_LENGTH"),
            wsgi_input_key: PyString::new(py, "wsgi.input"),
            chunked_transfer,
            qmon_warn_threshold,
            send_timeout,
        }
    }

    fn prepare_wsgi_environ(
        server_name: &str,
        server_port: &str,
        script_name: &str,
        sys: &PyModule,
        wsgi: Option<&PyModule>,
        py: Python,
    ) -> PyResult<PyDict> {
        let environ = PyDict::new(py);
        environ.set_item(py, "SERVER_NAME", server_name)?;
        environ.set_item(py, "SERVER_PORT", server_port)?;
        environ.set_item(py, "SCRIPT_NAME", script_name)?;
        environ.set_item(py, "wsgi.errors", sys.get(py, "stderr")?)?;
        environ.set_item(py, "wsgi.version", (1, 0))?;
        environ.set_item(py, "wsgi.multithread", false)?;
        environ.set_item(py, "wsgi.multiprocess", true)?;
        environ.set_item(py, "wsgi.run_once", false)?;
        environ.set_item(py, "wsgi.url_scheme", "http")?;
        if let Some(wsgi) = wsgi {
            debug!("Setting FileWrapper in environ");
            environ.set_item(py, "wsgi.file_wrapper", wsgi.get(py, "FileWrapper")?)?;
        }
        Ok(environ)
    }
}

pub type SharedWSGIOptions = Arc<WSGIOptions>;

pub fn shared_wsgi_options(
    server_name: String,
    server_port: String,
    script_name: String,
    chunked_transfer: bool,
    qmon_warn_threshold: Option<usize>,
    send_timeout: Duration,
    py: Python,
) -> SharedWSGIOptions {
    Arc::new(WSGIOptions::new(
        server_name,
        server_port,
        script_name,
        chunked_transfer,
        qmon_warn_threshold,
        send_timeout,
        py,
    ))
}

pub struct ServerOptions {
    pub num_workers: usize,
    pub max_number_headers: usize,
    pub connection_options: SharedConnectionOptions,
    pub wsgi_options: SharedWSGIOptions,
}

#[cfg(test)]
mod tests {
    use crate::globals::WSGIOptions;
    use cpython::{FromPyObject, PyString, Python};
    use log::debug;
    use std::time::Duration;

    #[test]
    fn test_creation() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let sn = String::from("127.0.0.1");
        let sp = String::from("7878");
        let script = String::from("/foo");
        let pypath = py.import("sys").unwrap().get(py, "path").unwrap();
        debug!("sys.path: {:?}", pypath);
        let got = WSGIOptions::new(
            sn.clone(),
            sp.clone(),
            script.clone(),
            false,
            None,
            Duration::from_secs(60),
            py,
        );
        match got.wsgi_environ.get_item(py, "SERVER_NAME") {
            Some(pyob) => {
                assert!(PyString::extract(py, &pyob).unwrap().to_string(py).unwrap() == sn)
            }
            None => assert!(false),
        }
        match got.wsgi_environ.get_item(py, "SERVER_PORT") {
            Some(pyob) => {
                assert!(PyString::extract(py, &pyob).unwrap().to_string(py).unwrap() == sp)
            }
            None => assert!(false),
        }
        match got.wsgi_environ.get_item(py, "SCRIPT_NAME") {
            Some(pyob) => {
                assert!(PyString::extract(py, &pyob).unwrap().to_string(py).unwrap() == script)
            }
            None => assert!(false),
        }
    }
}
