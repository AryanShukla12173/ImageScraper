# 🖼️ Image Scraper Script

A Python-based image scraper that uses **Selenium** to download food images from **DuckDuckGo** based on a list of food items provided in a JSON file.

---

## 📁 Configuration of the Script

1. **Chrome Browser (Testing Version)**
   - Download the **Chrome for Testing** browser from the official site:
     👉 [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
   - Extract the archive and locate the `chrome.exe` file inside the `chrome-win64` folder.
   - Copy its full path and update the following line in the script:
     ```python
     options.binary_location = r"your_chrome_path_here"
     ```

2. **ChromeDriver**
   - Make sure the ChromeDriver version matches the version of Chrome for Testing you downloaded.
   - You can download the corresponding `chromedriver-win64.zip` from the same site mentioned above or directly from:
     👉 [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
   - Extract the archive and locate `chromedriver.exe` inside the `chromedriver-win64` folder.
   - Copy its full path and update the following line in the script:
     ```python
     service = Service(r"your_chromedriver_path_here")
     ```

---

## 🔧 Parameters for Customizing Operation

- `max_images` : Number of images to scrape per food item.
- `delay`      : Delay between operations (in seconds). Helps reduce chances of bot detection.

---

## ▶️ Operating the Script

1. **Install Required Packages**
   ```bash
   pip install selenium pillow requests
