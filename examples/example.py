from __future__ import division
from __future__ import print_function

from photospicker.picker.last_photos_picker import LastPhotosPicker
from photospicker.uploader.filesystem_uploader import FilesystemUploader
from photospicker.filter.resize_filter import ResizeFilter
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

    try:
        picker = LastPhotosPicker('/pictures', 50)
        uploader = FilesystemUploader('/destination')
        filters = (ResizeFilter(800, 600),)

        photos_picker = PhotosPicker(picker, filters, uploader)
        photos_picker.run()
    except Exception as err:
        if err.message:
            print(err.message)
        else:
            raise err
