//! An arbitrary polygon.

use image::RgbImage;

use pyo3::prelude::*;

use crate::{
    Artist,
    Bezier,
    Shape,
    Vector,
};

#[pyclass]
#[derive(Clone)]
/// A polygon.
pub struct Polygon (Shape);

#[pymethods]
impl Polygon {
    #[new]
    /// Construct a new polygon.
    pub fn new(points: Vec<Vector>, center: Vector, color: [u8; 3], thickness: i32) -> Self {
        // Bezier curves
        let mut curves = Vec::new();

        for i in 0..(points.len() - 1) {
            // Construct one side
            let curve = Bezier::new(
                vec![points[i], points[i + 1]],
                Vector::zero(),
                color,
                thickness,
            );
            curves.push(curve);
        }

        // Close polygon
        let curve = Bezier::new(
            vec![points[points.len() - 1], points[0]],
            Vector::zero(),
            color,
            thickness,
        );
        curves.push(curve);

        Self (Shape::new(curves, center))
    }

    #[getter]
    /// Extract the chain of Bezier curves.
    pub fn get_shape(&self) -> Shape {
        self.0.clone()
    }
}

impl Artist for Polygon {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        self.0.draw(location, image);
    }
}