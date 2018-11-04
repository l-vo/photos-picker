# Uploaders

## FilesystemUploader

### Utility
Copy the photos to a given directory. This directory must exist and be empty.

### Constructor arguments
```python
def __init__(self, folder_path)
```
* `folder_path` (string): path where the photos will be copied

## DropboxUploader

### Utility
Upload the photos to Dropbox. ***Be careful, the script empty the `/photos-picker` directory (or the alternative directory you configured). You should limit your token access to application for avoiding unwanted deletions***.

### Constructor arguments
```python
def __init__(self, api_token, folder_name='photos-picker')
```
* `api_token` (string): authorization token from Dropbox for accessing API
* `folder_name` (string, optional): name of the folder in Dropbox

### Get a Dropbox api token
You can find home to generate your api token [here](https://www.dropbox.com/developers/reference/oauth-guide) in the Dropbox documentation.

## GDriveUploader

### Utility
Upload the photos to Google Drive. ***The script empty a directory named photos-picker. Take care that a directory with a such name doesn't already exist in the used drive account***.

### Constructor arguments
```python
def __init__(self, gauth, folder_name='photos-picker')
```
* `gauth` (pydrive.auth.GoogleAuth): authentified instance of GoogleAuth
* `folder_name` (string, optional): name of the folder in Google Drive

### GoogleAuth authentication
This library uses pyDrive for dealing with Google Drive API. For allowing your application to use Google Drive API, you must create a `client_secrets.json` credential file at the root of your application. How to get this file is well documented here: [pyDrive quickstart](https://pythonhosted.org/PyDrive/quickstart.html).

Once your application is authenticated, It will be asked to your application end-user to give access to its drive to your application. It's your application resonsability to memorize the authorization of your end-user. Otherwise, the authorization will be asked at each time. Here is an example :
```python
from pydrive.auth import GoogleAuth
from photospicker.uploader.gdrive_uploader import GDriveUploader

# Example from https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

uploader = GDriveUploader(gauth)
```