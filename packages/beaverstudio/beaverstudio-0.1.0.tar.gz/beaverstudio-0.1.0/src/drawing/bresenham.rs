//! Bresenham line-drawing algorithm.

/// A Bresenham line.
pub struct Bresenham {
    pub points: Vec<(u32, u32)>,
}

impl Bresenham {
    /// Construct a new Bresenham line.
    pub fn new(x0: u32, y0: u32, x1: u32, y1: u32) -> Self {
        // Line points
        let mut points = Vec::new();
        
        // Delta X and Delta Y
        let dx = x1.abs_diff(x0);
        let dy = y1.abs_diff(y0);

        // Is this a "steep" line?
        let steep = dy > dx;

        // Direction of X and Y
        let x_pos = x1 > x0;
        let y_pos = y1 > y0;

        // Current points
        let (mut x, mut y) = (x0, y0);

        // Draw first point
        points.push((x, y));

        // Error
        let mut error = 0;

        while x1.abs_diff(x) + y1.abs_diff(y) > 1 {
            // Update primary variable
            if steep {
                if y_pos {
                    y += 1;
                } else {
                    y -= 1;
                }
            } else {
                if x_pos {
                    x += 1;
                } else {
                    x -= 1;
                }
            }

            // Update error
            error += if steep {
                2*dx
            } else {
                2*dy
            };

            // Update secondary variable
            if steep {
                if error > dy {
                    if x_pos {
                        x += 1;
                    } else {
                        x -= 1;
                    }

                    // Adjusting in secondary direction decreases our error
                    error -= 2*dy;
                }
            } else {
                if error > dx {
                    if y_pos {
                        y += 1;
                    } else {
                        y -= 1;
                    }

                    // Adjusting in secondary direction decreases our error
                    error -= 2*dx;
                }
            }

            points.push((x, y));
        }

        Self {
            points,
        }
    }
}