//! Bezier curve implementation.

use image::{
    Rgb,
    RgbImage,
};

use pyo3::prelude::*;

use crate::{
    add_pixel,
    Animate,
    Animation,
    Artist,
    Bresenham,
    Brush,
    Shape,
    STEP,
    Trace,
    Vector,
};

/// Compute the binomial coefficient C(n,k).
fn binom(mut n: u32, k: u32) -> u32 {
    let mut output = 1;

    for _ in 0..k {
        output *= n;
        n -= 1;
    }

    for i in 2..=k {
        output /= i;
    }

    output
}

#[pyclass]
#[derive(Clone)]
/// A Bezier curve of arbitrary order, constructed with a series of control points.
pub struct Bezier {
    /// Origin.
    origin: Vector,

    /// Color (RGB).
    pub color: Rgb<u8>,

    /// Control points, relative to the origin.
    points: Vec<Vector>,

    /// Curve thickness.
    pub thickness: i32,

    /// Curve brush.
    brush: Brush,
}

#[pymethods]
impl Bezier {
    #[new]
    /// Construct a new Bezier curve, given control points and an origin.
    /// 
    /// Note that the control points are *relative* to the given origin.
    pub fn new(points: Vec<Vector>, origin: Vector, color: [u8; 3], thickness: i32) -> Self {
        Self {
            points,
            origin,
            color: Rgb (color),
            thickness,
            brush: Brush::new(thickness),
        }
    }

    #[getter]
    /// Turn this Bezier curve into a shape.
    pub fn get_shape(&self) -> Shape {
        Shape::new(vec![self.clone()], Vector::zero())
    }

    #[getter]
    /// Construct a (static) animation from this curve.
    pub fn get_display(&self) -> Animation {
        Animate::animate(self)
    }

    #[getter]
    /// Construct a tracing animation from this curve.
    pub fn get_trace(&self) -> Animation {
        Trace::new(self.get_shape(), false).animate()
    }

    #[getter]
    /// Construct an untracing animation from this curve.
    pub fn get_untrace(&self) -> Animation {
        Trace::new(self.get_shape(), true).animate()
    }
}

impl Bezier {
    /// Trace this Bezier curve.
    pub fn trace(&self, t: f64) -> Vector {
        // Zero vector
        let mut result = Vector::zero();

        // No curve if no points :(
        if self.points.len() == 0 {
            return result;
        }

        // Order of this Bezier curve
        let order = self.points.len() - 1;

        // Sum contributions from each control point
        for k in 0..self.points.len() {
            // Binomial coefficient
            let coeff = binom(order as u32, k as u32);

            // Add contribution
            result = result + (self.points[k] + self.origin) * coeff * (1.0 - t).powi((order - k) as i32) * t.powi(k as i32);
        }

        result
    }
}

impl Artist for Bezier {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Build collection of points to interpolate between
        let mut t = 0.0;
        let mut points = Vec::new();

        while t <= 1.0 {
            // Step along the curve
            t += STEP;

            // Fix floating-point errors
            let t_fixed = t.clamp(0.0, 1.0 - STEP);

            // Save this point
            points.push(location + self.trace(t_fixed));
        }

        // Interpolation (Bresenham's line algorithm)
        for i in 0..(points.len() - 1) {
            // Two points to draw between
            let this_point = points[i];
            let next_point = points[i + 1];

            // Convert points to integers
            let (x0, y0) = this_point.to_pixels(image.width(), image.height());
            let (x1, y1) = next_point.to_pixels(image.width(), image.height());

            // Construct Bresenham line
            let line = Bresenham::new(x0, y0, x1, y1).points;

            // Draw first point
            for (x, y) in line {
                for (i, j, strength) in &self.brush.points {
                    add_pixel(image, (x as i32 + i) as u32, (y as i32 + j) as u32, self.color, *strength);
                }
            }
        }
    }
}

impl Animate for Bezier {
    fn play(&self, _: f64) -> Box<dyn Artist> {
        Box::new(self.clone())
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}