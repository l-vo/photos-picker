from event.start_upload_event import StartUploadEvent
from event.end_upload_event import EndUploadEvent
from zope.event import notify
import ntpath


class PhotosPicker:
    """
    Select photos accorting to a chosen strategy and
    copy them to a chosen destination
    """

    def __init__(self, picker, uploader):
        """
        Constructor

        :param AbstractPicker picker    : photo selection strategy
        :param AbstractUploader uploader: upload strategy
        """
        self._picker = picker
        self._uploader = uploader

    def run(self):
        """Run photo selection and upload"""
        self._picker.initialize()
        self._picker.scan()

        total_picked = len(self._picker.picked_file_paths)

        self._uploader.initialize()
        for key, filepath in enumerate(self._picker.picked_file_paths):
            rank = key + 1
            with open(filepath, mode='rb') as f:
                file_content = f.read()

            notify(StartUploadEvent(filepath, rank, total_picked))
            self._uploader.increase_photo_counter()
            self._uploader.upload(file_content, ntpath.basename(filepath))
            notify(EndUploadEvent(filepath, rank, total_picked))
