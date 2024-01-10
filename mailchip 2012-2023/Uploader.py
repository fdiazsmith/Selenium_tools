from google_uploader import upload_image_file, upload_html_file, service_account_login
import csv
import os

service = service_account_login()

DATABASE_CSV = "campains/campaigns.csv"

# Read the campaigns from the csv file
campaigns = []
with open(DATABASE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] == "Sent":
            filename = row["filename"]

            print("NAME: ", filename)
        
            row["g_drive_id_html"] =  f"https://drive.google.com/file/d/{upload_image_file(service, filename + '.html', './campains/'+ filename + '.html', mimetype='text/html')}/view?usp=drive_link"
            row["g_drive_id_png"] =  f"https://drive.google.com/file/d/{upload_image_file(service, filename + '.png', './campains/'+ filename + '.png', mimetype='image/png')}/view?usp=drive_link"   
            campaigns.append(row) 

# write a new csv file with the new data
with open('campains/_campaigns.csv', 'w', newline='',  encoding='utf-8') as csvfile:
    # Get the fieldnames from the first campaign (assuming all campaigns have the same keys)
    fieldnames = campaigns[0].keys()

    # Create a DictWriter instance
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the campaigns
    for campaign in campaigns:
        writer.writerow(campaign)