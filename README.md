# Photos Picker

[![Build Status](https://travis-ci.org/l-vo/photos-picker.svg?branch=master)](https://travis-ci.org/l-vo/photos-picker)
[![codecov](https://codecov.io/gh/l-vo/photos-picker/branch/master/graph/badge.svg)](https://codecov.io/gh/l-vo/photos-picker)

This libary allows to pick photos in a folder according to a given strategy (last photos, random photos...) and copy them to a destination (another folder, Dropbox folder...)

## Compatibility
This library works and is tested with Python 2.7. Other Python versions are not tested yet.

## Install
```bash
$ pip install photos-picker
```

## Usage
The main class `PhotosPicker` accepts a "picker", a tuple of "filters" and an "uploader" as arguments. The picker allows to select photos while the filters modify them. At the end of the process, the uploader copy transformed (or not) photos to a given destination. Below the simplest example which copy the 50 lastest photos to another directory:

```python
from photospicker.picker.last_photos_picker import LastPhotosPicker
from photospicker.uploader.filesystem_uploader import FilesystemUploader
from photospicker.photos_picker import PhotosPicker

if __name__ == '__main__':
    picker = LastPhotosPicker('/pictures', 50)
    uploader = FilesystemUploader('/destination')

    photos_picker = PhotosPicker(picker, (), uploader)
    photos_picker.run()
```

Since picking and uloading may take a while, progress events are dispatched. 
You can see a more complex example which displays work progress [here](examples/example.py).

### Pickers:
* `LastPhotosPicker`: pick the *n* lastest photos. *n* is passed as argument to the constructor.
* `RandomPicker`: pick randomly *n* photos. *n* is passed as argument to the constructor.

### Filters:
* `ResizeFilter`: resize the photos with the width and height passed as filter arguments. The final photos sizes are computed for avoiding distortion.
* `RotateFilter`: rotate the photos according to EXIF data. Setting the expand argument to `True` allows to expands the output image to make it large enough to hold the entire rotated image.

### Uploaders:
Note that uploaders don't append new photos. Either the directory must be empty or the uploader clear it before copying files.

* `FilesystemUploader`: copy the photos to the directory passed as class constructor argument. This directory must exist and not be empty.
* `DropBoxUploader`: upload the photos to Dropbox. The class constructor accepts a Dropbox API token as argument. ***Be careful, the script empty the `/photos` directory, you must limit your token access to application for avoiding unwanted deletions***.

## Contributing
Other pickers, filters and uploaders will come along the time. If you need a specific picker, filter or uploader, post an issue. Or better, submit a pull request :)

If you submit a pull request, be sure that the PEP8 standards are respected and the tests are not broken launching the following command:
```bash
$ make validate
```
