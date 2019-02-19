# Contributing
When you submit a pull request, a CI will process to some checks:
- That the code is conform to the PEP8 standard
- That the unit tests are not broken
- That the functional tests are not broken

These tests are done in all Python versions supported by this library.

For running these checks locally, you should have installed:
- [pip](https://pip.pypa.io/en/stable/installing/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Tox](https://tox.readthedocs.io/)
- all the Python versions supported by photos-picker. If you don't have this, you can use my [docker container](https://hub.docker.com/r/lvo9/python-virtualenv)

Especially for functional tests are required:
- a [Dropbox token](https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/)
- a [Google Drive credential file](https://pythonhosted.org/PyDrive/quickstart.html#authentication) (`mycreds.json` at the root of the project)

If all these requirements are ok, the following command process locally at the same checks as the CI:
```bash
$ DROPBOX_TOKEN=mydropboxtoken tox
```
 
If you don't have a Dropbox token or a Google Drive credential file, you can however locally check the code standards and launch the unit tests:
```bash
$ make dev
$ make lint
$ make test-unit
```
You should run these tests in all Python versions supported by the library.

Functional tests download sample images in the repository [ianare/exif-samples](https://github.com/ianare/exif-samples). This repository size is about 31M but is downloaded once in your `/tmp` directory or in the path defined in `TMPDIR` environment variable if defined. Note for preventing multiple heavy downloads, the image archive is never deleted. If you want to delete it:
```bash
$ make clear-tmp
```
Anyway, if you need it again, it will be downloaded the next time you'll launch functional tests.
