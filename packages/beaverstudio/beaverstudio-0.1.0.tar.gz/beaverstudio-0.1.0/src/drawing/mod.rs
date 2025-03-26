//! Drawing abstractions for Beaver Studio.

mod animation;
mod artist;
mod bresenham;
mod brush;
mod interpolate;
mod trace;

pub use animation::{
    Animate,
    Animation,
};
pub use artist::Artist;
pub use bresenham::Bresenham;
pub use brush::Brush;
pub use interpolate::Interpolate;
pub use trace::{
    Trace,
    TracedShape,
};