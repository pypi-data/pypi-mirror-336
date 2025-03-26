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

use crate::err::PyResult;
use crate::ffi;
use crate::objects::PyObject;
use crate::python::{PyDrop, Python, PythonObject};

/// Conversion trait that allows various objects to be converted into Python objects.
///
/// Note: The associated type `ObjectType` is used so that some Rust types
/// convert to a more precise type of Python object.
/// For example, `[T]::to_py_object()` will result in a `PyList`.
/// You can always calls `val.to_py_object(py).into_py_object()` in order to obtain `PyObject`
/// (the second into_py_object() call via the PythonObject trait corresponds to the upcast from `PyList` to `PyObject`).
pub trait ToPyObject {
    type ObjectType: PythonObject;

    /// Converts self into a Python object.
    fn to_py_object(&self, py: Python) -> Self::ObjectType;

    /// Converts self into a Python object and calls the specified closure
    /// on the native FFI pointer underlying the Python object.
    ///
    /// May be more efficient than `to_py_object` because it does not need
    /// to touch any reference counts when the input object already is a Python object.
    #[inline]
    fn with_borrowed_ptr<F, R>(&self, py: Python, f: F) -> R
    where
        F: FnOnce(*mut ffi::PyObject) -> R,
    {
        let obj = self.to_py_object(py).into_object();
        let res = f(obj.as_ptr());
        obj.release_ref(py);
        res
    }

    // FFI functions that accept a borrowed reference will use:
    //   input.with_borrowed_ptr(|obj| ffi::Call(obj)
    // 1) input is &PyObject
    //   -> with_borrowed_ptr() just forwards to the closure
    // 2) input is PyObject
    //   -> with_borrowed_ptr() just forwards to the closure
    // 3) input is &str, int, ...
    //   -> to_py_object() allocates new Python object; FFI call happens; release_ref() calls Py_DECREF()

    // FFI functions that steal a reference will use:
    //   let input = input.into_py_object()?; ffi::Call(input.steal_ptr())
    // 1) input is &PyObject
    //   -> into_py_object() calls Py_INCREF
    // 2) input is PyObject
    //   -> into_py_object() is no-op
    // 3) input is &str, int, ...
    //   -> into_py_object() allocates new Python object
}

py_impl_to_py_object_for_python_object!(PyObject);

/// FromPyObject is implemented by various types that can be extracted from a Python object.
///
/// Normal usage is through the `PyObject::extract` helper method:
/// ```let obj: PyObject = ...;
/// let value = obj.extract::<TargetType>(py)?;
/// ```
///
/// Each target type for this conversion supports a different Python objects as input.
/// Calls with an unsupported input object will result in an exception (usually a `TypeError`).
///
/// This trait is also used by the `py_fn!` and `py_class!` and `py_argparse!` macros
/// in order to translate from Python objects to the expected Rust parameter types.
/// For example, the parameter `x` in `def method(self, x: i32)` will use
/// `impl FromPyObject for i32` to convert the input Python object into a Rust `i32`.
/// When these macros are used with reference parameters (`x: &str`), the trait
/// `RefFromPyObject` is used instead.
pub trait FromPyObject<'s>: Sized {
    /// Extracts `Self` from the source `PyObject`.
    fn extract(py: Python, obj: &'s PyObject) -> PyResult<Self>;
}

py_impl_from_py_object_for_python_object!(PyObject);

/// `ToPyObject` for references: calls to_py_object() on the underlying `T`.
impl<'a, T: ?Sized> ToPyObject for &'a T
where
    T: ToPyObject,
{
    type ObjectType = T::ObjectType;

    #[inline]
    fn to_py_object(&self, py: Python) -> T::ObjectType {
        <T as ToPyObject>::to_py_object(*self, py)
    }

    #[inline]
    fn with_borrowed_ptr<F, R>(&self, py: Python, f: F) -> R
    where
        F: FnOnce(*mut ffi::PyObject) -> R,
    {
        <T as ToPyObject>::with_borrowed_ptr(*self, py, f)
    }
}
