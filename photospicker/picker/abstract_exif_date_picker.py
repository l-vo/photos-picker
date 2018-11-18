from photospicker.picker.abstract_picker import AbstractPicker
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image
from PIL import ExifTags
from abc import ABCMeta, abstractmethod
import operator


class AbstractExifDatePicker(AbstractPicker):
    """Abstract class for pickers based on Exif photo date"""

    __metaclass__ = ABCMeta

    def _scan(self):  # pragma: no cover
        """
        Order photos by exif date and launch discriminating method

        :return list
        """
        return self._select(self._build_photos_to_select_list())

    def _build_photos_to_select_list(self):
        """
        Create an ordered photos list to select photos inside

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

        ret = []
        for filename, data in sorted_data:
            ret.append(filename)

        return ret

    @abstractmethod
    def _select(self, to_select):  # pragma: no cover
        """
        Finally select photos

        :param list to_select: list where process selection

        :return list
        """
        raise NotImplementedError()
