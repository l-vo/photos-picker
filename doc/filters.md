# Filters

## ResizeFilter

### Utility
Resize the photos with the given width and height. The final photos size are computed for avoiding distortion.

### Constructor arguments
```python
def __init__(self, max_width, max_height):
```

* `max_width` (int): max width of the photo after resizing
* `max_height` (int): max height of the photo after resizing

## RotateFilter

### Utility
Rotate the photos according to EXIF data.

### Constructor arguments
```python
def __init__(self, expand=True)
```

* `expand` (bool): whether the output photo will be expanded to make it large enough to hold the entire rotated image.