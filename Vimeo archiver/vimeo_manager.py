import vimeo
import csv
import requests
import os
import shutil

dbfilename = 'vimeo_video_archive.csv'
vimeo_token = '2230e3eb538f1fb20d4b78a9707d5ab1'
vimeo_key = 'f24e0b4eac01dccd43c662e4384cbb82dfc4b352'
vimeo_secret = 'CWlAmhSguJusPRGHJX59L0hXrLWiIf4BPQVIzKqEXUPyBRjLp3wokje7d2KLEhogpUiOw5jO5k4hEM0SvuSfYe4MUyRshCT003xIkJkX/KXz6VKAW2COpEV82sLTCLsg'
client = vimeo.VimeoClient( token=vimeo_token, key=vimeo_key,secret=vimeo_secret)


def get_all_videos():
	response = client.get('https://api.vimeo.com/me/videos')
	return response

def get_video_url(video):
	for source in video['download']:
		if source['quality'] == 'source':
			print("source found")
			return source['link']
	# If 'source' quality is not found, look for 'hd' quality and '1080p' rendition
	for source in video['download']:
		if source['quality'] == 'hd' and source['rendition'] == '1080p':
			print("hd 1080p found")
			return source['link']
	for source in video['download']:
		if source['quality'] == 'hd' :
			print("hd found")
			return source['link']
	for source in video['download']:
		print("found?? ", source['quality'])
		return source['link']
	
	
		
def sanitize_filename(name):
    invalid_chars = "<>:\"/\\|?*"
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

def download_file(data, destination_folder):
	url = get_video_url(data)
	name = sanitize_filename(data['name'])
	print(f"Downloading {name}...{url}")
	if url is None:
		print("No download links found")
		# create a dummy file
		with open(f'{destination_folder}/{name}.mp4', 'w') as file:
			file.write('No download links found')
		return
	# Send a GET request to the URL
	with requests.get(url, headers={'Authorization': f'Bearer {vimeo_token}'}, stream=True) as response:
		response.raise_for_status()  # Raise an exception for HTTP errors

		# Get the total file size from the headers (if available)
		total_length = response.headers.get('content-length')
		if total_length is not None:
			total_length = int(total_length)

		# Initialize the variables for tracking download progress
		downloaded = 0
		print(f"Downloading {name}...")
		# Open the destination file in binary write mode
		with open(f'{destination_folder}/{name}', 'wb') as file:
			for chunk in response.iter_content(chunk_size=8192): 
				# Write the chunk to the file
				if chunk:
					file.write(chunk)
					downloaded += len(chunk)

					# Print the progress
					if total_length is not None:
						done = int(50 * downloaded / total_length)
						progress = f"\r[{'=' * done}{' ' * (50-done)}] {downloaded * 100 / total_length:.2f}%"
						print(progress, end='')

	print(f"\nFile downloaded and saved as {f'{destination_folder}/{name}'}")

def delete_folder_contents(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def save_row(video):
	with open(dbfilename, 'a', newline='') as csvfile:
		fieldnames = ['name', 'description', 'link', 'created_time', 'available_albums', 'tags', 'albums', 'available_album_name', 'available_album_description', 'album_name', 'album_description', 'uri', 'url_source', 'google_drive_id']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		# Extract 'available_albums', 'tags', 'albums'
		available_albums = video['metadata']['connections']['available_albums']['total']
		available_album_name = []
		available_album_description = []
		uri = video['uri']
		url_source = get_video_url(video)
		google_drive_id =  video['google_drive_id']

		if available_albums > 0:
			album_url = video['metadata']['connections']['available_albums']['uri']
			album_response = client.get(album_url)
			album_data = album_response.json()['data']
			for album in album_data:
				available_album_name.append(album['name'])
				available_album_description.append(album['description'])
		
		tags = [tag['name'] for tag in video.get('tags', [])]  # List of tag names
		albums = video['metadata']['connections']['albums']['total']
		album_name = []
		album_description = []
		if albums > 0:
			album_url = video['metadata']['connections']['albums']['uri']
			album_response = client.get(album_url)
			album_data = album_response.json()['data']
			for album in album_data:
				album_name.append(album['name'])
				album_description.append(album['description'])

		row = {
			'name': video['name'], 
			'description': video['description'], 
			'link': video['link'], 
			'created_time': video['created_time'],
			'available_albums': available_albums,
			'tags': ', '.join(tags),  # Join tags by comma
			'albums': albums,
			'available_album_name': available_album_name,
			'available_album_description': available_album_description,
			'album_name': album_name,
			'album_description': album_description, 
			'uri': uri,
			'url_source': url_source, 
			'google_drive_id': google_drive_id
		}
		print(row)
		writer.writerow(row)

def iterate_all_videos():
	with open(dbfilename, 'w', newline='') as csvfile:
		fieldnames = ['name', 'description', 'link', 'created_time', 'available_albums', 'tags', 'albums', 'available_album_name', 'available_album_description', 'album_name', 'album_description', 'uri', 'url_source', 'google_drive_id']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		response = get_all_videos()
		data = response.json()['data']
		next_page = response.json()['paging']['next']

		for video in data:
			save_row(video, writer)
		# while next_page:
		# 	response = client.get(next_page)
		# 	data = response.json()['data']
		# 	next_page = response.json()['paging']['next']
		# 	for video in data:
		# 		save_row(video, writer)

def create_db(dbfilename):
	if not os.path.exists(dbfilename):
		with open(dbfilename, 'w', newline='') as csvfile:
			fieldnames = ['name', 'description', 'link', 'created_time', 'available_albums', 'tags', 'albums', 'available_album_name', 'available_album_description', 'album_name', 'album_description', 'uri', 'url_source', 'google_drive_id']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			print(f'Created {dbfilename}')
	else:
		print(f'{dbfilename} already exists')

# get lastest video data
def get_lastest_video(url):
	response = client.get(url)
	data = response.json()['data']
	#  while check_if_data_exist(data[0]) === True: keep looking for new video
	if check_if_data_exist(data[0]) == False:
		print('New video found', response.json()['paging']['next'])
		return data[0]
	else:
		next_page = response.json()['paging']['next']
		print('No new video found', next_page)
		return get_lastest_video(next_page)

def check_if_data_exist(video):
	with open(dbfilename, 'r', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['uri'] == video['uri']:
				return True
	return False



# create_db(dbfilename)
# vid_data = get_lastest_video('https://api.vimeo.com/me/videos?per_page=1')
# save_row(vid_data)
# iterate_all_videos()
