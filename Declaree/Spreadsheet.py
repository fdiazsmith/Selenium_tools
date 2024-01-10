import os
import csv

class Spreadsheet:
    def __init__(self, filename):
        self.filename = None
        self.path = None
        self.headers = ['date', 'amount', 'currency', 'category', 'description']
        self.create_file(filename)

    def update_and_save_headers(self, new_headers):
        # Temporary storage for updated rows
        updated_rows = []

        # Read the current data and update the rows
        with open(self.path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Update each row to match new headers
                updated_row = {header: row.get(header, '') for header in new_headers}
                updated_rows.append(updated_row)

        # Update headers
        self.headers = new_headers

        # Write the updated data back to the file
        with open(self.path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(updated_rows)

    def create_directory(self):
        if not os.path.exists('export'):
            os.mkdir('export')

    def create_file(self, filename):
        self.filename = f'{filename}.csv'
        self.path = f'export/{self.filename}'

        if not self.file_exists():
            self.create_directory()
            self.write_initial_file()

    def file_exists(self):
        return os.path.exists(self.path)

    def write_initial_file(self):
        with open(self.path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()

    def add_row(self, row):
        with open(self.path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(row)
