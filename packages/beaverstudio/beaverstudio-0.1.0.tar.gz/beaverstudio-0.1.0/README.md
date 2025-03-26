# Beaver Studio

An open-source 2D graphics engine for video generation, particularly for educational purposes.

**WIP**: Beaver Studio is still under heavy development and does not yet have a stable API!

## Requirements

**MSRV** (Minimum Supported Rust Version): 1.81.0

## Usage

Beaver Studio has three important data structures.  The first is the `Video` data structure, which
holds information about animations and renders them on screen.  The second is the `Animation` data structure,
which holds information about animations of 2D geometry.  The third is the `Shape` data structure,
which holds information about 2D geometries, such as polygons and Bezier curves.

The typical workflow begins with the creation of one or more `Shape` structures.  After creating these shapes,
they can be converted into `Animation` structures using interpolations, traces, or simple display.  These
animations can then be scheduled in the video and rendered on screen.

To begin, import Beaver Studio.

```python
from beaverstudio import *
```

### Creating a `Video` Object

All animations are rendered in videos, which are modeled by a sequence of still frames.  To
initialize a video, specify the width and height, background color (RGB), frame rate, and duration
(in seconds).

```python
video = Video(
    (1920, 1080),   # width, height (pixels)
    [0, 0, 0],      # background color (RGB)
    60,             # frame rate (fps)
    10,             # duration (seconds)
)
```

### Creating Points

In Beaver Studio, the center of the video frame is considered the origin.  All points can be constructed
relative to this origin by the `Vector` class.  Distances are specified in pixels relative to this origin.

```python
p1 = Vector(-10, 10)
```

### Creating Geometry

Nearly all geometry is animated by means of `Shape` objects.  Shapes can be constructed manually, or by creating
polygons or curves and converting them.

#### Building Bezier Curves

Bezier curves may be created using the `Bezier` class.  To create a Bezier curve, specify two or more control
points of the curve (in `Vector` form), an offset to apply to all control points, a color, and a thickness.

```python
b1 = Bezier(
    [point1, point2, point3],   # control points
    Vector.zero(),              # offset
    [255, 0, 0],                # color (RGB)
    2,                          # line thickness (pixels)
)
```

Bezier curves can be converted into `Shape` objects by the `.shape` attribute.

```python
s1 = b1.shape
```

#### Manually Constructing Shapes

Shapes can be manually constructed using a series of Bezier curves.  To create a `Shape` manually, specify a list
of Bezier curves and an offset.

```python
s2 = Shape(
    [bezier1, bezier2], # Bezier curves
    Vector.zero(),      # offset
)
```

#### Building Rectangles

Rectangles can be creating using the `Rect` class.  To create a `Rect`, specify a center, width, height, color,
and line thickness.

```python
r1 = Rect(
    Vector.zero(),  # center
    100,            # width (pixels)
    200,            # height (pixels)
    [0, 255, 255],  # color (RGB)
    10,             # line thickness (pixels)
)
```

Rectangles can be converted into `Shape` objects by the `.shape` attribute.

```python
s3 = r1.shape
```

#### Building Closed Polygons

Closed polygons can be created using the `Polygon` class.  To create a `Polygon`, specify a list of vertices
(in `Vector` form), an offset, a color, and a line thickness.

```python
poly1 = Polygon(
    [vertex1, vertex2, vertex3, vertex4],   # vertices
    Vector.zero(),                          # offset
    [255, 0, 255],                          # color
    12,                                     # line thickness (pixels)
)
```

Polygons can be converted into `Shape` objects by the `.shape` attribute.

```python
s4 = poly1.shape
```

#### Building Coordinate Axes

Coordinate axes do not use the `Shape` class.  Currently, only linear-linear axes are supported.  To create
linear axes, specify an origin location, a grid spacing, and minor gridline counts left and right of the Y axis
and above and below the X axis, respectively.

```python
axes = LinearAxes(
    Vector.zero(),  # origin location (pixels)
    100,            # grid spacing
    (8, 8),         # minor gridlines left and right of Y axis
    (5, 5),         # minor gridlines above and below X axis
)
```

Coordinate axes can be traced, displayed, and untraced directly.

```python
axes_anim = axes.trace
```

#### Building Parametric Curves

Parametric curves, like coordinate axes, do not use the `Shape` class.  To create a parametric curve, specify
two functions of time for the X and Y positions, as well as time bounds, an offset, a color, and a thickness.
Note that the result of the X and Y positions are in pixels.  If using this with coordinate axes, ensure that
this is consistent with the axes' grid spacing, for best results.

```python
para1 = Parametric(
    lambda t: 100*t,            # X position
    lambda t: 100*sin(100*t),   # Y position
    (-3.14, 3.14),              # time bounds (min, max)
    Vector.zero(),              # offset (pixels)
    [255, 0, 0],                # color (RGB)
    4,                          # line thickness (pixels)
)
```

### Creating Animations

Once `Shape` objects have been created, they need to be converted into `Animation` objects before they can be
added to the video.

#### Interpolation

One shape can smoothly become another using the `Shape.into()` method.

```python
anim1 = shape1.into(shape2)
```

#### Display

A shape can be simply displayed using the `.display` attribute.

```python
anim2 = shape.display
```

#### Trace

You can trace out a shape, creating a real-time drawing effect, by the `.trace` attribute.

```python
anim3 = shape.trace
```

You can also "untrace" the shape, creating a real-time erasing effect, by the `.untrace` attribute.

```python
anim4 = shape.untrace
```

### Adding Animations to the Video

Animations are added to the video using `Video.add()`.  To add an animation, specify its
offset, its start time (in seconds), and its end time (in seconds).

```python
video.add(
    animation,      # animation
    Vector.zero(),  # offset
    1.5,            # start time (seconds)
    3,              # end time (seconds)
)
```