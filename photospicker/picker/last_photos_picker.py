from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker


class LastPhotosPicker(AbstractExifDatePicker):
    """Pick the lastest photos by DateTimeOriginal in EXIF data"""

    def _select(self):
        """Finally select photos"""
        self._picked_file_paths = [
            filename for key, filename in enumerate(self._picked_file_paths)
            if key < self._photos_count
        ]
