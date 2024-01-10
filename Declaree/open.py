from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
# from PIL import Image
import io
import os

# Define the URL and the different resolutions
url = 'https://app.declaree.com/'

def create_temp_dir():
    if not os.path.exists('temp'):
        os.mkdir('temp')
        # return full path of the directory created
        return os.path.abspath('temp')
    else:
        # return full path of the directory already created
        return os.path.abspath('temp')


def start_session():
    tempdir = create_temp_dir()
    print("tempdir: ",tempdir)
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    chrome_options.add_experimental_option('prefs', {
    "download.default_directory": tempdir, # Change default directory for downloads
    "download.prompt_for_download": False, # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True, # It will not show PDF directly in chrome,
    "profile.default_content_setting_values.automatic_downloads": 1
    })
    chrome_options.add_experimental_option("detach", True)  # Add this line
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    # enable download in headless mode
    params = {'behavior': 'allow', 'downloadPath': tempdir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    
    return driver

if __name__ == '__main__':

    try:
        driver = start_session()
        print("executor url:   ",driver.command_executor._url)  # prints the executor URL
        print("session id:   ",driver.session_id)

        while True:
            time.sleep(10)  # wait for 10 seconds before checking again
    except KeyboardInterrupt:
        print("\nInterrupted by user. Closing driver...")
        driver.quit()