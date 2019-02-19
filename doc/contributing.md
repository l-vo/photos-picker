# Contributing
When you submit a pull request, a CI will process some to checks:
- That the code is conform with the PEP8 standard
- That the unit tests are not broken
- That the functional tests are not broken

For running these checks locally, you should have installed:
- [pip](https://pip.pypa.io/en/stable/installing/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Tox](https://tox.readthedocs.io/)

Especially for functional tests are required:
- a [Dropbox token](https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/)
- a [Google Drive credential file](https://pythonhosted.org/PyDrive/quickstart.html#authentication) (`mycreds.json` at the root of the project)

If all these requirements are ok, the following command process locally at the same checks as the CI:
```bash
$ DROPBOX_TOKEN=mydropboxtoken make validate
```
 
If you don't have a Dropbox token or a Google Drive credential file, you can however locally check the code standards and launch the unit tests:
```bash
$ make dev
$ make lint
$ make test-unit
```