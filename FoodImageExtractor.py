from json import load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests
import io
import os
from PIL import Image

# ---------- Setup ----------
# Load food names from JSON 
with open('food_ranking_list_india.json') as f:
    food_data = load(f)

# Ask user for start index
while True:
    try:
        start_index = int(input(f"Enter start index (0 to {len(food_data) - 1}): "))
        if 0 <= start_index < len(food_data):
            break
        else:
            print("Invalid input. Please enter a valid index.")
    except ValueError:
        print("Please enter an integer value.")

# Chrome setup
options = Options()
options.binary_location = r"C:\Users\6arya\Desktop\ImageScraper\chrome-win64\chrome.exe"
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")

service = Service(r"C:\Users\6arya\Desktop\ImageScraper\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ---------- Helper Functions ----------
def scroll_down(wd, delay):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay)

def get_images_from_search(wd, delay, max_images):
    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd, delay)
        thumbnails = wd.find_elements(By.CSS_SELECTOR, '.SZ76bwIlqO8BBoqOLqYV img')

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "d1fekHMv2WPYZzgPAV7b")
            for image in images:
                src = image.get_attribute('src')
                if src in image_urls:
                    skips += 1
                    continue
                if src and 'http' in src:
                    image_urls.add(src)
                    print(f"Found {len(image_urls)}")

            if len(image_urls) >= max_images:
                break

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        os.makedirs(download_path, exist_ok=True)
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Downloaded: {file_name}")
    except Exception as e:
        print(f"FAILED: {url} - {e}")

# ---------- Main Script ----------
for idx in range(start_index, len(food_data)):
    food_name = food_data[idx]['name']
    print(f"\n[{idx}] Searching images for: {food_name}")

    # Visit DuckDuckGo
    driver.get("https://duckduckgo.com/")
    time.sleep(2)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'searchbox_input'))
        )
        search_box.clear()
        search_box.send_keys(food_name)
        search_box.send_keys(Keys.RETURN)

        # Click on Images tab
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Images"))
        ).click()

        time.sleep(2)

        # Get image URLs
        image_urls = get_images_from_search(driver, delay=1, max_images=50)

        # Download images
        for i, url in enumerate(image_urls):
            download_image(f"imgs/{food_name}/", url, f"{i}.jpg")

    except Exception as e:
        print(f"Error fetching images for {food_name}: {e}")

driver.quit()
