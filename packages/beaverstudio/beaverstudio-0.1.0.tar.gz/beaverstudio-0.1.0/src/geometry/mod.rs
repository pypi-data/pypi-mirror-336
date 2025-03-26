//! Geometry abstractions for Beaver Studio.

mod bezier;
mod circle;
mod linear_axes;
mod parametric;
mod polygon;
mod rectangle;
mod shape;
mod vector;

pub use bezier::Bezier;
pub use circle::Circle;
pub use linear_axes::LinearAxes;
pub use parametric::Parametric;
pub use polygon::Polygon;
pub use rectangle::Rectangle;
pub use shape::Shape;
pub use vector::Vector;