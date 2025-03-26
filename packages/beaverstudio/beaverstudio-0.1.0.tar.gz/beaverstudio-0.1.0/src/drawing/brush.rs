//! A brush of a given thickness.

#[derive(Clone)]
/// A brush that draws a line or curve.
pub struct Brush {
    pub points: Vec<(i32, i32, f64)>,
}

impl Brush {
    /// Construct a circular brush based on a given thickness.
    pub fn new(thickness: i32) -> Self {
        // Curve "brush"
        let mut points = Vec::new();

        // See if points are in brush
        for i in -thickness..thickness {
            for j in -thickness..thickness {
                let dist = 4 * i.pow(2) + 4 * j.pow(2);
                if dist <= thickness.pow(2) {
                    points.push((i, j, 1.0));
                } else if dist <= (thickness + 2).pow(2) {
                    points.push((i, j, 0.7));
                } else if dist <= (thickness + 4).pow(2) {
                    points.push((i, j, 0.4));
                } else if dist <= (thickness + 6).pow(2) {
                    points.push((i, j, 0.1));
                }
            }
        }

        Self {
            points,
        }
    }
}