from photospicker.picker.picker_photo import PickerPhoto


class PickerPhotoStub(PickerPhoto):
    """Stub for comparing with PickerPhoto objects"""

    def __eq__(self, other):
        """Equality behavior"""
        if not isinstance(other, PickerPhoto):
            return False

        return self._filepath == other._filepath and self._date == self._date
