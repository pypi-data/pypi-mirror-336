//! Main library for the Beaver Studio.

#![deny(warnings)]
#![deny(missing_docs)]

mod drawing;
mod geometry;
mod video;

use pyo3::prelude::*;

use image::{
    Rgb,
    RgbImage,
};

use drawing::{
    Animate,
    Animation,
    Artist,
    Bresenham,
    Brush,
    Interpolate,
    Trace,
    TracedShape,
};
use geometry::{
    Bezier,
    Circle,
    LinearAxes,
    Parametric,
    Polygon,
    Rectangle,
    Shape,
    Vector,
};
use video::Video;

/// Interpolation step size.
pub const STEP: f64 = 1E-3;

/// Add a pixel to the image with a given strength.
pub fn add_pixel(image: &mut RgbImage, x: u32, y: u32, color: Rgb<u8>, strength: f64) {
    // Don't draw outside the image
    if x >= image.width() || y >= image.height() {
        return;
    }

    // Current pixel
    let current_pixel = image.get_pixel(x, y);

    // Interpolated pixel
    let new_pixel = Rgb ([
        ((color[0] as f64) * strength) as u8 + ((current_pixel[0] as f64) * (1.0 - strength)) as u8,
        ((color[1] as f64) * strength) as u8 + ((current_pixel[1] as f64) * (1.0 - strength)) as u8,
        ((color[2] as f64) * strength) as u8 + ((current_pixel[2] as f64) * (1.0 - strength)) as u8,
    ]);

    image.put_pixel(x, y, new_pixel);
}

/// Python interface for Beaver Studio.
#[pymodule]
fn beaverstudio(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add classes
    m.add_class::<Bezier>()?;
    m.add_class::<Circle>()?;
    m.add_class::<LinearAxes>()?;
    m.add_class::<Parametric>()?;
    m.add_class::<Polygon>()?;
    m.add_class::<Rectangle>()?;
    m.add_class::<Shape>()?;
    m.add_class::<Vector>()?;
    m.add_class::<Video>()?;
    
    Ok(())
}