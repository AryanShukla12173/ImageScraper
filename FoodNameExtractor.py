from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

class FoodItemExtractor:
    def __init__(self):
        # Setup Chrome options and driver here
        options = Options()
        options.binary_location = r"C:\Users\6arya\Desktop\ImageScraper\chrome-win64\chrome.exe"
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-web-security")

        service = Service(r"C:\Users\6arya\Desktop\ImageScraper\chromedriver-win64\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.food_items = []

    def extract_food_names(self, url):
        try:
            print(f"Loading URL: {url}")
            self.driver.get(url)
            time.sleep(3)
            self.load_all_items()
            self.extract_current_items()
            return self.food_items
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return []

    def load_all_items(self):
        load_more_clicked = 0
        max_attempts = 50
        while load_more_clicked < max_attempts:
            try:
                load_more_button = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(@onclick, 'loadAllListItems') and contains(text(), 'LOAD MORE')]"
                    ))
                )
                print(f"Clicking LOAD MORE button (attempt {load_more_clicked + 1})")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                time.sleep(1)
                load_more_button.click()
                time.sleep(3)
                load_more_clicked += 1
            except TimeoutException:
                print("No more LOAD MORE button found or timeout reached")
                break
            except Exception as e:
                print(f"Error clicking LOAD MORE: {str(e)}")
                break
        print(f"Total LOAD MORE clicks: {load_more_clicked}")

    def extract_current_items(self):
        selectors = [
            "h2.h1.h1--bold a",
            ".top-list-article__item h2 a",
            ".middle h2 a",
            "h2[class*='h1--bold'] a"
        ]

        food_elements = []
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    food_elements = elements
                    print(f"Found {len(elements)} food items using selector: {selector}")
                    break
            except:
                continue

        for i, element in enumerate(food_elements):
            try:
                food_name = element.text.strip()
                food_url = element.get_attribute('href')
                ranking = self.find_ranking(element)

                if food_name:
                    food_item = {
                        'name': food_name,
                        'url': food_url,
                        'ranking': ranking,
                        'position': i + 1
                    }
                    self.food_items.append(food_item)
                    print(f"Extracted: {food_name} (Rank: {ranking})")
            except Exception as e:
                print(f"Error extracting food item {i}: {str(e)}")

        print(f"Total food items extracted: {len(self.food_items)}")

    def find_ranking(self, element):
        try:
            parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'top-list-article__item')]")
            rank_element = parent.find_element(By.CSS_SELECTOR, ".left .h1.font-lining-figures")
            return rank_element.text.strip()
        except:
            try:
                parent = element.find_element(By.XPATH, "./ancestor::*[span[contains(@class, 'font-lining-figures')]]")
                rank_element = parent.find_element(By.CSS_SELECTOR, "span.font-lining-figures")
                return rank_element.text.strip()
            except:
                return None

    def save_to_file(self, filename="food_items.json"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.food_items, f, indent=2, ensure_ascii=False)
            print(f"Food items saved to {filename}")
        except Exception as e:
            print(f"Error saving to file: {str(e)}")

    def print_summary(self):
        print("\n" + "="*50)
        print("FOOD ITEMS EXTRACTION SUMMARY")
        print("="*50)
        for item in self.food_items:
            rank = item.get('ranking', 'N/A')
            name = item.get('name', 'Unknown')
            print(f"Rank {rank}: {name}")
        print(f"\nTotal items extracted: {len(self.food_items)}")

    def get_food_names_only(self):
        return [item['name'] for item in self.food_items if item.get('name')]

    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    url = "https://www.tasteatlas.com/best-rated-dishes-in-russia"
    extractor = None
    try:
        extractor = FoodItemExtractor()
        food_items = extractor.extract_food_names(url)
        extractor.print_summary()
        extractor.save_to_file("food_ranking_list_russia.json")
        food_names = extractor.get_food_names_only()
        print(f"\nSimple list of food names:")
        for name in food_names:
            print(f"- {name}")
    except Exception as e:
        print(f"Main execution error: {str(e)}")
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()
