# Contributing Guide

Thank you for contributing to the Beaver Studio project!

## Basics

At the heart of Beaver Studio is the `Artist` trait, the `Animate` trait, and the `Animation` structure.

### `trait Artist`

Types that are `Artist` draw on video frames, creating shapes and other visual objects.

### `trait Animate`

Types that are `Animate` represent animations that occur in time.  Given a `progress` value between 0% and
100%, they create an `Artist` trait object that is capable of creating the animation in the given state.

Any animated data type must implement `Animate`.  This trait has three methods.

- `Animate::play(&self, progress: f64) -> Box<dyn Artist>` (_required_): given a progress value, create an `Artist`
trait object representing the current state of the animation.

- `Animate::clone_box(&self) -> Box<dyn Animate>` (_required_): clone the given trait object, allowing the `Animation`
structure to be passed to Python functions.

- `Animate::animate(&self) -> Animation` (_provided_): construct an `Animation` structure from this trait object.

Moreover, _every type that is `Animate`_ must implement `Self::animate` like so.  This code enables your `MyAnimation`
type to be converted into an `Animation`, which can be processed by Python.

```rust
struct MyAnimation;

impl MyAnimation {
    #[getter]
    pub fn get_animate(&self) -> Animation {
        Animate::animate(self)
    }
}
```

### `struct Animation`

The `Animation` structure contains an `Animate` trait object, and exists to safely interface with Python.