# Pickers

## LastPhotosPicker

### Utility
Pick the *n* lastest photos.

### Constructor arguments
```python
def __init__(self, directory_patterns, photos_count, order=0, patterns=None, excluded_patterns=None):
```
* `directory_path` (list or string): directory path or list of directory paths to scan
* `photos_count` (int): photos count to retrieve
* `order` (int): sort of the retrieved photos:
    * sort=0: retrieved photos are shuffled
    * sort=1: retrieved photos are sorted from the oldest to the most recent
    * sort=-1: retrieved photos are sorted from the most recent to the oldest
* `patterns` (list of strings): patterns to consider, *.tif, *.tiff, *.jpg', *.jpeg and *.png by default
* `excluded_patterns` (list of strings): directory patterns which will be ignored during the scan, a directory is ignored if its path contains one of the strings listed in excluded_patterns

## RandomPicker

### Utility
Pick randomly *n* photos.

### Constructor arguments
```python
def __init__(self, directory_paths, photos_count, order=0, patterns=None, excluded_patterns=None):
```
* `directory_path` (list or string): directory path or list of directory paths to scan
* `photos_count` (int): photos count to retrieve
* `order` (int): sort of the retrieved photos:
    * sort=0: retrieved photos are shuffled
    * sort=1: retrieved photos are sorted from the oldest to the most recent
    * sort=-1: retrieved photos are sorted from the most recent to the oldest
* `patterns` (list of strings): patterns to consider, *.tif, *.tiff, *.jpg', *.jpeg and *.png by default
* `excluded_patterns` (list of string): directory patterns which will be ignored during the scan, a directory is ignored if its path contains one of the strings listed in excluded_patterns

## SmartPicker

### Utility
Pick randomy *n* photos. Recent photos have more chance to be picked than old ones. It results by a picking of a majority of recent photos and a few old ones.

### Constructor arguments
```python
def __init__(self, directory_paths, photos_count, order=0, patterns=None, excluded_patterns=None):
```
* `directory_path` (list or string): directory path or list of directory paths to scan
* `photos_count` (int): photos count to retrieve
* `order` (int): sort of the retrieved photos:
    * sort=0: retrieved photos are shuffled
    * sort=1: retrieved photos are sorted from the oldest to the most recent
    * sort=-1: retrieved photos are sorted from the most recent to the oldest
* `patterns` (list of strings): patterns to consider, *.tif, *.tiff, *.jpg', *.jpeg and *.png by default
* `excluded_patterns` (list of string): directory patterns which will be ignored during the scan, a directory is ignored if its path contains one of the strings listed in excluded_patterns