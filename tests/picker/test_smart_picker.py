from unittest import TestCase
from mock import Mock
from photospicker.picker.smart_picker import SmartPicker
import mock
import unittest_dataprovider


class TestSmartPicker(TestCase):
    """Test class for SmartPicker"""

    @staticmethod
    def provider_scan():
        return (
            (
                100,
                15,
                [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 100],
                [1, 2, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89]
            ),
            (
                50,
                20,
                [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 50],
                [
                    1, 2, 4, 5, 7, 8, 10, 13, 16, 19,
                    22, 25, 28, 31, 34, 37, 40, 43, 46
                ]
            ),
            (
                120,
                80,
                [120],
                range(1, 81)
            ),
            (
                100,
                100,
                [100],
                range(1, 101)
            )
        )

    @unittest_dataprovider.data_provider(provider_scan)
    @mock.patch('random.shuffle')
    def test_scan(
            self,
            photos_count,
            photos_to_retrieve,
            calls_data,
            expected_indexes,
            shuffle_mock
    ):
        """
        Test scan method

        :param int photos_count: photos count for the test
        :param int photos_to_retrieve: photos to retrieve count
        :param list calls_data: data for building expected shuffle call list
        :param list expected_indexes: indexes of the exoected picked photos
        :param mock.MagicMock shuffle_mock: mock for random.shuffle
        """

        shuffle_mock.side_effect = self._shuffle_mock_side_effect

        sut = SmartPicker('', photos_to_retrieve)
        sut._build_sorted_filenames = Mock()
        filenames_returned = []
        for i in range(1, photos_count + 1):
            filenames_returned.append('myphoto{i}.jpg'.format(i=i))
        sut._build_sorted_filenames.return_value = filenames_returned
        sut.scan()

        i = 0
        call = []
        calls = []
        while len(calls_data):
            i += 1
            call.append('myphoto{i}.jpg'.format(i=i))
            if i == calls_data[0]:
                calls.append(mock.call(call))
                call = []
                calls_data.pop(0)

        shuffle_mock.assert_has_calls(calls)

        expected_picked = []
        for i in expected_indexes:
            expected_picked.append('myphoto{i}.jpg'.format(i=i))

        self.assertEqual(
            expected_picked,
            sut.picked_file_paths
        )

    @staticmethod
    def _shuffle_mock_side_effect(photos):
        """
        Side effect for shuffle mock

        :param list photos: photo paths

        :return: list
        """
        return photos
