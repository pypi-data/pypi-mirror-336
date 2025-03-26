//! An image artist.

use image::RgbImage;

use crate::Vector;

/// An image artist.
/// 
/// Image artists create visuals on a given frame.
pub trait Artist {
    /// Draw on the given frame at the given location.
    fn draw(&self, location: Vector, image: &mut RgbImage);
}