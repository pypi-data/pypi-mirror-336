// Copyright (c) 2016 Daniel Grunwald
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

#![cfg_attr(feature="nightly", allow(incomplete_features))]
#![cfg_attr(feature="nightly", feature(
    specialization, // for impl FromPyObject<'s> for Vec<...> (#31844)
))]
#![allow(
    clippy::missing_safety_doc,
    clippy::manual_strip,
    clippy::match_like_matches_macro
)]

pub(crate) use pyo3_ffi as ffi;

pub use ffi::Py_ssize_t;

pub use crate::conversion::{FromPyObject, ToPyObject};
pub use crate::err::{PyErr, PyResult};
pub use crate::objectprotocol::ObjectProtocol;
pub use crate::objects::*;
pub use crate::python::{
    PyClone, PyDrop, Python, PythonObject, PythonObjectDowncastError,
    PythonObjectWithCheckedDowncast, PythonObjectWithTypeObject,
};

#[allow(non_camel_case_types)]
pub type Py_hash_t = ffi::Py_hash_t;

// AST coercion macros (https://danielkeep.github.io/tlborm/book/blk-ast-coercion.html)
#[macro_export]
#[doc(hidden)]
macro_rules! py_coerce_expr {
    ($s:expr) => {
        $s
    };
}
#[macro_export]
#[doc(hidden)]
macro_rules! py_coerce_item {
    ($s:item) => {
        $s
    };
}

#[macro_export]
#[doc(hidden)]
macro_rules! py_replace_expr {
    ($_t:tt $sub:expr) => {
        $sub
    };
}

#[macro_export]
#[doc(hidden)]
macro_rules! py_impl_to_py_object_for_python_object {
    ($T: ty) => {
        /// Identity conversion: allows using existing `PyObject` instances where
        /// `T: ToPyObject` is expected.
        impl $crate::ToPyObject for $T {
            type ObjectType = $T;

            #[inline]
            fn to_py_object(&self, py: $crate::Python) -> $T {
                $crate::PyClone::clone_ref(self, py)
            }

            #[inline]
            fn with_borrowed_ptr<F, R>(&self, _py: $crate::Python, f: F) -> R
            where
                F: FnOnce(*mut ffi::PyObject) -> R,
            {
                f($crate::PythonObject::as_object(self).as_ptr())
            }
        }
    };
}

#[macro_export]
#[doc(hidden)]
macro_rules! py_impl_from_py_object_for_python_object {
    ($T:ty) => {
        impl<'s> $crate::FromPyObject<'s> for $T {
            #[inline]
            fn extract(py: $crate::Python, obj: &'s $crate::PyObject) -> $crate::PyResult<$T> {
                use $crate::PyClone;
                Ok(obj.clone_ref(py).cast_into::<$T>(py)?)
            }
        }

        impl<'s> $crate::FromPyObject<'s> for &'s $T {
            #[inline]
            fn extract(py: $crate::Python, obj: &'s $crate::PyObject) -> $crate::PyResult<&'s $T> {
                Ok(obj.cast_as::<$T>(py)?)
            }
        }
    };
}

mod conversion;
mod err;
mod objectprotocol;
mod objects;
mod python;
mod pythonrun;

// Strip 'r#' prefix from stringified raw identifiers.
#[macro_export]
#[doc(hidden)]
macro_rules! strip_raw {
    ($s:expr) => {{
        let s = $s;
        if s.starts_with("r#") {
            &s[2..]
        } else {
            s
        }
    }};
}
