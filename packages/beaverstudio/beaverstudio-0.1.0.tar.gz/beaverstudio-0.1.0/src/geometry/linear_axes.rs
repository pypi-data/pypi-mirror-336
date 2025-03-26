//! Coordinate axes.

use crate::{
    Animate,
    Animation,
    Artist,
    Bezier,
    TracedShape,
    Vector,
};

use image::RgbImage;

use pyo3::prelude::*;

/// Color for major gridlines.
const MAJOR_COLOR: [u8; 3] = [255, 255, 255];

/// Color for minor gridlines.
const MINOR_COLOR: [u8; 3] = [160, 160, 160];

/// Thickness for major gridlines.
const MAJOR_THICKNESS: i32 = 4;

/// Thickness for minor gridlines.
const MINOR_THICKNESS: i32 = 2;

/// Progress multiplier for each successive minor gridline (smaller is denser).
const MULT: f64 = 0.25;

#[pyclass]
#[derive(Clone)]
/// Linear-linear coordinate axes.
pub struct LinearAxes {
    /// Bezier curves describing the X gridlines.
    pub x_minors: Vec<Bezier>,

    /// Bezier curves describing the Y gridlines.
    pub y_minors: Vec<Bezier>,

    /// X major gridline.
    pub x_major: Bezier,

    /// Y major gridline.
    pub y_major: Bezier,
}

#[pymethods]
impl LinearAxes {
    #[new]
    /// Create a set of coordinate axes with a specified origin, line spacing, and line count.
    pub fn new(origin: Vector, spacing: f64, x_count: (usize, usize), y_count: (usize, usize)) -> Self {
        // Minimum/maximum X and Y values
        let mut x_min = origin.x;
        let mut x_max = origin.x;
        let mut y_min = origin.y;
        let mut y_max = origin.y;

        // Current X value
        let mut x = origin.x;

        // X values to draw minor gridlines at
        let mut x_vals = Vec::new();

        // Draw positive X lines
        for _ in 0..x_count.1 {
            x += spacing;
            x_vals.push(x);
            x_max = x_max.max(x);
        }

        // Draw negative X lines
        x = origin.x;
        for _ in 0..x_count.0 {
            x -= spacing;
            x_vals.push(x);
            x_min = x_min.min(x);
        }

        // Sort X values away from origin
        x_vals.sort_by(|a, b| (a - origin.x).abs().partial_cmp(&(b - origin.x).abs()).unwrap());

        // Current Y value
        let mut y = origin.y;

        // Y values to draw minor gridlines at
        let mut y_vals = Vec::new();

        // Draw positive Y lines
        for _ in 0..y_count.1 {
            y += spacing;
            y_vals.push(y);
            y_max = y_max.max(y);
        }

        // Draw negative Y lines
        y = origin.y;
        for _ in 0..y_count.0 {
            y -= spacing;
            y_vals.push(y);
            y_min = y_min.min(y);
        }

        // Sort Y values away from origin
        y_vals.sort_by(|a, b| (a - origin.y).abs().partial_cmp(&(b - origin.y).abs()).unwrap());

        // Resultant Bezier curves
        let mut x_minors = Vec::new();
        let mut y_minors = Vec::new();

        // Construct Bezier curves for each X minor gridline
        for x_val in x_vals {
            let gridline = Bezier::new(
                vec![Vector::new(x_val, y_min), Vector::new(x_val, y_max)],
                Vector::zero(),
                MINOR_COLOR,
                MINOR_THICKNESS,
            );

            x_minors.push(gridline);
        }

        // Construct Bezier curves for each Y minor gridline
        for y_val in y_vals {
            let gridline = Bezier::new(
                vec![Vector::new(x_min, y_val), Vector::new(x_max, y_val)],
                Vector::zero(),
                MINOR_COLOR,
                MINOR_THICKNESS,
            );

            y_minors.push(gridline);
        }

        // Construct major gridlines
        let x_major = Bezier::new(
            vec![Vector::new(origin.x, y_min), Vector::new(origin.x, y_max)],
            Vector::zero(),
            MAJOR_COLOR,
            MAJOR_THICKNESS,
        );
        let y_major = Bezier::new(
            vec![Vector::new(x_min, origin.y), Vector::new(x_max, origin.y)],
            Vector::zero(),
            MAJOR_COLOR,
            MAJOR_THICKNESS,
        );

        Self {
            x_minors,
            y_minors,
            x_major,
            y_major,
        }
    }

    #[getter]
    /// Display these axes on screen.
    pub fn get_display(&self) -> Animation {
        Animate::animate(self)
    }

    #[getter]
    /// Construct a tracing animation.
    pub fn get_trace(&self) -> Animation {
        TraceLinearAxes::new(self.clone(), false).animate()
    }

    #[getter]
    /// Construct an untracing animation.
    pub fn get_untrace(&self) -> Animation {
        TraceLinearAxes::new(self.clone(), true).animate()
    }
}

impl Artist for LinearAxes {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Render X minor gridlines
        for curve in &self.x_minors {
            curve.draw(location, image);
        }

        // Render Y minor gridlines
        for curve in &self.y_minors {
            curve.draw(location, image);
        }

        // Render major gridlines
        self.x_major.draw(location, image);
        self.y_major.draw(location, image);
    }
}

impl Animate for LinearAxes {
    fn play(&self, _: f64) -> Box<dyn Artist> {
        Box::new(self.clone())
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

#[derive(Clone)]
/// An animation that traces linear axes over time.
pub struct TraceLinearAxes {
    /// Linear axes to trace.
    linear_axes: LinearAxes,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl TraceLinearAxes {
    /// Construct a new animation for linear axes.
    pub fn new(linear_axes: LinearAxes, untrace: bool) -> Self {
        Self {
            linear_axes,
            untrace,
        }
    }
}

impl Animate for TraceLinearAxes {
    fn play(&self, progress: f64) -> Box<dyn Artist> {
        Box::new(TracedLinearAxes::new(self.linear_axes.clone(), progress, self.untrace))
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

/// A partially traced set of linear axes.
pub struct TracedLinearAxes {
    /// Linear axes to trace.
    linear_axes: LinearAxes,

    /// Amount of progress we've made.
    progress: f64,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl TracedLinearAxes {
    /// Construct a new partially traced set of linear axes.
    pub fn new(linear_axes: LinearAxes, progress: f64, untrace: bool) -> Self {
        Self {
            linear_axes,
            progress,
            untrace,
        }
    }
}

impl Artist for TracedLinearAxes {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // X minor gridlines
        for (i, x_minor) in self.linear_axes.x_minors.iter().enumerate() {
            let x_minor = TracedShape::new(
                x_minor.get_shape(),
                self.progress.powf(i as f64 * MULT + (1.0 + MULT)),
                self.untrace,
            );
            x_minor.draw(location, image);
        }

        // Y minor gridlines
        for (j, y_minor) in self.linear_axes.y_minors.iter().enumerate() {
            let y_minor = TracedShape::new(
                y_minor.get_shape(),
                self.progress.powf(j as f64 * MULT + (1.0 + MULT)),
                self.untrace,
            );
            y_minor.draw(location, image);
        }

        // X major gridline
        let x_major = TracedShape::new(
            self.linear_axes.x_major.get_shape(),
            self.progress,
            self.untrace,
        );
        x_major.draw(location, image);

        // Y major gridline
        let y_major = TracedShape::new(
            self.linear_axes.y_major.get_shape(),
            self.progress,
            self.untrace,
        );
        y_major.draw(location, image);
    }
}