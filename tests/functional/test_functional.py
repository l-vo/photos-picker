from unittest import TestCase
import subprocess
import os
import hashlib
import unittest_dataprovider
from unittest import SkipTest

from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import DeleteError
from pydrive.drive import GoogleDrive

from photospicker.uploader.uploaders.gdrive_uploader import GDriveUploader
from pydrive.auth import GoogleAuth

from photospicker.uploader.uploaders.dropbox_uploader import DropboxUploader

from photospicker.filter.filters.rotate_filter import RotateFilter
from photospicker.photos_picker import PhotosPicker
from photospicker.uploader.uploaders.filesystem_uploader import FilesystemUploader

from photospicker.filter.filters.resize_filter import ResizeFilter
from photospicker.picker.pickers.last_photos_picker import LastPhotosPicker


class TestFunctional(TestCase):
    """Functional tests for whole the application"""

    @classmethod
    def setUpClass(cls):
        if 'TMPDIR' in os.environ.keys():
            cls.tmpdir = os.environ['TMPDIR']
        else:
            cls.tmpdir = '/tmp'

        skip_reason = "Can't execute functional tests if {dir} already exists"

        cls.sample_dir = cls.tmpdir + '/photos-picker-exif-samples'
        if os.path.isdir(cls.sample_dir):
            raise SkipTest(skip_reason.format(dir=cls.sample_dir))

        cls.target_dir = cls.tmpdir + '/tests-photos-picker'
        if os.path.isdir(cls.target_dir):
            raise SkipTest(skip_reason.format(dir=cls.target_dir))

        cls.remote_test_dir = 'photos-picker-test'

        func_tests_dir = os.path.dirname(os.path.realpath(__file__))
        cls.gdrive_creds_filepath = func_tests_dir + '/../../mycreds.json'

        samples_zip = cls.tmpdir + '/samples.zip'
        subprocess.call([
            "curl",
            "https://codeload.github.com/ianare/exif-samples/zip/"
            + "1c14d21c5278c77fc8183f260876b9799ea14a3b",
            "-o",
            samples_zip
        ])

        subprocess.call([
            "unzip",
            samples_zip,
            "-d",
            cls.tmpdir
        ])

        subprocess.call([
            "mv",
            cls.tmpdir
            + '/exif-samples-1c14d21c5278c77fc8183f260876b9799ea14a3b',
            cls.sample_dir
        ])

        # Causes problem with LastDatePicker (same date as another photo)
        # When date is the same, order may be different depending on systems
        os.remove(cls.sample_dir + '/jpg/hdr/iphone_hdr_NO.jpg')

    def setUp(self):
        subprocess.call(['mkdir', self.target_dir])

    @staticmethod
    def provider_filesystem_uploader():
        """
        Dataprovider for filesystem uploader

        :return: tuple
        """
        return (
            ([ResizeFilter(100, 100), RotateFilter()], {
                'photo1.jpg': '9f8bb12a840adc598c9257f0309fd04b',
                'photo2.jpg': '615a8cd4f1ead919dbe268a4d0526263',
                'photo3.jpg': '4955a9411b47113c07a3d9767ba67955',
                'photo4.jpg': '7517ea032f3bab1ecab4006a5e6dbe9b',
                'photo5.jpg': '25ca68bc469e3e63eddf38be7fbaaeed'
            }),
            ([ResizeFilter(100, 100)], {
                'photo1.jpg': '9f8bb12a840adc598c9257f0309fd04b',
                'photo2.jpg': '615a8cd4f1ead919dbe268a4d0526263',
                'photo3.jpg': '4955a9411b47113c07a3d9767ba67955',
                'photo4.jpg': '1bda1787b7aeef690f1d21a43d3b5e21',
                'photo5.jpg': '1bffaba99a0efcf8e4d033b2f451e0b2'
            }),
            ([RotateFilter()], {
                'photo1.jpg': '9f8bb12a840adc598c9257f0309fd04b',
                'photo2.jpg': '95268c0535b0588f5d01181162d382a7',
                'photo3.jpg': 'f7064521c932b0a534d8b958bc79901f',
                'photo4.jpg': 'f0688d400a6c7207c79400685d969ef9',
                'photo5.jpg': '8dd8067ffff25e33af3a95c17d1a4959'
            }),
            ([], {
                'photo1.jpg': '679c1fe27ea9d614d70ff7c74dcf740d',
                'photo2.jpg': 'b488f6de4f7389fddee9342864397060',
                'photo3.jpg': '95a959b982c2750d922fce264233e5f4',
                'photo4.jpg': 'f944b4a89ccce331a3f40b3898a148d0',
                'photo5.jpg': '91af45c5bb93366761906e6ad45f127e'
            }),
        )

    @unittest_dataprovider.data_provider(
        provider_filesystem_uploader
    )
    def test_last_photos_picker_filesystem_uploader(
            self,
            filters,
            expected_files
    ):
        """
        Test with LastPhotosPicker and FilesystemUploader

        :param array filters: filters to use
        :param dict expected_files: expected files with hash of their content
        """
        picker = LastPhotosPicker(self.sample_dir, 5, -1)
        uploader = FilesystemUploader(self.target_dir)

        photo_picker = PhotosPicker(picker, filters, uploader)
        photo_picker.run()

        actual_files = {}
        for filename in os.listdir(self.target_dir):
            fullpath = self.target_dir + '/' + filename
            md5 = self._compute_file_md5(fullpath)
            actual_files[filename] = md5
            os.remove(fullpath)

        self.assertEqual(expected_files, actual_files)

    @staticmethod
    def provider_web_uploaders():
        """
        Dataprovider for web uploaders

        :return: tuple
        """
        return (
            ([ResizeFilter(100, 100), RotateFilter()], {
                'photo1.jpg': '9f8bb12a840adc598c9257f0309fd04b',
                'photo2.jpg': '615a8cd4f1ead919dbe268a4d0526263',
                'photo3.jpg': '4955a9411b47113c07a3d9767ba67955',
                'photo4.jpg': '7517ea032f3bab1ecab4006a5e6dbe9b',
                'photo5.jpg': '25ca68bc469e3e63eddf38be7fbaaeed'
            }),
        )

    @unittest_dataprovider.data_provider(
        provider_web_uploaders
    )
    def test_last_photos_picker_dropbox_uploader(
            self,
            filters,
            expected_files
    ):
        """
        Test with LastPhotosPicker and DropboxUploader

        :param array filters: filters to use
        :param dict expected_files: expected files with hash of their content
        """
        if 'DROPBOX_TOKEN' not in os.environ.keys():
            raise SkipTest("DROPBOX_TOKEN environment variable is not defined")

        api_token = os.environ['DROPBOX_TOKEN']

        picker = LastPhotosPicker(self.sample_dir, 5, -1)
        uploader = DropboxUploader(api_token, self.remote_test_dir)

        photo_picker = PhotosPicker(picker, filters, uploader)
        photo_picker.run()

        dbx = Dropbox(api_token)

        test_dir = '/' + self.remote_test_dir
        files = dbx.files_list_folder(test_dir)
        actual_files = {}
        for file_metadata in files.entries:
            fullpath = self.target_dir + '/' + file_metadata.name
            dbx.files_download_to_file(
                fullpath,
                test_dir + '/' + file_metadata.name
            )
            md5 = self._compute_file_md5(fullpath)
            actual_files[file_metadata.name] = md5
            os.remove(fullpath)

        self.assertEqual(expected_files, actual_files)

    @unittest_dataprovider.data_provider(
        provider_web_uploaders
    )
    def test_last_photos_picker_gdrive_uploader(
            self,
            filters,
            expected_files
    ):
        """
        Test with LastPhotosPicker and GDriveUploader

        :param array filters: filters to use
        :param dict expected_files: expected files with hash of their content
        """
        if not os.path.isfile(self.gdrive_creds_filepath):
            txt = "mycreds.json file is missing"
            raise SkipTest(txt)

        gauth = self.create_gdrive_auth()
        picker = LastPhotosPicker(self.sample_dir, 5, -1)
        uploader = GDriveUploader(gauth, self.remote_test_dir)

        photo_picker = PhotosPicker(picker, filters, uploader)
        photo_picker.run()

        gdrive = GoogleDrive(gauth)

        query = "mimeType = 'application/vnd.google-apps.folder'" \
                + " and title = '{dir}' and trashed=false"
        query = query.format(dir=self.remote_test_dir)
        folders = gdrive.ListFile({"q": query}).GetList()

        self.assertEqual(1, len(folders))

        query = "'{folder_id}' in parents and trashed=false"
        files = gdrive.ListFile(
            {"q": query.format(folder_id=folders[0]['id'])}
        ).GetList()
        actual_files = {}
        for file_metadata in files:
            gd_file = gdrive.CreateFile({'id': file_metadata['id']})
            fullpath = self.target_dir + '/' + file_metadata['title']
            gd_file.GetContentFile(fullpath)
            md5 = self._compute_file_md5(fullpath)
            actual_files[file_metadata['title']] = md5
            os.remove(fullpath)

        self.assertEqual(expected_files, actual_files)

    def _compute_file_md5(self, filepath):
        """
        Compute md5 hash of a file content

        :param string filepath: full path of the file

        :return: string
        """
        with open(filepath, 'r') as content_file:
            content = content_file.read()
        md5 = hashlib.md5(content)
        return md5.hexdigest()

    @classmethod
    def create_gdrive_auth(cls):
        """
        Create an Oauth instance for Google Drive

        :return: GoogleAuth
        """
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(cls.gdrive_creds_filepath)
        if gauth.credentials is None:
            # See https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process
            # For generating correct credentials
            raise SkipTest("Wrong credentials in mycreds.json")
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        return gauth

    @classmethod
    def tearDown(cls):
        # Clear local test files
        subprocess.call(['rm', '-rf', cls.target_dir])

    @classmethod
    def tearDownClass(cls):
        # Clear sample files for tests
        subprocess.call(['rm', '-rf', cls.sample_dir])

        # Clear Dropbox test files
        if 'DROPBOX_TOKEN' in os.environ.keys():
            dbx = Dropbox(os.environ['DROPBOX_TOKEN'])
            try:
                dbx.files_delete_v2('/' + cls.remote_test_dir)
            except ApiError as e:
                if not isinstance(e.error, DeleteError) \
                        or not e.error.is_path_lookup():
                    raise e

        # Clear Google Drive test files
        if os.path.isfile(cls.gdrive_creds_filepath):
            gauth = cls.create_gdrive_auth()
            gdrive = GoogleDrive(gauth)
            query = "mimeType = 'application/vnd.google-apps.folder'" \
                    + " and title = '{dir}' and trashed=false"
            query = query.format(dir=cls.remote_test_dir)
            folders = gdrive.ListFile({"q": query}).GetList()

            if len(folders) == 1:
                folder = folders[0]
                query = "'{folder_id}' in parents and trashed=false"
                files = gdrive.ListFile(
                    {"q": query.format(folder_id=folder['id'])}
                ).GetList()
                for file_to_delete in files:
                    file_to_delete.Delete()