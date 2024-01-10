from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

from googleapiclient.discovery import build
import os

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/drive']

def service_account_login():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret_972796584910-lq1gu7ieunjqae1scop0emp1k7l608cq.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('drive', 'v3', credentials=creds)

def upload_file_to_shared_drive(filename, filepath, mimetype, folder_id, drive_id):
    service = service_account_login()
    file_metadata = {
        'name': filename,
        'parents': ['18TS06f7iQa_7IOODL-JSYvjB6kEdWPlS'],
        'driveId': '0ABBWaPbHUe2MUk9PVA',
        'corpora': 'drive',
        'includeItemsFromAllDrives': True,
        'supportsAllDrives': True
    }
    media = MediaIoBaseUpload(open(filepath, 'rb'), mimetype=mimetype)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()

    print(f"File ID: {file.get('id')}")


def upload_large_file(service,filename, filepath, mimetype):

    file_metadata = {
        'name': filename,
        'parents': ['18TS06f7iQa_7IOODL-JSYvjB6kEdWPlS'],
        'driveId': '0ABBWaPbHUe2MUk9PVA',
    }
    
    try:
        # Use MediaFileUpload with resumable=True for large files
        media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)
    except Exception as e: 
        print(f"Failed to upload {filepath}. Reason: {e}")
        return "None"
    
    file = service.files().create(
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
   

def upload_image_file(service, filename, filepath, mimetype='image/png'):
    file_metadata = {
        'name': filename,
        'parents': ['18TS06f7iQa_7IOODL-JSYvjB6kEdWPlS'],
        'driveId': '0ABBWaPbHUe2MUk9PVA',
    }

    media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)

    file = service.files().create(
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

def upload_html_file(service, filename, filepath, mimetype='text/html'):
    file_metadata = {
        'name': filename,
        'parents': ['18TS06f7iQa_7IOODL-JSYvjB6kEdWPlS'],
        'driveId': '0ABBWaPbHUe2MUk9PVA',
    }

    media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)

    file = service.files().create(
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

# Example usage
filename = 'video_from_vimeo.mp4.mp4'  # Name of the file to upload
filepath = 'video_from_vimeo.mp4'  # Path to the large file
mimetype = 'video/mp4'  # MIME type of the file

# service = service_account_login()
# upload_large_file(service, filename, filepath, mimetype)
