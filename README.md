# Photos Picker

[![Build Status](https://travis-ci.org/l-vo/photos-picker.svg?branch=master)](https://travis-ci.org/l-vo/photos-picker)

This libary allows to pick photos in a folder according to a given strategy (last photos, random photos...) and copy them to a destination (another folder, Dropbox folder...)

## Compatibility
This library works and is tested with Python 2.7. Other Python versions are not tested yet.

## Usage
The main class `PhotosPicker` accepts a "picker" and an "uploader" as arguments. The picker allows to select photos while the uploader copy them to a given destination. This is the simplest example which copy the 50 lastest photos to another directory:

```python
from photospicker.picker.last_photos_picker import LastPhotosPicker
from photospicker.uploader.filesystem_uploader import FilesystemUploader
from photospicker.photos_picker import PhotosPicker

if __name__ == '__main__':
    picker = LastPhotosPicker('/pictures', 50)
    uploader = FilesystemUploader('/destination')

    photos_picker = PhotosPicker(picker, uploader)
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
from zope.event.classhandler import handler
from photospicker.photos_picker import PhotosPicker

import sys


@handler(ScanProgressEvent)
def progress_listener(event):
    """Display pick progression

    :param ScanProgressEvent event: event
    """
    percent = int(event.files_scanned * 100/event.files_to_scan)
    print("\rScanning files: {percent}%".format(percent=percent), end='')
    sys.stdout.flush()

    if event.end:
        print("\nPicking photos...")


@handler(StartUploadEvent)
def start_upload_listener(event):
    """Display info when an upload starts

    :param StartUploadEvent event: event
    """

    msg = "Upload {rank}/{total}: uploading {filepath}..."
    print(msg.format(rank=event.upload_file_rank, total=event.files_to_upload, filepath=event.filepath), end='')
    sys.stdout.flush()


@handler(EndUploadEvent)
def end_upload_listener(event):
    """Display info when an upload ends

    :param EndUploadEvent event: event
    """
    msg = "\rUpload {uploaded}/{total}: upload finished for {filepath}"
    print(msg.format(uploaded=event.uploaded_files, total=event.files_to_upload, filepath=event.filepath))


if __name__ == '__main__':

    picker = LastPhotosPicker('/pictures', 50)
    uploader = FilesystemUploader('/destination')

    photos_picker = PhotosPicker(picker, uploader)
    photos_picker.run()
```

### Pickers:
* `LastPhotosPicker`: pick the *n* lastest photos. *n* is passed as argument to the constructor.
* `RandomPicker`: pick randomly *n* photos. *n* is passed as argument to the constructor.

### Uploaders:
Note that uploaders don't append new photos. Either the directory must be empty or the uploader clear it before copying files.

* `FilesystemUploader`: copy the photos to the directory passed as class constructor argument. This directory must exist and not be empty.
* `DropBoxUploader`: upload the photos to Dropbox. The class constructor accepts a Dropbox API token as argument. ***Be careful, the script empty the `/photos` directory, you must limit your token access to application for avoiding unwanted deletions***.

## Contributing
Other pickers and uploaders will come along the time. If you need a specific picker or a specific uploader, post an issue. Or better, submit a pull request :)
