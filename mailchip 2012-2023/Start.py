from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from PIL import Image
import io

# Define the URL and the different resolutions
url = 'http://localhost:8000/'



def start_session():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    chrome_options.add_experimental_option("detach", True)  # Add this line
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


try:
    driver = start_session()
    print("executor url:   ",driver.command_executor._url)  # prints the executor URL
    print("session id:   ",driver.session_id)

    while True:
        time.sleep(10)  # wait for 10 seconds before checking again
except KeyboardInterrupt:
    print("\nInterrupted by user. Closing driver...")
    driver.quit()