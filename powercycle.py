import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
# Using WebDriver Manager to handle the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Your code to interact with the webpage goes here


# Go to the login page of the website
driver.get("https://192.168.5.141/")

# Wait for the page to load

time.sleep(10)

# Find the username and password fields and enter the login credentials
username_field = driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > div.page-container > div > div:nth-child(2) > div > div.panel.panel-narrow > div > div > div > div > form > div > div:nth-child(1) > input")
username_field.send_keys("admin")

password_field = driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > div.page-container > div > div:nth-child(2) > div > div.panel.panel-narrow > div > div > div > div > form > div > div:nth-child(2) > input")
password_field.send_keys("Q7A5M2KHZ83D")

# Find and click the login button
login_button = driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > div.page-container > div > div:nth-child(2) > div > div.panel.panel-narrow > div > div > div > div > form > div > div.dashboard-login-buttons > button")
login_button.click()

# Wait for the login to complete and the new page to load
time.sleep(15)
showdetails = driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > div.page-container > div:nth-child(2) > div:nth-child(3) > div > div > div.dashboard-accordion-row-link > a")
showdetails.click()

# driver.get("hhttps://192.168.5.141/awusb/?view=status")
# Wait for the page to load
time.sleep(10)
# Find and click the target button after login
target_button = driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > div.page-container > div:nth-child(1) > div.accordion-wrapper.expander.accordion-wrapper-after-title.open-accordion > div.accordion-content > table > tbody > tr:nth-child(2) > td:nth-child(7) > input")
target_button.click()
time.sleep(20)
# Close the browser
driver.quit()
