import requests
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build

# Custom MediaIoBaseUpload class with progress reporting
class MediaIoBaseUploadWithProgress(MediaIoBaseUpload):
	def _next_chunk(self, http, num_retries=0):
		status, done = super(MediaIoBaseUploadWithProgress, self)._next_chunk(http, num_retries)
		if status:
			print(f"Uploaded {status.progress() * 100}%")
		return status, done
# Scopes required by the application
SCOPES = ['https://www.googleapis.com/auth/drive']





def main():
	# Perform OAuth 2.0 authorization flow
	flow = InstalledAppFlow.from_client_secrets_file('client_secret_972796584910-lq1gu7ieunjqae1scop0emp1k7l608cq.apps.googleusercontent.com.json', SCOPES)
	creds = flow.run_local_server(port=0)

	# Build the service object for Google Drive
	service = build('drive', 'v3', credentials=creds)

	# Folder ID in Google Drive where the file will be uploaded
	folder_id = '1D2tMC9K2pzjM4mF-AIhyHnWNMrakb3MK'

	# Vimeo video URL
	vimeo_video_url = 'https://player.vimeo.com/progressive_redirect/download/713210734/container/41d55b2b-3a30-45b7-b958-9add586ffa2d/19b76258/floriade_-_immersive_experience_-_vistors_-_2nd_cut%20%28Original%29.mp4?expires=1703095499&loc=external&oauth2_token_id=1753668412&signature=3ed6fdd900dbd7d01630b6967afd50c862aa4362607db01bcc67b0873847648d'
	vimeo_token = '2230e3eb538f1fb20d4b78a9707d5ab1'
	download_file(vimeo_video_url,vimeo_token, 'video_from_vimeo.mp4')
	# Stream the video from Vimeo
	# response = requests.get(vimeo_video_url, headers={'Authorization': f'Bearer {vimeo_token}'}, stream=True)
	# response.raise_for_status()
	# Wrap the stream in a BytesIO buffer
	# buffer = io.BytesIO(response.content)

	file_metadata = {
		'name': 'video_from_vimeo.mp4',  # Name of the file as it will appear in Drive
		'parents': [folder_id]  # Folder ID
	}

	# Upload the buffer to Google Drive
	# media = MediaIoBaseUpload(buffer, mimetype='video/mp4', resumable=True)
		# Create a MediaIoBaseUpload object with progress reporting
	media = MediaIoBaseUploadWithProgress(buffer, mimetype='video/mp4', resumable=True)

	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

	print('File ID: %s' % file.get('id'))





if __name__ == '__main__':
	main()
