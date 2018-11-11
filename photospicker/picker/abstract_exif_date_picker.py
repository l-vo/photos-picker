from photospicker.picker.abstract_picker import AbstractPicker
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image
from PIL import ExifTags
from abc import ABCMeta
import operator


class AbstractExifDatePicker(AbstractPicker):
    """Abstract class for pickers based on Exif photo date"""

    __metaclass__ = ABCMeta

    def _build_sorted_filenames(self):
        """
        Build a list of photos sorted by Exif date in reverse order

        :return list
        """

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

        filenames = []
        for filename, data in sorted_data:
            filenames.append(filename)

        return filenames
