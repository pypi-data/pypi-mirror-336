//! A video animation.

use pyo3::prelude::*;

use crate::Artist;

/// A video animation.
/// 
/// Video animations are controlled by their `progress` variable.  Given a progress value,
/// they return an image artist that is capable of modifying a provided frame.
pub trait Animate: Send + Sync {
    /// Creates an `Artist` trait object, given a progress value.
    fn play(&self, progress: f64) -> Box<dyn Artist>;

    /// Clones this trait object.
    fn clone_box(&self) -> Box<dyn Animate>;

    /// Converts this trait object into a Python-compatible `Animation`.
    fn animate(&self) -> Animation {
        Animation (self.clone_box())
    }
}

#[pyclass]
/// A Python-compatible animation type.
pub struct Animation (pub Box<dyn Animate>);

/// We derive `Clone` manually for this trait because
/// Rust cannot figure out how to clone it automatically,
/// and we use our `Animate::clone_box` method to do it
/// manually.
impl Clone for Animation {
    fn clone(&self) -> Self {
        Self (self.0.clone_box())
    }
}