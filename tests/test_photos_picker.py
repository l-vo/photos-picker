from unittest import TestCase
from mock import Mock
from mock import MagicMock
from photospicker.photos_picker import PhotosPicker
import mock


class TestPhotosPicker(TestCase):
    """Test the main photos picker class"""

    @mock.patch('__builtin__.open')
    def test_run(self, mock_open):
        """
        Test run method

        :param MagicMock mock_open: open built'in function mock
        """

        open_mock1 = MagicMock()
        open_mock1.__enter__().read.return_value = 'mydata1'

        open_mock2 = MagicMock()
        open_mock2.__enter__().read.return_value = 'mydata2'

        mock_open.side_effect = [open_mock1, open_mock2]

        picker = Mock()
        uploader = Mock()
        picker.picked_file_paths = [
            '/myfolder/myphoto1.jpg',
            '/myfolder/myphoto2.png'
        ]

        photos_picker = PhotosPicker(picker, uploader)
        photos_picker.run()

        picker.initialize.assert_called_once()
        picker.scan.assert_called_once()

        mock_open.assert_has_calls([
            mock.call('/myfolder/myphoto1.jpg', mode='rb'),
            mock.call('/myfolder/myphoto2.png', mode='rb')
        ], any_order=True)

        open_mock1.__enter__().read.assert_called_once()
        open_mock2.__enter__().read.assert_called_once()

        uploader.initialize.assert_called_once()
        uploader.upload.assert_has_calls([
            mock.call('mydata1', 'myphoto1.jpg'),
            mock.call('mydata2', 'myphoto2.png')
        ])
