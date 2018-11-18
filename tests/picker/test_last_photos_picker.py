from photospicker.picker.last_photos_picker import LastPhotosPicker
from unittest import TestCase
from mock import Mock


class TestLastPhotosPicker(TestCase):
    """Test class for LastPhotosPicker"""

    def test_scan(self,):
        """Test scan method"""

        sut = LastPhotosPicker('', 2)
        build_method_mock = Mock()
        build_method_mock.return_value = [
            'myphoto4.jpg',
            'myphoto1.jpg',
            'myphoto3.jpg'
        ]
        sut._build_photos_to_select_list = build_method_mock
        sut.scan()

        self.assertEqual(
            ['myphoto4.jpg', 'myphoto1.jpg'],
            sut.picked_file_paths
        )
