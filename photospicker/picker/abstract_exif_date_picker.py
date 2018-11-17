from photospicker.picker.abstract_picker import AbstractPicker
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image
from PIL import ExifTags
from abc import ABCMeta, abstractmethod
import operator


class AbstractExifDatePicker(AbstractPicker):
    """Abstract class for pickers based on Exif photo date"""

    __metaclass__ = ABCMeta

    def scan(self):
        """Order photos by exif date and launch discriminating method"""
        data_to_sort = {}

        scanned = 0
        self._notify_progress(scanned)
        for filepath in self._files_to_scan:
            img = Image.open(filepath)

            if isinstance(img, JpegImageFile):
                exif_data = img._getexif()

                if exif_data is None:
                    exif_data = {}

                for key in exif_data.keys():
                    if ExifTags.TAGS.get(key) != 'DateTimeOriginal':
                        continue

                    data_to_sort[filepath] = exif_data[key]

            scanned += 1
            self._notify_progress(scanned)

        self._notify_end()

        sorted_data = sorted(
            data_to_sort.items(),
            key=operator.itemgetter(1),
            reverse=True
        )

        for filename, data in sorted_data:
            self._picked_file_paths.append(filename)

        self._select()

    @abstractmethod
    def _select(self):  # pragma: no cover
        """
        Finally select photos

        :raise NotImplementedError
        """
        raise NotImplementedError()
