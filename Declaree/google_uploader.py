from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

from googleapiclient.discovery import build
import os

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/drive']

class Driveuploader:
    def __init__(self,cleint_secret):
        # flow = InstalledAppFlow.from_client_secrets_file('client_secret_972796584910-lq1gu7ieunjqae1scop0emp1k7l608cq.apps.googleusercontent.com.json', SCOPES)
        flow = InstalledAppFlow.from_client_secrets_file(cleint_secret, SCOPES)
        creds = flow.run_local_server(port=0)
        self.service = build('drive', 'v3', credentials=creds)
        # self.service = service_account_login()
        self.file_id = None
        self.folder_id = None

    def set_folder_id(self, folder_id):
        self.folder_id = folder_id


    
    def get_file_id(self):
        return self.file_id
    def get_file_url(self):
        return f"https://drive.google.com/file/d/{self.file_id}/view?usp=drive_link"
    
    def upload_large_file(self, filename, filepath, mimetype):

        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        try:
            # Use MediaFileUpload with resumable=True for large files
            media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)
        except Exception as e: 
            print(f"Failed to upload {filepath}. Reason: {e}")
            return "None"
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        )

        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
        if response:
            print(f"File ID: {response.get('id')}")
            return response.get('id')
        else:
            print("Failed to upload the file.")
            return None
   

    def upload_file(self,  filename, filepath, mimetype):
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id],
        }

        media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        )

        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
        if response:
            print(f"File ID: {response.get('id')}")
            return response.get('id')
        else:
            print("Failed to upload the file.")
            return None


