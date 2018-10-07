# Uploaders

## FilesystemUploader

### Utility
Copy the photos to a given directory. This directory must exist and be empty.

### Constructor arguments
```python
def __init__(self, folder_path)
```
* `folder_path` (string): path where the photos will be copie

## DropboxUploader

### Utility
Upload the photos to Dropbox. ***Be careful, the script empty the `/photos` directory, you must limit your token access to application for avoiding unwanted deletions***.

### Constructor arguments
```python
def __init__(self, api_token)
```
* `api_token` (string): authorization token from Dropbox for accessing API