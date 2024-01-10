import vimeo
import csv
import requests

dbfilename = 'videos.csv'

client = vimeo.VimeoClient(
	token='2230e3eb538f1fb20d4b78a9707d5ab1',
	key='f24e0b4eac01dccd43c662e4384cbb82dfc4b352',
	secret='CWlAmhSguJusPRGHJX59L0hXrLWiIf4BPQVIzKqEXUPyBRjLp3wokje7d2KLEhogpUiOw5jO5k4hEM0SvuSfYe4MUyRshCT003xIkJkX/KXz6VKAW2COpEV82sLTCLsg'
)


def get_all_videos():
	response = client.get('https://api.vimeo.com/me/videos')
	return response

def dowload_video(url):
	
	# Send a GET request to the video URL
	response = requests.get(url, stream=True)

	# Check if the request was successful
	if response.status_code == 200:
		# Open a file for writing in binary mode
		with open(file_path, 'wb') as file:
			# Write the video content to the file
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:  # filter out keep-alive new chunks
					file.write(chunk)
		print(f"Video downloaded successfully and saved as '{file_path}'")
	else:
		print("Failed to download the video.")


def save_row(video, writer):
	# Extract 'available_albums', 'tags', 'albums'
	available_albums = video['metadata']['connections']['available_albums']['total']
	available_album_name = []
	available_album_description = []
	uri = video['uri']
	url_source =''
	for source in video['download']:
		if source['quality'] == 'source':
			url_source = source['link']
			break

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
		'url_source': url_source
	}
	print(row)
	writer.writerow(row)

def iterate_all_videos():
	with open(dbfilename, 'w', newline='') as csvfile:
		fieldnames = ['name', 'description', 'link', 'created_time', 'available_albums', 'tags', 'albums', 'available_album_name', 'available_album_description', 'album_name', 'album_description', 'uri', 'url_source']
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

iterate_all_videos()

# iterate_all_videos()
