//! A 2-dimensional point on an image.

use std::ops::{
    Add,
    Sub,
    Mul,
    Neg,
};

use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Copy, Debug)]
/// A 2-dimensional vector on an image.
/// 
/// The origin of an image is in the center, and
/// the units of this vector are pixels.
pub struct Vector {
    pub x: f64,
    pub y: f64,
}

#[pymethods]
impl Vector {
    #[new]
    /// Construct a new vector.
    pub fn new(x: f64, y: f64) -> Self {
        Self {
            x,
            y,
        }
    }

    #[staticmethod]
    /// Construct the zero vector.
    pub fn zero() -> Self {
        Self {
            x: 0.0,
            y: 0.0,
        }
    }
}

impl Vector {
    /// Convert this vector into pixel values.
    pub fn to_pixels(&self, width: u32, height: u32) -> (u32, u32) {
        let x = (self.x + (width as f64)/2.0).round() as u32;
        let y = ((height as f64)/2.0 - self.y).round() as u32;
        
        // TODO don't even draw the pixel if it's off-screen
        (x.clamp(0, width-1), y.clamp(0, height-1))
    }
}

impl Add<Vector> for Vector {
    type Output = Vector;

    fn add(self, other: Vector) -> Self::Output {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Sub<Vector> for Vector {
    type Output = Vector;

    fn sub(self, other: Vector) -> Self::Output {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl Mul<f64> for Vector {
    type Output = Vector;

    fn mul(self, other: f64) -> Self::Output {
        Self {
            x: self.x * other,
            y: self.y * other,
        }
    }
}

impl Mul<u32> for Vector {
    type Output = Vector;

    fn mul(self, other: u32) -> Self::Output {
        Self {
            x: self.x * (other as f64),
            y: self.y * (other as f64),
        }
    }
}

impl Neg for Vector {
    type Output = Vector;

    fn neg(self) -> Self::Output {
        Self {
            x: -self.x,
            y: -self.y,
        }
    }
}