// Copyright (c) 2015 Daniel Grunwald
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this
// software and associated documentation files (the "Software"), to deal in the Software
// without restriction, including without limitation the rights to use, copy, modify, merge,
// publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
// to whom the Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all copies or
// substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
// FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

use std::{marker, rc, sync};

use crate::ffi;
use crate::python::Python;

static START: sync::Once = sync::Once::new();

/// RAII type that represents the Global Interpreter Lock acquisition.
///
/// # Example
/// ```
/// use cpython::Python;
///
/// {
///     let gil_guard = Python::acquire_gil();
///     let py = gil_guard.python();
/// } // GIL is released when gil_guard is dropped
/// ```
#[must_use]
pub struct GILGuard {
    gstate: ffi::PyGILState_STATE,
    // hack to opt out of Send on stable rust, which doesn't
    // have negative impls
    no_send: marker::PhantomData<rc::Rc<()>>,
}

/// The Drop implementation for GILGuard will release the GIL.
impl Drop for GILGuard {
    fn drop(&mut self) {
        unsafe { ffi::PyGILState_Release(self.gstate) }
    }
}

impl GILGuard {
    /// Acquires the global interpreter lock, which allows access to the Python runtime.
    ///
    /// If the Python runtime is not already initialized, this function will initialize it.
    /// See [prepare_freethreaded_python()](fn.prepare_freethreaded_python.html) for details.
    pub fn acquire() -> GILGuard {
        // Protect against race conditions when Python is not yet initialized
        // and multiple threads concurrently call 'prepare_freethreaded_python()'.
        // Note that we do not protect against concurrent initialization of the Python runtime
        // by other users of the Python C API.
        START.call_once(|| unsafe {
            if ffi::Py_IsInitialized() == 0 {
                // Initialize Python.
                // We use Py_InitializeEx() with initsigs=-1 to disable Python signal handling.
                // Signal handling depends on the notion of a 'main thread', which doesn't exist in this case.
                // Note that the 'main thread' notion in Python isn't documented properly;
                // and running Python without one is not officially supported.
                ffi::Py_InitializeEx(0);
                // Immediately release the GIL:
                let _thread_state = ffi::PyEval_SaveThread();
                // Note that the PyThreadState returned by PyEval_SaveThread is also held in TLS by the Python runtime,
                // and will be restored by PyGILState_Ensure.
            }
        });
        let gstate = unsafe { ffi::PyGILState_Ensure() }; // acquire GIL
        GILGuard {
            gstate,
            no_send: marker::PhantomData,
        }
    }

    /// Retrieves the marker type that proves that the GIL was acquired.
    #[inline]
    pub fn python(&self) -> Python<'_> {
        unsafe { Python::assume_gil_acquired() }
    }

}
