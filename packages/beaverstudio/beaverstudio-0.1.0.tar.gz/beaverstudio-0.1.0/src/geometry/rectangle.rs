//! A rectangle.

use image::RgbImage;

use pyo3::prelude::*;

use crate::{
    Artist,
    Bezier,
    Shape,
    Vector,
};

#[pyclass]
#[pyo3(name = "Rect")]
#[derive(Clone)]
/// A rectangle.
pub struct Rectangle (Shape);

#[pymethods]
impl Rectangle {
    #[new]
    /// Construct a new rectangle.
    pub fn new(center: Vector, width: f64, height: f64, color: [u8; 3], thickness: i32) -> Self {
        // Half-sides
        let xside = Vector::new(0.5*width, 0.0);
        let yside = Vector::new(0.0, 0.5*height);

        Self (Shape::new(vec![
            Bezier::new(vec![xside + yside, -xside + yside], Vector::zero(), color, thickness),
            Bezier::new(vec![-xside + yside, -xside - yside], Vector::zero(), color, thickness),
            Bezier::new(vec![-xside - yside, xside - yside], Vector::zero(), color, thickness),
            Bezier::new(vec![xside - yside, xside + yside], Vector::zero(), color, thickness),
        ], center))
    }

    #[getter]
    /// Extract the chain of Bezier curves.
    pub fn get_shape(&self) -> Shape {
        self.0.clone()
    }
}

impl Artist for Rectangle {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        self.0.draw(location, image);
    }
}