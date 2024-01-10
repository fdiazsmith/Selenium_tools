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
import time
from PIL import Image
import sys
import io
import csv
# Define the URL and the different resolutions
url = 'http://localhost:8000/'



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

# Usage
if len(sys.argv) != 3:
    print("Usage: python script.py <executor_url> <session_id>")
    sys.exit(1)



def get_active_campaigns(driver):
    # Find elements by tag name
    e_xpath = '//li[contains(@class, "c-campaignManager_slat")]' 
    elements = driver.find_elements(By.XPATH, e_xpath)


    # Return the elements
    return elements



def get_links(driver):
    print("get_links")
    links = get_active_campaigns(driver)
    
    
    return links
def zoomout(driver):
    # Create an ActionChains instance
    actions = ActionChains(driver)

    # Send the zoom out shortcut
    actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
def zoom_defaul(driver):
     # Create an ActionChains instance
    actions = ActionChains(driver)

    # Send the control and zero 
    actions.key_down(Keys.CONTROL).send_keys('0').key_up(Keys.CONTROL).perform()
    
def get_info(driver):
    campaing_info = []
    active_campaign = get_active_campaigns(driver)
    for campaign in active_campaign:
        campaign_name = campaign.find_element(By.XPATH, './/h4').text
        campaign_status = campaign.find_element(By.XPATH, './/*[contains(@class, "c-campaignManager_slat_stat")][1]').text 
        try:
            campaign_opens_percent = campaign.find_element(By.XPATH, './/*[contains(@class, "c-campaignManager_slat_stat")][2]//*[contains(@class, "c-campaignManager_slat_stat_primary")]//p').text
            campaign_opens_count  = campaign.find_element(By.XPATH, './/*[contains(@class, "c-campaignManager_slat_stat")][2]//*[contains(@class, "c-campaignManager_slat_stat_secondary")]//p').get_attribute('innerHTML') 
            campaign_clicks_count = campaign.find_element(By.XPATH, './div[5]/div[2]/div[1]/p[1]').get_attribute('innerHTML')
            campaign_clicks_percent = campaign.find_element(By.XPATH, './div[5]/div[2]/div[2]/p[1]').get_attribute('innerHTML')
            campaign_link = campaign.find_element(By.XPATH, './div[3]/h4/a').get_attribute('href')
            
            # campaign_opens_count  = campaign.find_element(By.XPATH, './/*[contains(@class, "c-campaignManager_slat_stat")][2]//*[contains(@class, "c-campaignManager_slat_stat_secondary")]//p').text
        except:
            campaign_opens_percent = "-"
            campaign_opens_count = "-"
            campaign_clicks_count = "-"
            campaign_clicks_percent = "-"
            campaign_link = "-"
        
        # campaign_clicks = campaign.find_element(By.XPATH, './/c-campaignManager_slat_stat[2]//c-campaignManager_slat_stat_secondary//p[1]')
        c = {"name": campaign_name, 'filename': sanitize_filename(campaign_name), 'link':campaign_link,  "status": campaign_status, "campaign_opens_percent": campaign_opens_percent, "campaign_opens_count": campaign_opens_count, "campaign_clicks_count": campaign_clicks_count, "campaign_clicks_percent": campaign_clicks_percent}
        campaing_info.append(c)
        # print(campaign_opens_percent, campaign_opens_count,"click",  campaign_clicks_count, campaign_clicks_percent)
    return campaing_info



def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()


def get_screenshot(driver, data):
    print("get_screenshot", data)
    # Load the page
    driver.get(data['link'])

    # Wait for the page to fully load
    time.sleep(8)

    driver.switch_to.window(driver.window_handles[0])
    # find body tag
    # element_xpath = '//body'
    # element = driver.find_element(By.XPATH, element_xpath)
    # print("element", element)
    # #switch to ifra me
    driver.switch_to.frame("fallback")

    
   

    # Find the element by id
    element_xpath = '//iframe[@id="campaign-overview-html"]'
    element = driver.find_element(By.XPATH, element_xpath)
    zoomout(driver)
    time.sleep(2)
    height = driver.execute_script("return arguments[0].scrollHeight", element)
    #set the window size to the element size
    print("height", height)
    driver.set_window_size(1080, height)
    # Wait for the page to fully load
    time.sleep(2)
    # Take a screenshot of the element and save it to a file
    element.screenshot(f'campains/{data["filename"]}.png')
    zoom_defaul(driver)

    driver.switch_to.frame(element)
    print("element", element)
    # Get the outer HTML of the element
    html = driver.page_source #element.get_attribute('innerHTML')
    # Write the HTML to a file
    with open(f'campains/{data["filename"]}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    time.sleep(1)
     # Switch back to the main document
    driver.switch_to.default_content()

    return data

executor_url  = sys.argv[1]
session_id = sys.argv[2]
# print executor_link and session_id
print("executor url:   ",executor_url)  # prints the executor URL
print("session id:   ",session_id)
# attach to the session
driver = attach_to_session(executor_url, session_id)
# check if the driver is attached
print("executor url:   ",driver.command_executor._url)  # prints the executor URL
print("current url:   ",driver.current_url)
print("window_handles: ",driver.window_handles)
driver.switch_to.window(driver.window_handles[0])


campaigns = get_info(driver)
# print("campaign:   ",campaign)

for i, campaign in enumerate(campaigns):
    if campaign['status'] == "Sent":
       campaigns[i] =  get_screenshot(driver, campaign)

# write the campaigns to a csv file

with open('campains/campaigns.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'link', 'status', 'campaign_opens_percent', 'campaign_opens_count', 'campaign_clicks_count', 'campaign_clicks_percent', 'filename']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for campaign in campaigns:
        writer.writerow(campaign)
