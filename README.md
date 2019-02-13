# Photos Picker

[![Build Status](https://travis-ci.org/l-vo/photos-picker.svg?branch=master)](https://travis-ci.org/l-vo/photos-picker)
[![codecov](https://codecov.io/gh/l-vo/photos-picker/branch/master/graph/badge.svg)](https://codecov.io/gh/l-vo/photos-picker)

This libary allows to pick photos in a folder according to a given strategy (last photos, random photos...) and copy them to a destination (another system folder, Dropbox or Google drive folder...)

## Compatibility
This library works and is tested with Python 2.7. Other Python versions are not tested yet.

## Install
```bash
$ pip install photos-picker
```

## Usage
The main class `PhotosPicker` accepts a "picker", a tuple of "filters" and an "uploader" as arguments. The picker allows to select photos while the filters modify them. At the end of the process, the uploader copy transformed (or not) photos to a given destination. Below the simplest example which copy the 50 lastest photos to another directory:

```python
from photospicker.exception.abstract_exception import AbstractException
from photospicker.picker.pickers.last_photos_picker import LastPhotosPicker
from photospicker.uploader.uploaders.filesystem_uploader import FilesystemUploader
from photospicker.photos_picker import PhotosPicker

if __name__ == '__main__':
    try:
        picker = LastPhotosPicker('/pictures', 50)
        uploader = FilesystemUploader('/destination')
    
        photos_picker = PhotosPicker(picker, (), uploader)
        photos_picker.run()
    except AbstractException as err:
        print err.message
```

Since picking and uloading may take a while, progress events are dispatched. 
You can see a more complex example which displays work progress [here](examples/example.py).

### Pickers:
* `LastPhotosPicker`: pick the *n* lastest photos.
* `RandomPicker`: pick randomly *n* photos. 
* `SmartPicker`: pick randomy *n* photos. Recent photos have more chance to be picked than old ones. It results by a picking of a majority of recent photos and a few old ones.

More details [here](doc/pickers.md)

Note you can also create your own picker extending the base class `AbstractPicker`.

### Filters:
* `ResizeFilter`: resize the photos with the given width and height. The final photos size are computed for avoiding distortion.
* `RotateFilter`: Rotate the photos according to EXIF data.

More details [here](doc/filters.md)

Note you can also create your own filter extending the base class `AbstractFilter`.

### Uploaders:
Note that uploaders don't append new photos. Either the directory must be empty or the uploader clear it before copying files.

* `FilesystemUploader`: copy the photos to a given directory. This directory must exist and be empty.
* `DropBoxUploader`: upload the photos to Dropbox. Note that you should limit your token access to application. Creating a full access token is not needed and may induce security issues.
* `GDriveUploader` upload  the photos to Google Drive.

More details [here](doc/uploaders.md)

Note you can also create your own uploader extending the base class `AbstractUploader`.

## Contributing
The project is currenlty currently shipped with many pickers, filters or uploaders. But others can be developed, you may post an issue for that. Or better, pull request are welcome :)

If you submit a pull request, a CI will process some checks:
- That the code is conform with PEP8 standard
- That the unit tests are not broken
- That the functional tests are not broken

For running them locally, functional tests need you to have a Dropbox token and a Google Drive credential file (`mycreds.json`) at the root of the project. The following command process locally at the same checks as the CI:
```bash
$ DROPBOX_TOKEN=mydropboxtoken make validate
```
 
If you don't have Dropbox/Google Drive token/credential file, you can however check the code standards and launch the unit tests:
```bash
$ make lint
$ make test-unit
```