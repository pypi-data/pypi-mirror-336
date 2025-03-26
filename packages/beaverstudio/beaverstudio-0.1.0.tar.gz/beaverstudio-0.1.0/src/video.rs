//! A video.

use std::{
    f64::consts::PI,
    fs,
};

use image::{
    Rgb,
    RgbImage,
};

use indicatif::{
    ProgressBar,
    ProgressStyle,
};

use pyo3::prelude::*;

use rayon::{
    prelude::*,
    ThreadPoolBuilder,
};

use crate::{
    Animation,
    LinearAxes,
    Parametric,
    Shape,
    Vector,
};

/// Time required to trace an object (seconds).
pub const TRACE_TIME: f64 = 1.0;

/// Type alias for an animation with its location and start/stop frames.
type Instance = (Animation, Vector, u32, u32);

#[pyclass]
/// A video, represented as a series of still frames.
pub struct Video {
    #[pyo3(get, set)]
    /// Video width (pixels).
    width: u32,

    #[pyo3(get, set)]
    /// Video height (pixels).
    height: u32,

    /// Background color (RGB).
    background: Rgb<u8>,

    #[pyo3(get, set)]
    /// Video frame rate (fps).
    fps: f64,

    #[pyo3(get, set)]
    /// Video duration (seconds).
    duration: f64,

    /// Video animations, combined with their location, start frame, and end frame.
    animations: Vec<Instance>,
}

#[pymethods]
impl Video {
    #[new]
    /// Construct a new video.
    pub fn new(
        size: (u32, u32),
        background: [u8; 3],
        fps: f64,
        duration: f64,
    ) -> Self {
        Self {
            width: size.0,
            height: size.1,
            background: Rgb (background),
            fps,
            duration,
            animations: Vec::new(),
        }
    }

    /// Add an animation to this video.
    /// 
    /// Note that `start` and `end` are given in seconds.  These are converted into
    /// frame numbers based on the FPS of the video.
    pub fn add(&mut self, animation: Animation, location: Vector, start: f64, end: f64) {
        // Frame numbers from timestamps
        let start_frame = (start * self.fps) as u32;
        let end_frame = (end * self.fps) as u32;

        self.animations.push((animation, location, start_frame, end_frame));
    }

    /// Trace and untrace a shape on this video.
    /// 
    /// Note that `start` and `end` are given in seconds.  These are converted into
    /// frame numbers based on the FPS of the video.  For `Video::trace_untrace`, these
    /// must be at least 2 seconds apart.
    pub fn add_shape(&mut self, shape: Shape, location: Vector, start: f64, end: f64) {
        if end - start < 2.0 {
            return;
        }

        self.add(shape.get_trace(), location, start, start + TRACE_TIME);
        self.add(shape.get_display(), location, start + TRACE_TIME, end - TRACE_TIME);
        self.add(shape.get_untrace(), location, end - TRACE_TIME, end);
    }

    /// Create a "flow" effect according to a parametric curve.
    /// 
    /// Note that `start` and `end` are given in seconds.  These are converted into
    /// frame numbers based on the FPS of the video.  For `Video::trace_untrace`, these
    /// must be at least 2 seconds apart.
    pub fn flow(&mut self, parametric: Parametric, location: Vector, start: f64) {
        self.add(parametric.get_trace(), location, start, start + TRACE_TIME*0.5);
        self.add(parametric.get_untrace(), location, start + TRACE_TIME*0.5, start + TRACE_TIME);
    }

    /// Trace and untrace a parametric on this video.
    /// 
    /// Note that `start` and `end` are given in seconds.  These are converted into
    /// frame numbers based on the FPS of the video.  For `Video::trace_untrace`, these
    /// must be at least 2 seconds apart.
    pub fn add_parametric(&mut self, parametric: Parametric, location: Vector, start: f64, end: f64) {
        if end - start < 2.0 {
            return;
        }

        self.add(parametric.get_trace(), location, start, start + TRACE_TIME);
        self.add(parametric.get_display(), location, start + TRACE_TIME, end - TRACE_TIME);
        self.add(parametric.get_untrace(), location, end - TRACE_TIME, end);
    }

    /// Trace and untrace linear axes on this video.
    /// 
    /// Note that `start` and `end` are given in seconds.  These are converted into
    /// frame numbers based on the FPS of the video.  For `Video::trace_untrace`, these
    /// must be at least 2 seconds apart.
    pub fn add_axes(&mut self, linear_axes: LinearAxes, location: Vector, start: f64, end: f64) {
        if end - start < 2.0 {
            return;
        }

        self.add(linear_axes.get_trace(), location, start, start + TRACE_TIME);
        self.add(linear_axes.get_display(), location, start + TRACE_TIME, end - TRACE_TIME);
        self.add(linear_axes.get_untrace(), location, end - TRACE_TIME, end);
    }

    #[pyo3(signature=(output_dir, threads=1))]
    /// Render this video from a series of still frames.
    pub fn render(&self, output_dir: String, threads: usize) {
        // How many frames?
        let frame_count = (self.duration * self.fps) as u32;

        // Progress bar style
        let style = ProgressStyle::with_template(
            "[{elapsed_precise}] {wide_bar} {pos:>7}/{len:7} frames [ETA {eta_precise}]"
        ).unwrap();

        // Clear/create output directory
        fs::remove_dir_all(&output_dir).unwrap();
        fs::create_dir_all(&output_dir).unwrap();

        // Progress bar, for user
        let bar = ProgressBar::new(frame_count as u64).with_style(style);

        // Create thread pool
        ThreadPoolBuilder::new().num_threads(threads).build_global().unwrap();

        // Render in parallel
        (0..frame_count).into_par_iter().for_each(|k| {
            // New, empty frame
            let mut frame = RgbImage::new(self.width, self.height);

            // Create background
            for i in 0..self.width {
                for j in 0..self.height {
                    frame.put_pixel(i, j, self.background);
                }
            }

            for (animation, location, start, end) in &self.animations {
                // Determine progress of this animation
                let progress = (k as f64 - *start as f64) / (*end as f64 - *start as f64);

                if 0.0 <= progress && progress <= 1.0 {
                    // Transform the progress variable to create smooth transitions
                    let progress_transform = 0.5 - 0.5 * (progress * PI).cos();

                    // Construct visual artist from this animation
                    let artist = animation.0.play(progress_transform);

                    // Draw on this frame
                    artist.draw(*location, &mut frame);
                }
            }

            frame.save(format!("{}/frame_{:04}.png", output_dir, k)).unwrap();

            // Increment progress bar
            bar.inc(1);
        });

        bar.finish();
    }
}