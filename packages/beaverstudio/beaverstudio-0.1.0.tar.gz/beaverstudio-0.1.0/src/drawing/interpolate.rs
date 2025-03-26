//! Interpolation between two Bezier curves.

use image::{
    Rgb,
    RgbImage,
};

use crate::{
    add_pixel,
    Animate,
    Artist,
    Bresenham,
    Brush,
    Shape,
    STEP,
    Vector,
};

#[derive(Clone)]
/// An interpolation animation, where one shape smoothly becomes another.
pub struct Interpolate {
    one: Shape,
    two: Shape,
}

impl Interpolate {
    /// Construct a new interpolation.
    pub fn new(one: Shape, two: Shape) -> Self {
        Self {
            one,
            two,
        }
    }
}

impl Animate for Interpolate {
    fn play(&self, progress: f64) -> Box<dyn Artist> {
        Box::new(InterpolatedCurve::new(self.one.clone(), self.two.clone(), progress))
    }

    fn clone_box(&self) -> Box<dyn Animate> {
        Box::new(self.clone())
    }
}

/// A linear interpolation between two shapes.
pub struct InterpolatedCurve {
    one: Shape,
    two: Shape,
    progress: f64,
}

impl InterpolatedCurve {
    /// Construct a new interpolated curve.
    pub fn new(one: Shape, two: Shape, progress: f64) -> Self {
        Self {
            one,
            two,
            progress,
        }
    }
}

impl Artist for InterpolatedCurve {
    fn draw(&self, location: Vector, image: &mut RgbImage) {
        // Build collection of points to interpolate between
        let mut t = 0.0f64;
        let mut points = Vec::new();

        while t <= 1.0 {
            // Fix floating-point errors
            let t_fixed = t.clamp(0.0, 1.0 - STEP);

            // Calculate offset from location
            let trace1 = self.one.trace(t_fixed) + location;
            let trace2 = self.two.trace(t_fixed) + location;

            // Compute weighted average
            let trace = trace1 * (1.0 - self.progress) + trace2 * self.progress;

            // Save this point
            points.push(location + trace);

            // Step along the curve
            t += STEP;
        }

        // Interpolate colors
        // TODO this is a sloppy interpolation, can it be better?
        let (r, g, b): (f64, f64, f64) = (
            (self.one.color.0[0] as f64) * (1.0 - self.progress) + (self.two.color.0[0] as f64) * self.progress,
            (self.one.color.0[1] as f64) * (1.0 - self.progress) + (self.two.color.0[1] as f64) * self.progress,
            (self.one.color.0[2] as f64) * (1.0 - self.progress) + (self.two.color.0[2] as f64) * self.progress,
        );
        let color = Rgb ([r as u8, g as u8, b as u8]);

        // Thickness of this interpolation
        let thickness = (self.one.thickness as f64) * (1.0 - self.progress) + (self.two.thickness as f64) * self.progress;

        // Brush to draw with
        let brush = Brush::new(thickness.round() as i32);

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
                    add_pixel(image, (x as i32 + i) as u32, (y as i32 + j) as u32, color, *strength);
                }
            }
        }
    }
}