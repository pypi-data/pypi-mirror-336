//! Trace a shape.

use image::RgbImage;

use crate::{
    add_pixel,
    Artist,
    Animate,
    Bresenham,
    Brush,
    Shape,
    STEP,
    Vector,
};

#[derive(Clone)]
/// An animation that traces the outline of a shape, drawing it over time.
pub struct Trace {
    /// Shape to be traced.
    shape: Shape,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl Trace {
    /// Construct a new tracing animation.
    pub fn new(shape: Shape, untrace: bool) -> Self {
        Self {
            shape,
            untrace,
        }
    }
}

impl Animate for Trace {
    fn play(&self, progress: f64) -> Box<dyn Artist> {
        Box::new(TracedShape::new(self.shape.clone(), progress, self.untrace))
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

/// A shape that is partially traced.
pub struct TracedShape {
    /// Shape to be traced.
    shape: Shape,

    /// Amount of progress this tracing has made.
    progress: f64,

    /// Are we tracing or untracing?
    untrace: bool,
}

impl TracedShape {
    /// Construct a new shape to be traced.
    pub fn new(shape: Shape, progress: f64, untrace: bool) -> Self {
        Self {
            shape,
            progress,
            untrace,
        }
    }
}

impl Artist for TracedShape {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Amount of progress per curve
        let progress_per_curve = 1.0 / (self.shape.curves.len() as f64);

        for (i, curve) in self.shape.curves.iter().enumerate() {
            // How much progress along this curve?
            let progress = ((self.progress - i as f64 * progress_per_curve) / progress_per_curve).clamp(0.0, 1.0);

            // Build collection of points to interpolate between
            let mut t = if self.untrace { progress } else { 0.0 };
            let mut points = Vec::new();

            // Condition to finish tracing on this frame
            let condition = |t: f64| if self.untrace { t < 1.0 } else { t <= progress };

            while condition(t) {
                // Step along the curve
                t += STEP;
                
                // Fix floating-point errors
                let t_fixed = t.clamp(0.0, 1.0 - STEP);

                // Save this point
                points.push(location + self.shape.origin + curve.trace(t_fixed));
            }

            // Brush to draw with
            let brush = Brush::new(self.shape.thickness);

            // If there are no points, don't draw anything
            if points.len() == 0 {
                continue;
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
                    for (i, j, strength) in &brush.points {
                        add_pixel(image, (x as i32 + i) as u32, (y as i32 + j) as u32, self.shape.color, *strength);
                    }
                }
            }
        }
    }
}