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

Since picking and uloading may take a while, progress events are dispatched. This is a more complex example which displays work progress:

```python
from __future__ import division
from __future__ import print_function

from photospicker.picker.last_photos_picker import LastPhotosPicker
from photospicker.uploader.filesystem_uploader import FilesystemUploader
from photospicker.event.scan_progress_event import ScanProgressEvent
from photospicker.event.start_upload_event import StartUploadEvent
from photospicker.event.end_upload_event import EndUploadEvent
from photospicker.event.start_filter_event import StartFilterEvent
from photospicker.event.end_filter_event import EndFilterEvent
from zope.event.classhandler import handler
from photospicker.photos_picker import PhotosPicker

import sys


@handler(ScanProgressEvent)
def progress_listener(event):
    """
    Display pick progression

    :param ScanProgressEvent event: event
    """
    percent = int(event.files_scanned * 100/event.files_to_scan)
    print("\rScanning files: {percent}%".format(percent=percent), end='')
    sys.stdout.flush()

    if event.end:
        print("\nPicking photos...")


@handler(StartUploadEvent)
def start_upload_listener(event):
    """
    Display info when an upload starts

    :param StartUploadEvent event: event
    """

    msg = "Upload {rank}/{total}: uploading {filepath}..."
    print(msg.format(rank=event.upload_file_rank, total=event.files_to_upload, filepath=event.filepath), end='')
    sys.stdout.flush()


@handler(EndUploadEvent)
def end_upload_listener(event):
    """
    Display info when an upload ends

    :param EndUploadEvent event: event
    """
    msg = "\rUpload {uploaded}/{total}: upload finished for {filepath}"
    print(msg.format(uploaded=event.uploaded_files, total=event.files_to_upload, filepath=event.filepath))
    
@handler(StartFilterEvent)
def start_filter_listener(event):
    """
    Display when a filter start

    :param StartFilterEvent event: event
    """
    msg = "Start filter {filter} for {filepath}";
    print(msg.format(filter=event.filter_name(), filepath=event.filepath()))


@handler(EndFilterEvent)
def end_filter_listener(event):
    """
    Display when a filter end

    :param EndFilterEvent event: event
    """
    msg = "End filter {filter} for {filepath}"
    print(msg.format(filter=event.filter_name(), filepath=event.filepath()))


if __name__ == '__main__':

    picker = LastPhotosPicker('/pictures', 50)
    uploader = FilesystemUploader('/destination')

    photos_picker = PhotosPicker(picker, (800, 600), uploader)
    photos_picker.run()
```

### Pickers:
* `LastPhotosPicker`: pick the *n* lastest photos. *n* is passed as argument to the constructor.
* `RandomPicker`: pick randomly *n* photos. *n* is passed as argument to the constructor.

### Filters:
* `ResizeFilter`: resize the photos with the width and height passed as filter arguments. The final photos sizes are computed for avoiding distortion.

### Uploaders:
Note that uploaders don't append new photos. Either the directory must be empty or the uploader clear it before copying files.

* `FilesystemUploader`: copy the photos to the directory passed as class constructor argument. This directory must exist and not be empty.
* `DropBoxUploader`: upload the photos to Dropbox. The class constructor accepts a Dropbox API token as argument. ***Be careful, the script empty the `/photos` directory, you must limit your token access to application for avoiding unwanted deletions***.

## Contributing
Other pickers, filters and uploaders will come along the time. If you need a specific picker, filter or uploader, post an issue. Or better, submit a pull request :)

If you submit a pull request, be sure that the PEP8 standards are respected and the tests are not broken launching the following command:
```bash
$ make valid
```
