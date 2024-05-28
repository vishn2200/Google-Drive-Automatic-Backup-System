from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from kubernetes import client, config
import os
import os.path
import logging


logging.basicConfig(filename='backup.log', level=logging.INFO)
def backup_data():
    # Perform backup operation
    logging.info('Backup operation started...')
    # Your backup logic here
    logging.info('Backup operation completed successfully.')


SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Authenticate the user and return the service."""
    creds = None
    # Check for existing saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing access token: {e}")
                creds = None
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)  # Ensure this is the correct path to your client secret file
                creds = flow.run_local_server(port=8080)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Failed to retrieve new token: {e}")
                exit(1)
    service = build('drive', 'v3', credentials=creds)
    return service


def upload_file(service, file_path, file_name, mime_type, parent_folder_id=None):
    """Uploads a file to Google Drive."""
    try:
        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File ID: {file.get('id')}")
    except Exception as e:
        print(f"Failed to upload file: {e}")

def upload_folder(service, folder_path, parent_folder_id=None):
    """Uploads a folder and its contents to Google Drive."""
    print("Folders will upload now...")
    try:
        folder_name = os.path.basename(folder_path)
        folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Folder ID: {folder.get('id')}")


        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                upload_file(service, item_path, item, mime_type='application/octet-stream', parent_folder_id=folder['id'])
            elif os.path.isdir(item_path):
                upload_folder(service, item_path, parent_folder_id=folder['id'])
    except Exception as e:
        print(f"Failed to upload folder: {e}")


def main():
    service = authenticate()
    backup_data()
    upload_folder(service, 'tocopy')

if __name__ == '__main__':
    main()