# master
* Update usage examples: only catch photospicker AbstractException for displaying exception message
* Add CHANGELOG.md
* Add SmartPicker
* Take care that photos to retrieve count is not greater than total photos count (at AbstractPicker level)

# 0.3.1
* Allow to use a custom target directory in Dropbox
* Allow to use a custom target directory in Google Drive

# 0.3.0
* Rename Dropbox photos directory as photos-picker
* Add Google Drive uploader

# 0.2.1
* Add try except in examples
* Rename PickerException to UploaderException
* Raise exception when no file to scan
* Remove requirements-dev.txt
* Improve tests
* Use excluded patterns instead of excluded paths
* Fix crash when image format provide no exif data

# 0.1.2
* Make build don't fail anymore if dist content is empty
* Use bdist_wheel for building
* Add dependencies to setup.py
* Don't include tests in packages

# 0.1.1
* Add rotate filter to documentation

# 0.1.0
* Add rotate filter

# 0.0.1
* Initial release