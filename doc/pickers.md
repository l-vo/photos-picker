# Pickers

## LastPhotosPicker

### Utility
Pick the *n* lastest photos.

### Constructor arguments
```python
def __init__(self, directory_paths, photos_count, patterns=None, excluded_paths=None):
```
* `directory_path` (list or string): directory path or list of directory paths to scan
* `photos_count` (int): photos count to retrieve
* `patterns` (list of strings): patterns to consider, *.tif, *.tiff, *.jpg', *.jpeg and *.png by default
* `excluded_paths` (list of string): directory paths which will be ignored during the scan

## RandomPicker

### Utility
pick randomly *n* photos.

### Constructor arguments
```python
def __init__(self, directory_paths, photos_count, patterns=None, excluded_paths=None):
```
* `directory_path` (list or string): directory path or list of directory paths to scan
* `photos_count` (int): photos count to retrieve
* `patterns` (list of strings): patterns to consider, *.tif, *.tiff, *.jpg', *.jpeg and *.png by default
* `excluded_paths` (list of string): directory paths which will be ignored during the scan