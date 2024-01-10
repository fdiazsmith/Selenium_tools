from google_upload import service_account_login, upload_file_to_shared_drive, upload_large_file
from vimeo_manager import create_db, get_lastest_video, save_row, download_file, delete_folder_contents, sanitize_filename

dbfilename = 'vimeo_video_archive.csv'

# get gogle service
service = service_account_login()
create_db(dbfilename)
# get latest video from vimeo
vid_data = get_lastest_video('https://api.vimeo.com/me/videos?per_page=1&page=85')

while vid_data:
    # download video from vimeo
    download_file(vid_data, 'temp')

    # upload video to google drive
    filename = f'{sanitize_filename(vid_data["name"])}'  # Name of the file to upload
    filepath = f'temp/{sanitize_filename(vid_data["name"])}'  # Path to the large file
    mimetype = 'video/mp4'  # MIME type of the file

    vid_data['google_drive_id'] = f'https://drive.google.com/file/d/{upload_large_file(service, filename, filepath, mimetype)}/view?usp=drive_link'

    # update database
    save_row(vid_data)
    delete_folder_contents('temp')

    # repeat
    vid_data = get_lastest_video('https://api.vimeo.com/me/videos?per_page=1&page=85')
