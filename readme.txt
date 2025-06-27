
Image Scraper Script Instructions
=================================

Configuration of the Script
---------------------------
1) Locate the `chrome.exe` file inside the `chrome-win64` folder.
   - Copy its full path and paste it into the following line in the script:
     options.binary_location = r"your_chrome_path_here"

2) Locate the `chromedriver.exe` file inside the `chromedriver-win64` folder.
   - Copy its full path and paste it into the following line in the script:
     service = Service(r"your_chromedriver_path_here")

Parameters for Customizing Operation
------------------------------------
1) max_images : Controls how many images get scraped for each food item.
2) delay      : Controls the delay between operations. Helps avoid bot detection.

Operating the Script
--------------------
1) Ensure required packages are installed:
   pip install selenium pillow requests

2) The script loads a JSON file with a list of food items from a specific country:
   Example:
   with open('food_ranking_list_india.json') as f:

3) To switch countries:
   Replace the JSON file in the script with another file like:
   'food_ranking_list_china.json', 'food_ranking_list_usa.json', etc.

4) When prompted, enter the starting index for scraping:
   Enter start index (0 to 99): 0

5) The script will open DuckDuckGo, search for each food item, switch to the "Images" tab, and download images to the `imgs/<food_name>/` folder.

Note
----
- The script is not 100% reliable; some images may fail to download due to bad URLs or minor script glitches.
- Recommended to test with a few items first.
