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
urls = ["https://www.tellart.com/",
"https://www.tellart.com/services",
"https://www.tellart.com/about",
"https://www.tellart.com/projects/dinner-in-2050",
"https://www.tellart.com/projects/uae-pavilion",
"https://www.tellart.com/projects/chrome-web-lab",
"https://www.tellart.com/projects/mofgs-2015",
"https://www.tellart.com/projects/biomuseo",
"https://www.tellart.com/projects/van-gogh-dreams",
"https://www.tellart.com/projects/concept-i",
"https://www.tellart.com/projects/deyoungsters",
"https://www.tellart.com/projects/challenge-museum",
"https://www.tellart.com/projects/panacea",
"https://www.tellart.com/projects/arc",
"https://www.tellart.com/projects/asian-galleries",
"https://www.tellart.com/projects/coffee-connector",
"https://www.tellart.com/projects/soundaffects-nyc",
"https://www.tellart.com/projects/real-good-chair-experiment",
"https://www.tellart.com/projects/color-visualizer",
"https://www.tellart.com/projects/designnonfiction",
"https://www.tellart.com/projects/terraform-table",
"https://www.tellart.com/projects/mofgs-2014",
"https://www.tellart.com/projects/museum-of-the-future-machinic-life",
"https://www.tellart.com/projects/floriade-2022"]
# urls = ['http://localhost:8000/', 'http://localhost:8000/about.html', 'http://localhost:8000/services.html', 'http://localhost:8000/projects/designnonfiction/','http://localhost:8000/projects/concept-i/' ,'http://localhost:8000/projects/concept-i/','http://localhost:8000/projects/biomuseo/','http://localhost:8000/projects/deyoungsters/', 'http://localhost:8000/projects/s7-imagination-machine/', 'http://localhost:8000/projects/chrome-web-lab/', 'http://localhost:8000/projects/terraform-table/','http://localhost:8000/projects/alita-battle-angel/','http://localhost:8000/projects/binoculars/', 'http://localhost:8000/projects/asian-galleries/', 'http://localhost:8000/projects/van-gogh-dreams/', 'http://localhost:8000/projects/craftsmanship/','http://localhost:8000/projects/coffee-connector/','http://localhost:8000/projects/museum-of-the-future-climate-change-reimagined/', 'http://localhost:8000/projects/museum-of-the-future-machinic-life/', 'http://localhost:8000/projects/autoportrait/', 'http://localhost:8000/projects/real-good-chair-experiment/', 'http://localhost:8000/projects/mofgs-2015/','http://localhost:8000/projects/soundaffects-nyc/', 'http://localhost:8000/projects/deep-future-star-charts-for-the-next-hundred-thousand-years/', 'http://localhost:8000/projects/mofgs-2014/', 'http://localhost:8000/projects/color-visualizer/']
resolutions = [(1920, 1200), (720, 1024), (430, 932)]



def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def get_total_height(driver, url):
    driver.get(url)
    time.sleep(2)
    return driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")


def accept_cookies(driver):
    coockies_btn = driver.find_element(By.CSS_SELECTOR, "body > div.cc-window.cc-floating.cc-type-info.cc-theme-block.cc-bottom.cc-right.cc-color-override-119089823 > div > a")
    coockies_btn.click()

def capture_segments(driver, total_height, scroll_height):
    # Scroll and capture the page in segments
    segments = []
    for i in range(0, total_height, scroll_height):
        if i > 0:
            driver.execute_script("document.querySelector('header').style.display = 'none'; ")
            # print("\t\theader removed")
        # h  = get_total_height(driver, url)
        driver.execute_script(f"window.scrollTo(0, {i})")
        scrollY = driver.execute_script("return window.scrollY")
        offset  = scrollY - i 
        # if offset != 0:
        #     driver.set_window_size(1920, scroll_height-offset)
        #     time.sleep(.5)  
        #     driver.execute_script(f"window.scrollTo(0, {i-offset })")
        print("scrollY", scrollY, i, offset, scrollY + offset )
        time.sleep(.5)  # Adjust as necessary
        png = driver.get_screenshot_as_png()
        im = Image.open(io.BytesIO(png))
        segments.append(im)
    return segments

def stich_segments(segments, url, width, total_height):
    # Stitch images together
    stitched_image = Image.new('RGB', (width, total_height))
    y_offset = 0
    for im in segments:
        stitched_image.paste(im, (0, y_offset))
        y_offset += im.size[1]

    # Save stitched image
    filename = f'www_{url.replace("https://www.", "").replace("/","_")}_{width}.png'
    stitched_image.save(filename)
    
def get_screenshot(driver, url, width):
    driver.get(url)
    driver.set_window_size(width, 800)
    driver.refresh()
    time.sleep(5)
    total_height = get_total_height(driver, url)
    print("url", url, "width", width, "total_height", total_height)
    try:
        accept_cookies(driver)
    except:
        print("no cookies")

    time.sleep(10)
    
    print("Window size before setting:", driver.get_window_size())
    driver.set_window_size(width, total_height)  # Set a reasonable window height
    print("Window size after setting:", driver.get_window_size())
    time.sleep(5)
    # Find the full page element (usually 'body') and capture the screenshot
    full_page = driver.find_element(By.TAG_NAME, "html")
    print("Full page size before screenshot:", full_page.size )
    filename = f'2023.{url.replace("https://www.", "").replace("/","_").replace(".html","")}_{width}.png'
    full_page.screenshot(filename)
    driver.quit()



for url in urls:
    for resolution in resolutions:
        driver = setup_driver()
        get_screenshot(driver, url, resolution[0])

# driver.quit()


