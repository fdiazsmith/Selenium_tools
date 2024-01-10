from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import sys
import os
from urllib.parse import urlparse
import Spreadsheet
import time
from file_manager import Tempdir
from google_uploader import Driveuploader


# Constants
TEMP_DIR = 'temp'
GOOGLE_CLIENT_SECRET = 'client_secret_972796584910-lq1gu7ieunjqae1scop0emp1k7l608cq.apps.googleusercontent.com.json'
GOOGLE_FOLDER_ID = "1kBlV6sIbFEtct8JnA3POt0wQG38Rv6XZ"

tempdir = Tempdir('temp')

def attach_to_session(executor_url, session_id):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    original_function = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'status': 0, 'value': {'sessionId': session_id, 'capabilities': {}}}
        else:
            return original_function(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    options = webdriver.ChromeOptions()
    new_driver = webdriver.Remote(command_executor=executor_url, options=options)
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = original_function

    return new_driver

class Exporter:
    def __init__(self, driver):
        self.driver = driver
        self.sp = Spreadsheet.Spreadsheet("expenses")
        self.drive = None 
        self.tempdir = Tempdir('temp')
        print("Exporter init")

    def get_header_by_index(self, header, index):
        for i, h in enumerate(header):
            if h['index'] == index:
                return h

    def extract_headers(self):
        headers_xpath = "//table[contains(@class, 'table-expenses')]//th"
        return self.driver.find_elements(By.XPATH, headers_xpath)

    def format_header(self, header_element, index):
        if "hide" in header_element.get_attribute('class'):
            return None
        return {
            'text': header_element.text,
            'index': index,
            'class': header_element.get_attribute('class'),
            'hname': header_element.text if header_element.text else f"_{header_element.get_attribute('class').split(' ')[0]}" 
        }

    def get_table_headers(self):
        table_headers = self.extract_headers()
        formatted_headers = [self.format_header(header,i) for i, header in enumerate(table_headers)]
        filtered_headers = [header for header in formatted_headers if header is not None]

        self.sp.update_and_save_headers([h['hname'] for h in filtered_headers])
        return filtered_headers
    
    def wait_for_download_to_complete(self, filepath, timeout=30):
        """
        Wait for the file at the given filepath to finish downloading.

        Parameters:
        - filepath: The full path of the file.
        - timeout: The maximum time to wait, in seconds.
        """
        # Wait for the .crdownload file to disappear
        start_time = time.time()
        print("waiting for download to complete", filepath, end="\t")
        while os.path.exists(filepath + '.crdownload'):
            print("waiting for download to complete")
            if time.time() - start_time > timeout:
                raise Exception(f"Timeout reached while waiting for file {filepath} to finish downloading")
            time.sleep(1)
        time.sleep(2)
        print("download completed" , end="\t")

    def upload_file(self, row, i):
        print(f"{row['_cselect']}: status file {i}", end="\t")
        rename_file = f"{row['_cselect']}_receipt_{i}"
        files = tempdir.list_files()
        file = files[0] 
        print("file: ",file , end="\t")
        self.wait_for_download_to_complete(tempdir.get_full_path(files[0]))
        files = tempdir.list_files()
        file = files[0] 
        # time.sleep(1)
        tempdir.rename_file(file,rename_file)
        files = tempdir.list_files()
        file = files[0] 
        mimetype = tempdir.get_file_mime_type(files[0]) 
        filepath = tempdir.get_full_path(files[0])

        return f"https://drive.google.com/file/d/{self.drive.upload_file( file, filepath, mimetype=mimetype)}/view?usp=drive_link"
        
    def download_img_from_tab(self, row, i):
        time.sleep(1)
        # get src from the img tag
        src = self.driver.find_element(By.TAG_NAME, "img").get_attribute('src')
        # Parse the URL
        parsed_url = urlparse(src)
        # Get the path part of the URL
        path = parsed_url.path

        # Get the extension (without the dot)
        extension = os.path.splitext(path)[1][1:]
        os.system(f"curl -o {tempdir.path}/{row['_cselect']}_receipt_{i}.{extension} {src}")
        
        

        

        # Close the new tab
        self.driver.close()

    def get_all_files(self, row):
        time.sleep(2)
        links = []
        links_xpath = '//*[@id="files"]//*[contains(@class, "item file")]'
        # links_xpath = '//*[@id="files"]//img'
        links_btn = self.driver.find_elements(By.XPATH, links_xpath)
        # print the length of the links_btn
        # print()
        print(f"\n \n {row['_cselect']} : Receipts", len(links_btn))
        
        for i, link in enumerate(links_btn):
            time.sleep(1)
            
            xpath_download = '//*[@id="expense-body"]/div/div/div[2]/div[3]/div/a[2]'
            download_btn = self.driver.find_element(By.XPATH, xpath_download)
        
            self.driver.execute_script("arguments[0].scrollIntoView();", download_btn)
            download_btn.click()

            # Wait for the new tab to open
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.number_of_windows_to_be(2))

            # Switch to the new tab
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                self.download_img_from_tab(row, i)
            except:
                # print("pdf")
                pass
            finally:
                # Close the driver
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                # Switch back to the original window
                self.driver.switch_to.window(self.driver.window_handles[0])
            links.append( self.upload_file(row, i) )
            tempdir.delete_all_files()
            
            try:
                xpath_next = '//*[@id="expense-body"]/div/div/div[2]/div[3]/div/div[2]/a[2]'
                next_btn = self.driver.find_element(By.XPATH, xpath_next)
                next_btn.click()
            except:
                print("no more files, or only one")
        return links
    
    def print_row(self, row):
        print(f"{row['_cselect']} \t {row['Date']} \t {row['Amount']}  \t {row['Category']} \t {row['Description']} \n\n\n")
        
    def print_header(self, header):
        print(f"\n\n\n {header['hname']} \n\n\n")

    def get_receipts(self, h, row):
        modalpath = './/a[@data-toggle="remote-modal"][1]'
        modal = h.find_element(By.XPATH, modalpath)
        
        self.driver.execute_script("arguments[0].scrollIntoView();", modal )
        
        # modal.click()
        self.driver.execute_script("arguments[0].click();", modal)
        
        # Wait for the modal to be visible
        xpath_modal = '//*[@id="remote-modal"]'
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_modal)))

        time.sleep(3)
        # get all the files and join them with |
        row['_caffix'] = " | ".join( self.get_all_files(row) )

        # close the modal
        xpath_close = '//*[@id="remote-modal"]/div/a'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_close)))
        close_btn = self.driver.find_element(By.XPATH, xpath_close)
        close_btn.click()


    def get_table_rows(self,  headers, start_index=0):
        # Find elements by tag name
        xpath = "//table[contains(@class, 'table-expenses')]//tr[contains(@class, 'record')]"
        table_rows = self.driver.find_elements(By.XPATH, xpath)
        tr = []
        indexes = [h['index'] for h in headers]
        

        for i_r, h in enumerate(table_rows):
            if i_r <= start_index:
                continue
            # from table_row only keep the indexes listesd in indexes
            table_cells = h.find_elements(By.TAG_NAME, "td")
            
            # table_row_c = [cell for i, cell in enumerate(table_cells) if i in indexes]
            row = {}
            
            for i_c, hc in enumerate(table_cells):
                hname = self.get_header_by_index(headers,i_c)
                if hname is None:
                    continue
                
                row[hname['hname']] = hc.text
                
                # print(row[hname['hname']] ,"\tXXXXX\t", hc.text)
            row['_cselect'] = i_r        
            self.get_receipts(h,row)
            self.print_row(row)
            self.sp.add_row(row)
        # Return the elements
        return tr

    def log_in(self,  username, password):
        time.sleep(2)
        print("log_in", username, password)
        xpath_username = '//*[@id="username"]'
        xpath_password = '//*[@id="password"]'
        xpath_submit = '/html/body/div/div[2]/form/div[1]/div[6]/button'
        username_input = self.driver.find_element(By.XPATH, xpath_username)
        password_input = self.driver.find_element(By.XPATH, xpath_password)
        submit_btn = self.driver.find_element(By.XPATH, xpath_submit)
        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_btn.click()
        

    def zoom_out(self, steps=5):
        actions = ActionChains(self.driver)
        for _ in range(steps):
            actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()

    def zoom_default(self):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('0').key_up(Keys.CONTROL).perform()

        
    def get_data(self, last_uploaded_file=-1):
        start_index = 0
        if last_uploaded_file is not None:
            start_index = last_uploaded_file
        data = []
        headers = self.get_table_headers()
        rows = self.get_table_rows(headers, start_index)
        
        return 



    def sanitize_filename(self, filename):
        return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
"""
________________________
"""
def main():
    try:
        executor_url, session_id = sys.argv[1:3]
        last_uploaded_file = int(sys.argv[3]) if len(sys.argv) > 3 else -1

        print(f"Executor URL: {executor_url}")
        print(f"Session ID: {session_id}")

        driver = attach_to_session(executor_url, session_id)
        print(f"Attached to session. Current URL: {driver.current_url}")

        drive = Driveuploader(GOOGLE_CLIENT_SECRET)
        drive.set_folder_id(GOOGLE_FOLDER_ID)

        exporter = Exporter(driver)
        exporter.drive = drive
        exporter.get_data(last_uploaded_file)

        print("Processing completed successfully.")

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Exiting application.")

if __name__ == '__main__':
    main()
