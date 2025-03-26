//! A circle.

use image::RgbImage;

use pyo3::prelude::*;

use crate::{
    Artist,
    Bezier,
    Shape,
    Vector,
};

/// Magic number for a circle, relating the positions of Bezier control points.
pub const MAGIC: f64 = 0.552284749831;

#[pyclass]
#[derive(Clone)]
/// A circle.
pub struct Circle (Shape);

#[pymethods]
impl Circle {
    #[new]
    /// Construct a new circle.
    pub fn new(center: Vector, radius: f64, color: [u8; 3], thickness: i32) -> Self {
        // Magic steps
        let xstep = Vector::new(radius*MAGIC, 0.0);
        let ystep = Vector::new(0.0, radius*MAGIC);

        // Radius steps
        let xrad = Vector::new(radius, 0.0);
        let yrad = Vector::new(0.0, radius);

        Self (Shape::new(vec![
            Bezier::new(vec![xrad, xrad + ystep, yrad + xstep, yrad], Vector::zero(), color, thickness),
            Bezier::new(vec![yrad, yrad - xstep, -xrad + ystep, -xrad], Vector::zero(), color, thickness),
            Bezier::new(vec![-xrad, -xrad - ystep, -yrad - xstep, -yrad], Vector::zero(), color, thickness),
            Bezier::new(vec![-yrad, -yrad + xstep, xrad - ystep, xrad], Vector::zero(), color, thickness),
        ], center))
    }

    #[getter]
    /// Extract the chain of Bezier curves.
    pub fn get_shape(&self) -> Shape {
        self.0.clone()
    }
}

impl Artist for Circle {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        self.0.draw(location, image);
    }
}