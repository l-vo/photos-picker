from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker


class LastPhotosPicker(AbstractExifDatePicker):
    """Pick the lastest photos by DateTimeOriginal in EXIF data"""

    def scan(self):
        """Scan the given path for building picked file paths list"""

        sorted_filenames = self._build_sorted_filenames()

        for key, filename in enumerate(sorted_filenames):
            if key >= self._photos_count:
                break
            self._picked_file_paths.append(filename)
