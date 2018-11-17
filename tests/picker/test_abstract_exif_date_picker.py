from PIL.JpegImagePlugin import JpegImageFile
from unittest import TestCase
from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker
from mock import MagicMock  # noqa
from mock import Mock
import mock


class DummyPicker(AbstractExifDatePicker):
    """Dummy class for testing AbstractExifDatePicker"""

    def _select(self):
        """Dummy abstract method"""
        pass

    @property
    def picked_file_paths(self):
        """Getter for _picked_file_paths return"""
        return self._picked_file_paths


class TestAbstractExifDatePicker(TestCase):
    """Unit tests for AbstractExifDatePicker"""

    @mock.patch('PIL.Image.open')
    @mock.patch('os.walk')
    def test_scan(self, walk_mock, image_open_mock):
        """
        Test scan

        :param MagicMock walk_mock:       mock for walk method
        :param MagicMock image_open_mock: mock for PIL Image mock method
        """

        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.jpg',
            'myphoto3.jpg',
            'myphoto4.jpg',
            'myphoto5.jpg'
        ]]]

        image_mock1 = Mock(spec=JpegImageFile)
        image_mock1._getexif.return_value = {
            36865: 'myData',
            36867: '2017-05-01 23:50:00'
        }

        image_mock2 = Mock(spec=JpegImageFile)
        image_mock2._getexif.return_value = None

        image_mock3 = Mock(spec=JpegImageFile)
        image_mock3._getexif.return_value = {
            36867: '2017-05-01 23:49:50',
            36882: 'myOtherData'
        }

        image_mock4 = Mock(spec=JpegImageFile)
        image_mock4._getexif.return_value = {
            36864: 'myOtherData',
            36867: '2017-05-01 23:55:00',
            36888: 'anotherData'
        }

        image_mock5 = Mock()

        image_open_mock.side_effect = [
            image_mock1,
            image_mock2,
            image_mock3,
            image_mock4,
            image_mock5
        ]

        select_mock = Mock()

        sut = DummyPicker('', 0)
        sut._select = select_mock
        sut.initialize()
        sut.scan()

        select_mock.assert_called_once()

        self.assertEqual(
            ['myphoto4.jpg', 'myphoto1.jpg', 'myphoto3.jpg'],
            sut.picked_file_paths
        )
