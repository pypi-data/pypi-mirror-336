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

#![allow(clippy::transmute_ptr_to_ptr,static_mut_refs)]
use crate::conversion::{FromPyObject, ToPyObject};
use crate::err::{self, PyErr, PyResult};
use crate::ffi;
use crate::objectprotocol::ObjectProtocol;
use crate::python::{
    PyDrop, Python, PythonObject, PythonObjectDowncastError, PythonObjectWithCheckedDowncast,
    PythonObjectWithTypeObject, ToPythonPointer,
};

use libc::{c_char, c_long};
use num_traits::cast::cast;
use std::borrow::Cow;
use std::{char, str};
use std::ffi::{CStr, CString};
use std::{mem, ptr};
pub use std::result::Result;

#[macro_export]
macro_rules! pyobject_newtype(
    ($name: ident) => (
        $crate::py_impl_to_py_object_for_python_object!($name);
        $crate::py_impl_from_py_object_for_python_object!($name);

        impl $crate::PythonObject for $name {
            #[inline]
            fn as_object(&self) -> &$crate::PyObject {
                &self.0
            }

            #[inline]
            fn into_object(self) -> $crate::PyObject {
                self.0
            }

            /// Unchecked downcast from PyObject to Self.
            /// Undefined behavior if the input object does not have the expected type.
            #[inline]
            unsafe fn unchecked_downcast_from(obj: $crate::PyObject) -> Self {
                $name(obj)
            }
        }
    );
    ($name: ident, $checkfunction: ident) => (
        pyobject_newtype!($name);

        impl crate::python::PythonObjectWithCheckedDowncast for $name {
            #[inline]
            fn downcast_from<'p>(py: crate::python::Python<'p>, obj: PyObject) -> Result<$name, crate::python::PythonObjectDowncastError<'p>> {
                unsafe {
                    if crate::ffi::$checkfunction(obj.as_ptr()) != 0 {
                        Ok($name(obj))
                    } else {
                        Err(crate::python::PythonObjectDowncastError::new(
                            py,
                            stringify!($name),
                            obj.get_type(py)
                        ))
                    }
                }
            }

            #[inline]
            fn downcast_borrow_from<'a, 'p>(py: crate::python::Python<'p>, obj: &'a PyObject) -> Result<&'a $name, crate::python::PythonObjectDowncastError<'p>> {
                unsafe {
                    if crate::ffi::$checkfunction(obj.as_ptr()) != 0 {
                        Ok(std::mem::transmute(obj))
                    } else {
                        Err(crate::python::PythonObjectDowncastError::new(
                            py,
                            stringify!($name),
                            obj.get_type(py)
                        ))
                    }
                }
            }
        }
    );
    ($name: ident, $checkfunction: ident, $typeobject: ident) => (
        pyobject_newtype!($name, $checkfunction);

        impl crate::python::PythonObjectWithTypeObject for $name {
            #[inline]
            fn type_object(py: crate::python::Python) -> PyType {
                unsafe { PyType::from_type_ptr(py, &mut crate::ffi::$typeobject) }
            }
        }
    );
);

macro_rules! extract(
    ($obj:ident to $t:ty; $(#[$meta:meta])* $py:ident => $body: block) => {
        impl <'s> crate::conversion::FromPyObject<'s>
            for $t
        {
            $(#[$meta])*
            fn extract($py: Python, $obj: &'s PyObject) -> PyResult<Self> {
                $body
            }
        }
    }
);

/// Represents a Python `bool`.
pub struct PyBool(PyObject);

pyobject_newtype!(PyBool, PyBool_Check, PyBool_Type);

impl PyBool {
    /// Depending on `val`, returns `py.True()` or `py.False()`.
    #[inline]
    pub fn get(py: Python, val: bool) -> PyBool {
        if val {
            unsafe { PyObject::from_borrowed_ptr(py, ffi::Py_True()).unchecked_cast_into::<PyBool>() }
        } else {
            unsafe { PyObject::from_borrowed_ptr(py, ffi::Py_False()).unchecked_cast_into::<PyBool>() }
        }
    }

    /// Gets whether this boolean is `true`.
    #[inline]
    pub fn is_true(&self) -> bool {
        self.0.as_ptr() == unsafe { crate::ffi::Py_True() }
    }
}

// mod boolobject;
/// Converts a rust `bool` to a Python `bool`.
impl ToPyObject for bool {
    type ObjectType = PyBool;

    #[inline]
    fn to_py_object(&self, py: Python) -> PyBool {
        PyBool::get(py, *self)
    }

    #[inline]
    fn with_borrowed_ptr<F, R>(&self, _py: Python, f: F) -> R
    where
        F: FnOnce(*mut ffi::PyObject) -> R,
    {
        // Avoid unnecessary Py_INCREF/Py_DECREF pair
        f(unsafe {
            if *self {
                ffi::Py_True()
            } else {
                ffi::Py_False()
            }
        })
    }
}
// mod dict;
/// Represents a Python `dict`.
pub struct PyDict(PyObject);

pyobject_newtype!(PyDict, PyDict_Check, PyDict_Type);

impl PyDict {
    /// Creates a new empty dictionary.
    ///
    /// May panic when running out of memory.
    pub fn new(py: Python) -> PyDict {
        unsafe { err::cast_from_owned_ptr_or_panic(py, ffi::PyDict_New()) }
    }

    /// Return a new dictionary that contains the same key-value pairs as self.
    /// Corresponds to `dict(self)` in Python.
    pub fn copy(&self, py: Python) -> PyResult<PyDict> {
        unsafe { err::result_cast_from_owned_ptr(py, ffi::PyDict_Copy(self.0.as_ptr())) }
    }

    /// Return the number of items in the dictionary.
    /// This is equivalent to len(p) on a dictionary.
    #[inline]
    pub fn len(&self, _py: Python) -> usize {
        unsafe { ffi::PyDict_Size(self.0.as_ptr()) as usize }
    }

    /// Gets an item from the dictionary.
    /// Returns None if the item is not present, or if an error occurs.
    pub fn get_item<K>(&self, py: Python, key: K) -> Option<PyObject>
    where
        K: ToPyObject,
    {
        key.with_borrowed_ptr(py, |key| unsafe {
            PyObject::from_borrowed_ptr_opt(py, ffi::PyDict_GetItem(self.0.as_ptr(), key))
        })
    }

    /// Sets an item value.
    /// This is equivalent to the Python expression `self[key] = value`.
    pub fn set_item<K, V>(&self, py: Python, key: K, value: V) -> PyResult<()>
    where
        K: ToPyObject,
        V: ToPyObject,
    {
        key.with_borrowed_ptr(py, move |key| {
            value.with_borrowed_ptr(py, |value| unsafe {
                err::error_on_minusone(py, ffi::PyDict_SetItem(self.0.as_ptr(), key, value))
            })
        })
    }
}
// pub mod exc;
macro_rules! exc_type(
    ($name:ident, $exc_name:ident) => (
        pub struct $name(PyObject);

        pyobject_newtype!($name);

        impl PythonObjectWithCheckedDowncast for $name {
            #[inline]
            fn downcast_from<'p>(py: Python<'p>, obj : PyObject)
                -> Result<$name, PythonObjectDowncastError<'p>>
            {
                unsafe {
                    if ffi::PyObject_TypeCheck(obj.as_ptr(), ffi::$exc_name as *mut ffi::PyTypeObject) != 0 {
                        Ok(PythonObject::unchecked_downcast_from(obj))
                    } else {
                        Err(PythonObjectDowncastError::new(
                            py,
                            stringify!($name),
                            obj.get_type(py),
                        ))
                    }
                }
            }

            #[inline]
            fn downcast_borrow_from<'a, 'p>(py: Python<'p>, obj: &'a PyObject)
                -> Result<&'a $name, PythonObjectDowncastError<'p>>
            {
                unsafe {
                    if ffi::PyObject_TypeCheck(obj.as_ptr(), ffi::$exc_name as *mut ffi::PyTypeObject) != 0 {
                        Ok(std::mem::transmute(obj))
                    } else {
                        Err(PythonObjectDowncastError::new(
                            py,
                            stringify!($name),
                            obj.get_type(py),
                        ))
                    }
                }
            }
        }

        impl PythonObjectWithTypeObject for $name {
            #[inline]
            fn type_object(py: Python) -> PyType {
                unsafe { PyType::from_type_ptr(py, ffi::$exc_name as *mut ffi::PyTypeObject) }
            }
        }
    );
);

exc_type!(BaseException, PyExc_BaseException);
exc_type!(Exception, PyExc_Exception);
exc_type!(LookupError, PyExc_LookupError);
exc_type!(AssertionError, PyExc_AssertionError);
exc_type!(AttributeError, PyExc_AttributeError);
exc_type!(BlockingIOError, PyExc_BlockingIOError);
exc_type!(BrokenPipeError, PyExc_BrokenPipeError);
exc_type!(ChildProcessError, PyExc_ChildProcessError);
exc_type!(ConnectionAbortedError, PyExc_ConnectionAbortedError);
exc_type!(ConnectionError, PyExc_ConnectionError);
exc_type!(ConnectionRefusedError, PyExc_ConnectionRefusedError);
exc_type!(ConnectionResetError, PyExc_ConnectionResetError);
exc_type!(EOFError, PyExc_EOFError);
exc_type!(EnvironmentError, PyExc_EnvironmentError);
exc_type!(FileExistsError, PyExc_FileExistsError);
exc_type!(FileNotFoundError, PyExc_FileNotFoundError);
exc_type!(FloatingPointError, PyExc_FloatingPointError);
exc_type!(IOError, PyExc_IOError);
exc_type!(ImportError, PyExc_ImportError);
exc_type!(IndexError, PyExc_IndexError);
exc_type!(InterruptedError, PyExc_InterruptedError);
exc_type!(IsADirectoryError, PyExc_IsADirectoryError);
exc_type!(KeyError, PyExc_KeyError);
exc_type!(KeyboardInterrupt, PyExc_KeyboardInterrupt);
exc_type!(MemoryError, PyExc_MemoryError);
exc_type!(NameError, PyExc_NameError);
exc_type!(NotADirectoryError, PyExc_NotADirectoryError);
exc_type!(NotImplementedError, PyExc_NotImplementedError);
exc_type!(OSError, PyExc_OSError);
exc_type!(OverflowError, PyExc_OverflowError);
exc_type!(PermissionError, PyExc_PermissionError);
exc_type!(ProcessLookupError, PyExc_ProcessLookupError);
exc_type!(ReferenceError, PyExc_ReferenceError);
exc_type!(RuntimeError, PyExc_RuntimeError);
exc_type!(SyntaxError, PyExc_SyntaxError);
exc_type!(SystemError, PyExc_SystemError);
exc_type!(SystemExit, PyExc_SystemExit);
exc_type!(TimeoutError, PyExc_TimeoutError);
exc_type!(TypeError, PyExc_TypeError);
exc_type!(ValueError, PyExc_ValueError);
exc_type!(ZeroDivisionError, PyExc_ZeroDivisionError);

exc_type!(BufferError, PyExc_BufferError);

exc_type!(UnicodeDecodeError, PyExc_UnicodeDecodeError);
exc_type!(UnicodeEncodeError, PyExc_UnicodeEncodeError);
exc_type!(UnicodeTranslateError, PyExc_UnicodeTranslateError);
// mod iterator;
/// A python iterator object.
///
/// Unlike other python objects, this class includes a `Python<'p>` token
/// so that PyIterator can implement the rust `Iterator` trait.
pub struct PyIterator<'p> {
    py: Python<'p>,
    iter: PyObject,
}

impl<'p> PyIterator<'p> {
    /// Constructs a PyIterator from a Python iterator object.
    pub fn from_object(
        py: Python<'p>,
        obj: PyObject,
    ) -> Result<PyIterator<'p>, PythonObjectDowncastError<'p>> {
        if unsafe { ffi::PyIter_Check(obj.as_ptr()) != 0 } {
            Ok(PyIterator { py, iter: obj })
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "PyIterator",
                obj.get_type(py),
            ))
        }
    }
}

impl<'p> Iterator for PyIterator<'p> {
    type Item = PyResult<PyObject>;

    /// Retrieves the next item from an iterator.
    /// Returns `None` when the iterator is exhausted.
    /// If an exception occurs, returns `Some(Err(..))`.
    /// Further next() calls after an exception occurs are likely
    /// to repeatedly result in the same exception.
    fn next(&mut self) -> Option<PyResult<PyObject>> {
        let py = self.py;
        match unsafe { PyObject::from_owned_ptr_opt(py, ffi::PyIter_Next(self.iter.as_ptr())) } {
            Some(obj) => Some(Ok(obj)),
            None => {
                if PyErr::occurred(py) {
                    Some(Err(PyErr::fetch(py)))
                } else {
                    None
                }
            }
        }
    }
}
// mod list;
/// Represents a Python `list`.
pub struct PyList(PyObject);

pyobject_newtype!(PyList, PyList_Check, PyList_Type);

impl PyList {

    /// Gets the length of the list.
    #[inline]
    pub fn len(&self, _py: Python) -> usize {
        // non-negative Py_ssize_t should always fit into Rust usize
        unsafe { ffi::PyList_Size(self.0.as_ptr()) as usize }
    }

    /// Gets the item at the specified index.
    ///
    /// Panics if the index is out of range.
    pub fn get_item(&self, py: Python, index: usize) -> PyObject {
        // TODO: do we really want to panic here?
        assert!(index < self.len(py));
        unsafe {
            PyObject::from_borrowed_ptr(
                py,
                ffi::PyList_GetItem(self.0.as_ptr(), index as ffi::Py_ssize_t),
            )
        }
    }

    #[inline]
    pub fn iter<'a, 'p>(&'a self, py: Python<'p>) -> PyListIterator<'a, 'p> {
        PyListIterator {
            py,
            list: self,
            index: 0,
        }
    }
}

/// Used by `PyList::iter()`.
pub struct PyListIterator<'a, 'p> {
    py: Python<'p>,
    list: &'a PyList,
    index: usize,
}

impl<'a, 'p> Iterator for PyListIterator<'a, 'p> {
    type Item = PyObject;

    #[inline]
    fn next(&mut self) -> Option<PyObject> {
        if self.index < self.list.len(self.py) {
            let item = self.list.get_item(self.py, self.index);
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    // Note: we cannot implement size_hint because the length of the list
    // might change during the iteration.
}
// mod module;
/// Represents a Python module object.
pub struct PyModule(PyObject);

pyobject_newtype!(PyModule, PyModule_Check, PyModule_Type);

impl PyModule {
    /// Import the Python module with the specified name.
    pub fn import(py: Python, name: &str) -> PyResult<PyModule> {
        let name = CString::new(name).unwrap();
        unsafe { err::result_cast_from_owned_ptr(py, ffi::PyImport_ImportModule(name.as_ptr())) }
    }

    /// Gets a member from the module.
    /// This is equivalent to the Python expression: `getattr(module, name)`
    pub fn get(&self, py: Python, name: &str) -> PyResult<PyObject> {
        self.as_object().getattr(py, name)
    }

    /// Calls a function in the module.
    /// This is equivalent to the Python expression: `getattr(module, name)(*args, **kwargs)`
    ///
    /// `args` should be a value that, when converted to Python, results in a tuple.
    /// For this purpose, you can use:
    ///  * `cpython::NoArgs` when calling a method without any arguments
    ///  * otherwise, a Rust tuple with 1 or more elements
    ///
    /// # Example
    /// ```
    /// use cpython::NoArgs;
    /// # use cpython::Python;
    /// # let gil = Python::acquire_gil();
    /// # let py = gil.python();
    /// let sys = py.import("sys").unwrap();
    /// // Call function without arguments:
    /// let encoding = sys.call(py, "getdefaultencoding", NoArgs, None).unwrap();
    /// // Call function with a single argument:
    /// sys.call(py, "setrecursionlimit", (1000,), None).unwrap();
    /// ```
    pub fn call<A>(
        &self,
        py: Python,
        name: &str,
        args: A,
        kwargs: Option<&PyDict>,
    ) -> PyResult<PyObject>
    where
        A: ToPyObject<ObjectType = PyTuple>,
    {
        self.as_object().getattr(py, name)?.call(py, args, kwargs)
    }
}
// mod num;
/// In Python 3.x, represents a Python `int` object.
/// Both `PyInt` and `PyLong` refer to the same type on Python 3.x.
///
/// You can usually avoid directly working with this type
/// by using [ToPyObject](trait.ToPyObject.html)
/// and [extract](struct.PyObject.html#method.extract)
/// with the primitive Rust integer types.
pub struct PyLong(PyObject);
pyobject_newtype!(PyLong, PyLong_Check, PyLong_Type);

macro_rules! int_fits_c_long(
    ($rust_type:ty) => (
        /// Conversion of Rust integer to Python `int`.
        impl ToPyObject for $rust_type {
            type ObjectType = PyLong;

            fn to_py_object(&self, py: Python) -> PyLong {
                unsafe {
                    err::cast_from_owned_ptr_or_panic(py,
                        ffi::PyLong_FromLong(*self as c_long))
                }
            }
        }

        extract!(
            obj to $rust_type;
            /// Converts Python integers to Rust integers.
            ///
            /// Returns OverflowError if the input integer does not fit the Rust type;
            /// or TypeError if the input is not an integer.
            py => {
                let ptr = obj.as_ptr();
                let val;
                unsafe {
                    if ffi::PyLong_Check(ptr) != 0 {
                        val = ffi::PyLong_AsLong(obj.as_ptr());
                    } else {
                        let num = err::result_from_owned_ptr(py, ffi::PyNumber_Index(ptr))?;
                        val = ffi::PyLong_AsLong(num.as_ptr());
                        num.release_ref(py);
                    }
                };
                if val == -1 && PyErr::occurred(py) {
                    return Err(PyErr::fetch(py));
                }
                match cast::<c_long, $rust_type>(val) {
                    Some(v) => Ok(v),
                    None => Err(overflow_error(py))
                }
            }
        );
    )
);

macro_rules! int_fits_larger_int(
    ($rust_type:ty, $larger_type:ty) => (
        /// Conversion of Rust integer to Python `int`.
        /// On Python 2.x, may also result in a `long` if the value does not fit into a Python `int`.
        impl ToPyObject for $rust_type {
            type ObjectType = <$larger_type as ToPyObject>::ObjectType;

            #[inline]
            fn to_py_object(&self, py: Python) -> <$larger_type as ToPyObject>::ObjectType {
                (*self as $larger_type).to_py_object(py)
            }
        }
    )
);

macro_rules! int_convert_u64_or_i64 (
    ($rust_type:ty, $pylong_from_ll_or_ull:expr, $pylong_as_ull_or_ull:expr) => (
        /// Conversion of Rust integer to Python `int`.
        /// On Python 2.x, may also result in a `long` if the value does not fit into a Python `int`.
        impl <'p> ToPyObject for $rust_type {
            type ObjectType = PyLong;

            fn to_py_object(&self, py: Python) -> PyLong {
                unsafe {
                    err::cast_from_owned_ptr_or_panic(py, $pylong_from_ll_or_ull(*self))
                }
            }
        }
    )
);

int_fits_c_long!(i8);
int_fits_c_long!(u8);
int_fits_c_long!(i16);
int_fits_c_long!(u16);
int_fits_c_long!(i32);

// If c_long is 64-bits, we can use more types with int_fits_c_long!:
#[cfg(all(target_pointer_width = "64", not(target_os = "windows")))]
int_fits_c_long!(u32);

#[cfg(all(target_pointer_width = "64", not(target_os = "windows")))]
int_fits_c_long!(i64);

#[cfg(all(target_pointer_width = "64", not(target_os = "windows")))]
int_fits_c_long!(isize);

int_fits_larger_int!(usize, u64);

// u64 has a manual implementation as it never fits into signed long
int_convert_u64_or_i64!(
    u64,
    ffi::PyLong_FromUnsignedLongLong,
    ffi::PyLong_AsUnsignedLongLong
);

fn overflow_error(py: Python) -> PyErr {
    PyErr::new_lazy_init(py.get_type::<OverflowError>(), None)
}
// mod object;
/// Represents a reference to a Python object.
///
/// Python objects are reference counted.
/// Calling `clone_ref()` on a `PyObject` will return a new reference to the same object
/// (thus incrementing the reference count).
/// The `Drop` implementation will automatically decrement the reference count.
/// You can also call `release_ref()` to explicitly decrement the reference count.
/// This is slightly faster than relying on automatic drop, because `release_ref`
/// does not need to check whether the GIL needs to be acquired.
///
/// `PyObject` can be used with all Python objects, since all python types
/// derive from `object`. This crate also contains other, more specific types
/// that serve as references to Python objects (e.g. `PyTuple` for Python tuples, etc.).
///
/// You can convert from any Python object to `PyObject` by calling `as_object()` or `into_object()`
/// from the [PythonObject trait](trait.PythonObject.html).
/// In the other direction, you can call `cast_as()` or `cast_into()`
/// on `PyObject` to convert to more specific object types.
///
/// Most of the interesting methods are provided by the [ObjectProtocol trait](trait.ObjectProtocol.html).
#[repr(C)]
pub struct PyObject {
    // PyObject owns one reference to the *PyObject
    // ptr is not null
    ptr: ptr::NonNull<ffi::PyObject>,
}

// PyObject is thread-safe, because all operations on it require a Python<'p> token.
unsafe impl Send for PyObject {}
unsafe impl Sync for PyObject {}

/// Dropping a `PyObject` decrements the reference count on the object by 1.
impl Drop for PyObject {
    fn drop(&mut self) {
        let _gil_guard = Python::acquire_gil();
        unsafe {
            ffi::Py_DECREF(self.ptr.as_ptr());
        }
    }
}

impl PythonObject for PyObject {
    #[inline]
    fn as_object(&self) -> &PyObject {
        self
    }

    #[inline]
    fn into_object(self) -> PyObject {
        self
    }

    #[inline]
    unsafe fn unchecked_downcast_from(o: PyObject) -> PyObject {
        o
    }
}

impl PythonObjectWithCheckedDowncast for PyObject {
    #[inline]
    fn downcast_from(
        _py: Python<'_>,
        obj: PyObject,
    ) -> Result<PyObject, PythonObjectDowncastError<'_>> {
        Ok(obj)
    }

    #[inline]
    fn downcast_borrow_from<'a, 'p>(
        _py: Python<'p>,
        obj: &'a PyObject,
    ) -> Result<&'a PyObject, PythonObjectDowncastError<'p>> {
        Ok(obj)
    }
}

impl PyObject {
    /// Creates a PyObject instance for the given FFI pointer.
    /// This moves ownership over the pointer into the PyObject.
    /// Undefined behavior if the pointer is NULL or invalid.
    #[inline]
    pub unsafe fn from_owned_ptr(_py: Python, ptr: *mut ffi::PyObject) -> PyObject {
        debug_assert!(!ptr.is_null() && ffi::Py_REFCNT(ptr) > 0);
        PyObject {
            ptr: ptr::NonNull::new_unchecked(ptr),
        }
    }

    /// Creates a PyObject instance for the given FFI pointer.
    /// Calls Py_INCREF() on the ptr.
    /// Undefined behavior if the pointer is NULL or invalid.
    #[inline]
    pub unsafe fn from_borrowed_ptr(_py: Python, ptr: *mut ffi::PyObject) -> PyObject {
        debug_assert!(!ptr.is_null() && ffi::Py_REFCNT(ptr) > 0);
        ffi::Py_INCREF(ptr);
        PyObject {
            ptr: ptr::NonNull::new_unchecked(ptr),
        }
    }

    /// Creates a PyObject instance for the given FFI pointer.
    /// This moves ownership over the pointer into the PyObject.
    /// Returns None for null pointers; undefined behavior if the pointer is invalid.
    #[inline]
    pub unsafe fn from_owned_ptr_opt(py: Python, ptr: *mut ffi::PyObject) -> Option<PyObject> {
        if ptr.is_null() {
            None
        } else {
            Some(PyObject::from_owned_ptr(py, ptr))
        }
    }

    /// Returns None for null pointers; undefined behavior if the pointer is invalid.
    #[inline]
    pub unsafe fn from_borrowed_ptr_opt(py: Python, ptr: *mut ffi::PyObject) -> Option<PyObject> {
        if ptr.is_null() {
            None
        } else {
            Some(PyObject::from_borrowed_ptr(py, ptr))
        }
    }

    /// Gets the underlying FFI pointer.
    /// Returns a borrowed pointer.
    #[inline]
    pub fn as_ptr(&self) -> *mut ffi::PyObject {
        self.ptr.as_ptr()
    }

    /// Gets the underlying FFI pointer.
    /// Consumes `self` without calling `Py_DECREF()`, thus returning an owned pointer.
    #[inline]
    #[must_use]
    pub fn steal_ptr(self) -> *mut ffi::PyObject {
        let ptr = self.as_ptr();
        mem::forget(self);
        ptr
    }

    /// Gets the reference count of this Python object.
    #[inline]
    pub fn get_refcnt(&self, _py: Python) -> usize {
        unsafe { ffi::Py_REFCNT(self.as_ptr()) as usize }
    }

    /// Gets the Python type object for this object's type.
    pub fn get_type(&self, py: Python) -> PyType {
        unsafe { PyType::from_type_ptr(py, (*self.as_ptr()).ob_type) }
    }

    /// Casts the PyObject to a concrete Python object type.
    /// Causes undefined behavior if the object is not of the expected type.
    /// This is a wrapper function around `PythonObject::unchecked_downcast_from()`.
    #[inline]
    pub unsafe fn unchecked_cast_into<T>(self) -> T
    where
        T: PythonObject,
    {
        PythonObject::unchecked_downcast_from(self)
    }

    /// Casts the PyObject to a concrete Python object type.
    /// Fails with `PythonObjectDowncastError` if the object is not of the expected type.
    /// This is a wrapper function around `PythonObjectWithCheckedDowncast::downcast_from()`.
    #[inline]
    pub fn cast_into<T>(self, py: Python<'_>) -> Result<T, PythonObjectDowncastError<'_>>
    where
        T: PythonObjectWithCheckedDowncast,
    {
        PythonObjectWithCheckedDowncast::downcast_from(py, self)
    }

    /// Casts the PyObject to a concrete Python object type.
    /// Fails with `PythonObjectDowncastError` if the object is not of the expected type.
    /// This is a wrapper function around `PythonObjectWithCheckedDowncast::downcast_borrow_from()`.
    #[inline]
    pub fn cast_as<'s, 'p, T>(
        &'s self,
        py: Python<'p>,
    ) -> Result<&'s T, PythonObjectDowncastError<'p>>
    where
        T: PythonObjectWithCheckedDowncast,
    {
        PythonObjectWithCheckedDowncast::downcast_borrow_from(py, self)
    }

    /// Extracts some type from the Python object.
    /// This is a wrapper function around `FromPyObject::from_py_object()`.
    #[inline]
    pub fn extract<'a, T>(&'a self, py: Python) -> PyResult<T>
    where
        T: crate::conversion::FromPyObject<'a>,
    {
        crate::conversion::FromPyObject::extract(py, self)
    }

    /// True if this is None in Python.
    #[inline]
    pub fn is_none(&self, _py: Python) -> bool {
        self.as_ptr() == unsafe { ffi::Py_None() }
    }

    pub unsafe fn alloc(py: Python, ty: &PyType, _init_val: ()) -> PyResult<PyObject> {
        let ptr = ffi::PyType_GenericAlloc(ty.as_type_ptr(), 0);
        err::result_from_owned_ptr(py, ptr)
    }

    pub unsafe fn dealloc(_py: Python, obj: *mut ffi::PyObject) {
        // Unfortunately, there is no PyType_GenericFree, so
        // we have to manually un-do the work of PyType_GenericAlloc:
        let ty = ffi::Py_TYPE(obj);
        if ffi::PyType_IS_GC(ty) != 0 {
            ffi::PyObject_GC_Del(obj as *mut libc::c_void);
        } else {
            ffi::PyObject_Free(obj as *mut libc::c_void);
        }
        // For heap types, PyType_GenericAlloc calls INCREF on the type objects,
        // so we need to call DECREF here:
        if ffi::PyType_HasFeature(ty, ffi::Py_TPFLAGS_HEAPTYPE) != 0 {
            ffi::Py_DECREF(ty as *mut ffi::PyObject);
        }
    }
}

/// PyObject implements the `==` operator using reference equality:
/// `obj1 == obj2` in rust is equivalent to `obj1 is obj2` in Python.
impl PartialEq for PyObject {
    #[inline]
    fn eq(&self, o: &PyObject) -> bool {
        self.as_ptr() == o.as_ptr()
    }
}

/// PyObject implements the `==` operator using reference equality:
/// `obj1 == obj2` in rust is equivalent to `obj1 is obj2` in Python.
impl Eq for PyObject {}
// mod string;
/// Represents a Python string.
/// Corresponds to `basestring` in Python 2, and `str` in Python 3.
pub struct PyString(PyObject);

pyobject_newtype!(PyString, PyUnicode_Check, PyUnicode_Type);

/// Represents a Python byte string.
/// Corresponds to `str` in Python 2, and `bytes` in Python 3.
pub struct PyBytes(PyObject);

pyobject_newtype!(PyBytes, PyBytes_Check, PyBytes_Type);

/// Enum of possible Python string representations.
#[derive(Clone, Copy, Debug)]
pub enum PyStringData<'a> {
    Latin1(&'a [u8]),
    Utf8(&'a [u8]),
    Utf16(&'a [u16]),
    Utf32(&'a [u32]),
}

impl<'a> PyStringData<'a> {
    /// Convert the Python string data to a Rust string.
    ///
    /// Returns a borrow into the original string data if possible.
    ///
    /// Data that isn't valid in its encoding will be replaced
    /// with U+FFFD REPLACEMENT CHARACTER.
    pub fn to_string_lossy(self) -> Cow<'a, str> {
        match self {
            PyStringData::Utf8(data) => String::from_utf8_lossy(data),
            PyStringData::Latin1(data) => {
                if data.is_ascii() {
                    Cow::Borrowed(unsafe { str::from_utf8_unchecked(data) })
                } else {
                    Cow::Owned(data.iter().map(|&b| b as char).collect())
                }
            }
            PyStringData::Utf16(data) => Cow::Owned(String::from_utf16_lossy(data)),
            PyStringData::Utf32(data) => Cow::Owned(
                data.iter()
                    .map(|&u| char::from_u32(u).unwrap_or('\u{FFFD}'))
                    .collect(),
            ),
        }
    }
}

impl PyString {
    /// Creates a new Python string object.
    ///
    /// the input string will be
    /// converted to a unicode string.
    /// Use `PyUnicode::new()` to always create a unicode string.
    ///
    /// Panics if out of memory.
    pub fn new(py: Python, s: &str) -> PyString {
        fn new_impl(py: Python, s: &str) -> PyString {
            let ptr = s.as_ptr() as *const c_char;
            let len = s.len() as ffi::Py_ssize_t;
            unsafe {
                err::cast_from_owned_ptr_or_panic(py, ffi::PyUnicode_FromStringAndSize(ptr, len))
            }
        }
        new_impl(py, s)
    }

    /// Gets the python string data in its underlying representation.
    ///
    /// For Python 2 byte strings, this function always returns `PyStringData::Utf8`,
    /// even if the bytes are not valid UTF-8.
    /// For unicode strings, returns the underlying representation used by Python.
    pub fn data(&self, py: Python) -> PyStringData {
        self.data_impl(py)
    }

    fn data_impl(&self, _py: Python) -> PyStringData {
        let ptr = self.as_ptr();
        unsafe {
            let ready = ffi::PyUnicode_READY(ptr);
            if ready < 0 {
                // should fail only on OOM
                ffi::PyErr_Print();
                panic!("PyUnicode_READY failed");
            }
            let size = ffi::PyUnicode_GET_LENGTH(ptr) as usize;
            let data = ffi::PyUnicode_DATA(ptr);
            let kind = ffi::PyUnicode_KIND(ptr);
            match kind {
                ffi::PyUnicode_1BYTE_KIND => {
                    PyStringData::Latin1(std::slice::from_raw_parts(data as *const u8, size))
                }
                ffi::PyUnicode_2BYTE_KIND => {
                    PyStringData::Utf16(std::slice::from_raw_parts(data as *const u16, size))
                }
                ffi::PyUnicode_4BYTE_KIND => {
                    PyStringData::Utf32(std::slice::from_raw_parts(data as *const u32, size))
                }
                _ => panic!("Unknown PyUnicode_KIND"),
            }
        }
    }

    /// Convert the `PyString` into a Rust string.
    ///
    /// On Python 2.7, if the `PyString` refers to a byte string,
    /// it will be decoded using UTF-8.
    ///
    /// Returns a `UnicodeDecodeError` if the input is not valid unicode
    /// (containing unpaired surrogates, or a Python 2.7 byte string that is
    /// not valid UTF-8).
    pub fn to_string(&self, py: Python) -> PyResult<Cow<str>> {
        unsafe {
            // On Python 3, we can use the UTF-8 representation stored
            // inside the Python string.
            // This should produce identical results to
            // `self.data(py).to_string(py)` but avoids
            // re-encoding the string on every to_string call.
            let mut size: ffi::Py_ssize_t = 0;
            let data = ffi::PyUnicode_AsUTF8AndSize(self.as_ptr(), &mut size);
            if data.is_null() {
                Err(PyErr::fetch(py))
            } else {
                let slice = std::slice::from_raw_parts(data as *const u8, size as usize);
                Ok(Cow::Borrowed(std::str::from_utf8_unchecked(slice)))
            }
        }
    }

    /// Convert the `PyString` into a Rust string.
    ///
    /// On Python 2.7, if the `PyString` refers to a byte string,
    /// it will be decoded using UTF-8.
    ///
    /// Unpaired surrogates and (on Python 2.7) invalid UTF-8 sequences are
    /// replaced with U+FFFD REPLACEMENT CHARACTER.
    pub fn to_string_lossy(&self, py: Python) -> Cow<str> {
        self.data(py).to_string_lossy()
    }
}

impl PyBytes {
    /// Creates a new Python byte string object.
    /// The byte string is initialized by copying the data from the `&[u8]`.
    ///
    /// Panics if out of memory.
    pub fn new(py: Python, s: &[u8]) -> PyBytes {
        let ptr = s.as_ptr() as *const c_char;
        let len = s.len() as ffi::Py_ssize_t;
        unsafe { err::cast_from_owned_ptr_or_panic(py, ffi::PyBytes_FromStringAndSize(ptr, len)) }
    }

    /// Gets the Python string data as byte slice.
    pub fn data(&self, _py: Python) -> &[u8] {
        unsafe {
            let buffer = ffi::PyBytes_AsString(self.as_ptr()) as *const u8;
            let length = ffi::PyBytes_Size(self.as_ptr()) as usize;
            std::slice::from_raw_parts(buffer, length)
        }
    }
}

/// Converts Rust `str` to Python object.
///
/// On Python 2.7, this impl will create a byte string if the
/// input string is ASCII-only; and a unicode string otherwise.
/// Use `PyUnicode::new()` to always create a unicode string.
///
/// On Python 3.x, this function always creates unicode `str` objects.
impl ToPyObject for str {
    type ObjectType = PyString;

    #[inline]
    fn to_py_object(&self, py: Python) -> PyString {
        PyString::new(py, self)
    }
}

/// Converts Rust `str` to Python object.
///
/// On Python 2.7, this impl will create a byte string if the
/// input string is ASCII-only; and a unicode string otherwise.
/// Use `PyUnicode::new()` to always create a unicode string.
///
/// On Python 3.x, this function always creates unicode `str` objects.
impl ToPyObject for String {
    type ObjectType = PyString;

    #[inline]
    fn to_py_object(&self, py: Python) -> PyString {
        PyString::new(py, self)
    }
}

/// Allows extracting strings from Python objects.
/// Accepts Python `str` and `unicode` objects.
/// In Python 2.7, `str` is expected to be UTF-8 encoded.
///
/// Returns a `UnicodeDecodeError` if the input is not valid unicode
/// (containing unpaired surrogates, or a Python 2.7 byte string that is
/// not valid UTF-8).
impl<'s> FromPyObject<'s> for Cow<'s, str> {
    fn extract(py: Python, obj: &'s PyObject) -> PyResult<Self> {
        obj.cast_as::<PyString>(py)?.to_string(py)
    }
}

/// Allows extracting strings from Python objects.
/// Accepts Python `str` and `unicode` objects.
/// In Python 2.7, `str` is expected to be UTF-8 encoded.
///
/// Returns a `UnicodeDecodeError` if the input is not valid unicode
/// (containing unpaired surrogates, or a Python 2.7 byte string that is
/// not valid UTF-8).
impl<'s> FromPyObject<'s> for String {
    fn extract(py: Python, obj: &'s PyObject) -> PyResult<Self> {
        obj.extract::<Cow<str>>(py).map(Cow::into_owned)
    }
}
// mod tuple;
/// Represents a Python tuple object.
pub struct PyTuple(PyObject);

pyobject_newtype!(PyTuple, PyTuple_Check, PyTuple_Type);

impl PyTuple {
    /// Construct a new tuple with the given elements.
    pub fn new(py: Python, elements: &[PyObject]) -> PyTuple {
        unsafe {
            let len = elements.len();
            let ptr = ffi::PyTuple_New(len as ffi::Py_ssize_t);
            let t = err::result_cast_from_owned_ptr::<PyTuple>(py, ptr).unwrap();
            for (i, e) in elements.iter().enumerate() {
                ffi::PyTuple_SetItem(ptr, i as ffi::Py_ssize_t, e.steal_ptr(py));
            }
            t
        }
    }

    /// Retrieves the empty tuple.
    pub fn empty(py: Python) -> PyTuple {
        unsafe { err::result_cast_from_owned_ptr::<PyTuple>(py, ffi::PyTuple_New(0)).unwrap() }
    }

    /// Gets the length of the tuple.
    #[inline]
    pub fn len(&self, _py: Python) -> usize {
        unsafe {
            // non-negative Py_ssize_t should always fit into Rust uint
            ffi::PyTuple_GET_SIZE(self.0.as_ptr()) as usize
        }
    }

    /// Gets the item at the specified index.
    ///
    /// Panics if the index is out of range.
    pub fn get_item(&self, py: Python, index: usize) -> PyObject {
        // TODO: reconsider whether we should panic
        // It's quite inconsistent that this method takes `Python` when `len()` does not.
        assert!(index < self.len(py));
        unsafe {
            PyObject::from_borrowed_ptr(
                py,
                ffi::PyTuple_GET_ITEM(self.0.as_ptr(), index as ffi::Py_ssize_t),
            )
        }
    }

}

macro_rules! tuple_conversion ({$length:expr,$(($refN:ident, $n:tt, $T:ident)),+} => {
    /// Converts a Rust tuple to a Python `tuple`.
    impl <$($T: ToPyObject),+> ToPyObject for ($($T,)+) {
        type ObjectType = PyTuple;

        fn to_py_object(&self, py: Python) -> PyTuple {
            PyTuple::new(py, &[
                $(py_coerce_expr!(self.$n.to_py_object(py)).into_object(),)+
            ])
        }
    }
});

tuple_conversion!(1, (ref0, 0, A));
tuple_conversion!(2, (ref0, 0, A), (ref1, 1, B));
tuple_conversion!(3, (ref0, 0, A), (ref1, 1, B), (ref2, 2, C));
tuple_conversion!(4, (ref0, 0, A), (ref1, 1, B), (ref2, 2, C), (ref3, 3, D));
tuple_conversion!(
    5,
    (ref0, 0, A),
    (ref1, 1, B),
    (ref2, 2, C),
    (ref3, 3, D),
    (ref4, 4, E)
);
tuple_conversion!(
    6,
    (ref0, 0, A),
    (ref1, 1, B),
    (ref2, 2, C),
    (ref3, 3, D),
    (ref4, 4, E),
    (ref5, 5, F)
);
tuple_conversion!(
    7,
    (ref0, 0, A),
    (ref1, 1, B),
    (ref2, 2, C),
    (ref3, 3, D),
    (ref4, 4, E),
    (ref5, 5, F),
    (ref6, 6, G)
);
tuple_conversion!(
    8,
    (ref0, 0, A),
    (ref1, 1, B),
    (ref2, 2, C),
    (ref3, 3, D),
    (ref4, 4, E),
    (ref5, 5, F),
    (ref6, 6, G),
    (ref7, 7, H)
);
tuple_conversion!(
    9,
    (ref0, 0, A),
    (ref1, 1, B),
    (ref2, 2, C),
    (ref3, 3, D),
    (ref4, 4, E),
    (ref5, 5, F),
    (ref6, 6, G),
    (ref7, 7, H),
    (ref8, 8, I)
);

// Empty tuple:

/// An empty struct that represents the empty argument list.
/// Corresponds to the empty tuple `()` in Python.
///
/// # Example
/// ```
/// let gil_guard = cpython::Python::acquire_gil();
/// let py = gil_guard.python();
/// let os = py.import("os").unwrap();
/// let pid = os.call(py, "getpid", cpython::NoArgs, None).unwrap();
/// ```
#[derive(Copy, Clone, Debug)]
pub struct NoArgs;

/// Converts `NoArgs` to an empty Python tuple.
impl ToPyObject for NoArgs {
    type ObjectType = PyTuple;

    fn to_py_object(&self, py: Python) -> PyTuple {
        PyTuple::empty(py)
    }
}
// mod typeobject;
/// Represents a reference to a Python type object.
pub struct PyType(PyObject);

pyobject_newtype!(PyType, PyType_Check, PyType_Type);

impl PyType {
    /// Retrieves the underlying FFI pointer associated with this Python object.
    #[inline]
    pub fn as_type_ptr(&self) -> *mut ffi::PyTypeObject {
        self.0.as_ptr() as *mut ffi::PyTypeObject
    }

    /// Retrieves the PyType instance for the given FFI pointer.
    /// This increments the reference count on the type object.
    /// Undefined behavior if the pointer is NULL or invalid.
    #[inline]
    pub unsafe fn from_type_ptr(py: Python, p: *mut ffi::PyTypeObject) -> PyType {
        PyObject::from_borrowed_ptr(py, p as *mut ffi::PyObject).unchecked_cast_into::<PyType>()
    }

    /// Gets the name of the PyType.
    pub fn name<'a>(&'a self, _py: Python<'a>) -> Cow<'a, str> {
        unsafe { CStr::from_ptr((*self.as_type_ptr()).tp_name).to_string_lossy() }
    }

    /// Return true if `obj` is an instance of `self`.
    #[inline]
    pub fn is_instance(&self, _: Python, obj: &PyObject) -> bool {
        unsafe { ffi::PyObject_TypeCheck(obj.as_ptr(), self.as_type_ptr()) != 0 }
    }

    /// Calls the type object, thus creating a new instance.
    /// This is equivalent to the Python expression: `self(*args, **kwargs)`
    #[inline]
    pub fn call<A>(&self, py: Python, args: A, kwargs: Option<&PyDict>) -> PyResult<PyObject>
    where
        A: ToPyObject<ObjectType = PyTuple>,
    {
        args.with_borrowed_ptr(py, |args| unsafe {
            err::result_from_owned_ptr(
                py,
                ffi::PyObject_Call(self.0.as_ptr(), args, kwargs.as_ptr()),
            )
        })
    }
}

impl PartialEq for PyType {
    #[inline]
    fn eq(&self, o: &PyType) -> bool {
        self.as_type_ptr() == o.as_type_ptr()
    }
}
impl Eq for PyType {}
