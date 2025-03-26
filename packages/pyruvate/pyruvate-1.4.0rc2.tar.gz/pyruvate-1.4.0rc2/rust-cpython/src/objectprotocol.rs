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

use std::fmt;

use crate::conversion::ToPyObject;
use crate::err::{self, PyResult};
use crate::ffi;
use crate::objects::{PyDict, PyObject, PyString, PyTuple};
use crate::python::{Python, PythonObject, ToPythonPointer};

/// Trait that contains methods
pub trait ObjectProtocol: PythonObject {
    /// Determines whether this object has the given attribute.
    /// This is equivalent to the Python expression 'hasattr(self, attr_name)'.
    #[inline]
    fn hasattr<N>(&self, py: Python, attr_name: N) -> PyResult<bool>
    where
        N: ToPyObject,
    {
        attr_name.with_borrowed_ptr(py, |attr_name| unsafe {
            Ok(ffi::PyObject_HasAttr(self.as_ptr(), attr_name) != 0)
        })
    }

    /// Retrieves an attribute value.
    /// This is equivalent to the Python expression 'self.attr_name'.
    #[inline]
    fn getattr<N>(&self, py: Python, attr_name: N) -> PyResult<PyObject>
    where
        N: ToPyObject,
    {
        attr_name.with_borrowed_ptr(py, |attr_name| unsafe {
            err::result_from_owned_ptr(py, ffi::PyObject_GetAttr(self.as_ptr(), attr_name))
        })
    }

    /// Sets an attribute value.
    /// This is equivalent to the Python expression 'self.attr_name = value'.
    #[inline]
    fn setattr<N, V>(&self, py: Python, attr_name: N, value: V) -> PyResult<()>
    where
        N: ToPyObject,
        V: ToPyObject,
    {
        attr_name.with_borrowed_ptr(py, move |attr_name| {
            value.with_borrowed_ptr(py, |value| unsafe {
                err::error_on_minusone(py, ffi::PyObject_SetAttr(self.as_ptr(), attr_name, value))
            })
        })
    }

    /// Compute the string representation of self.
    /// This is equivalent to the Python expression 'repr(self)'.
    #[inline]
    fn repr(&self, py: Python) -> PyResult<PyString> {
        unsafe { err::result_cast_from_owned_ptr(py, ffi::PyObject_Repr(self.as_ptr())) }
    }

    /// Compute the string representation of self.
    /// This is equivalent to the Python expression 'str(self)'.
    #[inline]
    fn str(&self, py: Python) -> PyResult<PyString> {
        unsafe { err::result_cast_from_owned_ptr(py, ffi::PyObject_Str(self.as_ptr())) }
    }

    /// Calls the object.
    /// This is equivalent to the Python expression: 'self(*args, **kwargs)'
    ///
    /// `args` should be a value that, when converted to Python, results in a tuple.
    /// For this purpose, you can use:
    ///  * `cpython::NoArgs` when calling a method without any arguments
    ///  * otherwise, a Rust tuple with 1 or more elements
    #[inline]
    fn call<A>(&self, py: Python, args: A, kwargs: Option<&PyDict>) -> PyResult<PyObject>
    where
        A: ToPyObject<ObjectType = PyTuple>,
    {
        args.with_borrowed_ptr(py, |args| unsafe {
            let res = ffi::PyObject_Call(self.as_ptr(), args, kwargs.as_ptr());
            err::result_from_owned_ptr(py, res)
        })
    }

    /// Calls a method on the object.
    /// This is equivalent to the Python expression: 'self.name(*args, **kwargs)'
    ///
    /// `args` should be a value that, when converted to Python, results in a tuple.
    /// For this purpose, you can use:
    ///  * `cpython::NoArgs` when calling a method without any arguments
    ///  * otherwise, a Rust tuple with 1 or more elements
    ///
    /// # Example
    /// ```no_run
    /// use cpython::{NoArgs, ObjectProtocol};
    /// # use cpython::Python;
    /// # let gil = Python::acquire_gil();
    /// # let py = gil.python();
    /// # let obj = py.None();
    /// // Call method without arguments:
    /// let value = obj.call_method(py, "method0", NoArgs, None).unwrap();
    /// // Call method with a single argument:
    /// obj.call_method(py, "method1", (true,), None).unwrap();
    /// ```
    #[inline]
    fn call_method<A>(
        &self,
        py: Python,
        name: &str,
        args: A,
        kwargs: Option<&PyDict>,
    ) -> PyResult<PyObject>
    where
        A: ToPyObject<ObjectType = PyTuple>,
    {
        self.getattr(py, name)?.call(py, args, kwargs)
    }
}

impl ObjectProtocol for PyObject {}

impl fmt::Debug for PyObject {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        // TODO: we shouldn't use fmt::Error when repr() fails
        let gil_guard = Python::acquire_gil();
        let py = gil_guard.python();
        let repr_obj = self.repr(py).map_err(|_| fmt::Error)?;
        f.write_str(&repr_obj.to_string_lossy(py))
    }
}

impl fmt::Display for PyObject {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        // TODO: we shouldn't use fmt::Error when str() fails
        let gil_guard = Python::acquire_gil();
        let py = gil_guard.python();
        let str_obj = self.str(py).map_err(|_| fmt::Error)?;
        f.write_str(&str_obj.to_string_lossy(py))
    }
}
