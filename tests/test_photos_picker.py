from unittest import TestCase
from mock import Mock
from mock import MagicMock
from photospicker.photos_picker import PhotosPicker
import mock


class TestPhotosPicker(TestCase):
    """Test the main photos picker class"""

    @staticmethod
    def _filter_execute_side_effect(file_content):
        """
        Side effect for filter execute method

        :param str file_content: binary content of the file

        :return: str
        """
        return file_content

    @mock.patch('__builtin__.open')
    def test_run(self, mock_open):
        """
        Test run method

        :param mock.MagicMock mock_open: open built'in function mock
        """

        open_mock1 = MagicMock()
        open_mock1.__enter__().read.return_value = 'mydata1'

        open_mock2 = MagicMock()
        open_mock2.__enter__().read.return_value = 'mydata2'

        mock_open.side_effect = [open_mock1, open_mock2]

        picker = Mock()
        picker.picked_file_paths = [
            '/myfolder/myphoto1.jpg',
            '/myfolder/myphoto2.png'
        ]

        filter1 = Mock()
        filter1.execute.side_effect = self._filter_execute_side_effect
        filter2 = Mock()
        filter2.execute.side_effect = self._filter_execute_side_effect

        uploader = Mock()

        photos_picker = PhotosPicker(picker, (filter1, filter2), uploader)
        photos_picker.run()

        picker.initialize.assert_called_once()
        picker.scan.assert_called_once()

        mock_open.assert_has_calls([
            mock.call('/myfolder/myphoto1.jpg', mode='rb'),
            mock.call('/myfolder/myphoto2.png', mode='rb')
        ])

        open_mock1.__enter__().read.assert_called_once()
        open_mock2.__enter__().read.assert_called_once()

        filter1.execute.assert_has_calls([
            mock.call('mydata1'),
            mock.call('mydata2')
        ])
        filter2.execute.assert_has_calls([
            mock.call('mydata1'),
            mock.call('mydata2')
        ])

        uploader.initialize.assert_called_once()
        uploader.upload.assert_has_calls([
            mock.call('mydata1', 'myphoto1.jpg'),
            mock.call('mydata2', 'myphoto2.png')
        ])
