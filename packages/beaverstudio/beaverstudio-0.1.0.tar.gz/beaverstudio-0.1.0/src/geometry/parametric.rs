//! A 2D parametric curve.

use image::{
    Rgb,
    RgbImage,
};

use pyo3::{
    prelude::*,
    types::PyFunction,
};

use crate::{
    add_pixel,
    Animate,
    Animation,
    Artist,
    Bresenham,
    Brush,
    STEP,
    Vector,
};

#[pyclass]
#[derive(Clone)]
/// A 2D parametric curve.
pub struct Parametric {
    /// Points along this parametric curve, as well as their time values.
    pub points: Vec<(Vector, f64)>,

    /// Color of curve.
    pub color: Rgb<u8>,

    /// Curve brush.
    pub brush: Brush,
}

#[pymethods]
impl Parametric {
    #[new]
    /// Construct a new parametric function.
    pub fn new(x_func: Py<PyFunction>, y_func: Py<PyFunction>, times: (f64, f64), origin: Vector, color: [u8; 3], thickness: i32) -> Self {
        // Build collection of points to interpolate between
        let mut t = times.0;
        let mut points = Vec::new();

        while t <= times.1 {
            // Step along the curve
            t += STEP;

            // Scale to between 0 and 1
            let t_fixed = (t - times.0) / (times.1 - times.0);

            // Get X and Y position
            let pos = Python::with_gil(|py| {
                // TODO this is sloppy
                let x: f64 = x_func.call(py, (t,), None).unwrap().extract(py).unwrap();
                let y: f64 = y_func.call(py, (t,), None).unwrap().extract(py).unwrap();

                Vector::new(x, y)
            });

            // Save this point
            points.push((origin + pos, t_fixed));
        }

        Self {
            points,
            color: Rgb (color),
            brush: Brush::new(thickness),
        }
    }

    #[getter]
    /// Construct a (static) animation from this shape.
    pub fn get_display(&self) -> Animation {
        Animate::animate(self)
    }

    #[getter]
    /// Construct a tracing animation from this shape.
    pub fn get_trace(&self) -> Animation {
        TraceParametric::new(self.clone(), false).animate()
    }

    #[getter]
    /// Construct an untracing animation from this shape.
    pub fn get_untrace(&self) -> Animation {
        TraceParametric::new(self.clone(), true).animate()
    }
}

impl Artist for Parametric {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Interpolation (Bresenham's line algorithm)
        for i in 0..(self.points.len() - 1) {
            // Two points to draw between
            let this_point = location + self.points[i].0;
            let next_point = location + self.points[i + 1].0;

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

impl Animate for Parametric {
    fn play(&self, _: f64) -> Box<dyn Artist> {
        Box::new(self.clone())
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

#[derive(Clone)]
/// An animation that traces a parametric curve, drawing it over time.
pub struct TraceParametric {
    /// Curve to be traced.
    curve: Parametric,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl TraceParametric {
    /// Construct a new tracing animation.
    pub fn new(curve: Parametric, untrace: bool) -> Self {
        Self {
            curve,
            untrace,
        }
    }
}

impl Animate for TraceParametric {
    fn play(&self, progress: f64) -> Box<dyn Artist> {
        Box::new(TracedParametric::new(self.curve.clone(), progress, self.untrace))
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

/// A parametric that is partially traced.
pub struct TracedParametric {
    /// Curve to be traced.
    curve: Parametric,

    /// Amount of progress this tracing has made.
    progress: f64,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl TracedParametric {
    /// Construct a new curve to be traced.
    pub fn new(curve: Parametric, progress: f64, untrace: bool) -> Self {
        Self {
            curve,
            progress,
            untrace,
        }
    }
}

impl Artist for TracedParametric {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Interpolation (Bresenham's line algorithm)
        for i in 0..(self.curve.points.len() - 1) {
            // Two points to draw between
            let this_point = location + self.curve.points[i].0;
            let next_point = location + self.curve.points[i + 1].0;

            // Convert points to integers
            let (x0, y0) = this_point.to_pixels(image.width(), image.height());
            let (x1, y1) = next_point.to_pixels(image.width(), image.height());

            // Construct Bresenham line
            let line = Bresenham::new(x0, y0, x1, y1).points;

            // Are we past the bounds?
            if self.untrace {
                // Before the progress point, skip
                if self.curve.points[i].1 < self.progress {
                    continue;
                }
            } else {
                // Past the progress point, stop drawing
                if self.curve.points[i + 1].1 > self.progress {
                    break;
                }
            }

            // Draw points
            for (x, y) in line {
                for (i, j, strength) in &self.curve.brush.points {
                    add_pixel(image, (x as i32 + i) as u32, (y as i32 + j) as u32, self.curve.color, *strength);
                }
            }
        }
    }
}