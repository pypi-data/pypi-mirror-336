import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import List, Dict
from .selectors import SELECTORS
from ..core.browser_factory import get_browser_driver


class EntryScraper:

    def __init__(
            self, 
            topic: str, 
            driver_name: str = "uc", 
            headless: bool = False, 
            binary_location: str = None, 
            max_page_limit: int = None, 
            reverse: bool = False
            ):
        self.topic = topic
        self.driver_name = driver_name
        self.headless = headless
        self.browser = get_browser_driver(driver_name, headless, binary_location=binary_location)
        self.driver = self.browser.driver
        self.max_page_limit = max_page_limit
        self.reverse = reverse
        self.entries = []
        self.topic_url = ""

    def open_search_page(self) -> None:
        website = SELECTORS["website"]

        self.driver.get(website)
        try:
            wait_for = SELECTORS["search"]["input"]
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, wait_for))
            )
        except Exception as e:
            print(f"[WARN] Search input did not load properly: {e}")
        
        return
    
    def submit_search(self) -> None:
        input_element_id = SELECTORS["search"]["input"]
        
        search_box = self.driver.find_element("id", input_element_id)
        search_box.clear()
        search_box.send_keys(self.topic)

        button_element_selector = SELECTORS["search"]["button"]
        submit_btn = self.driver.find_element("css selector", button_element_selector)
        submit_btn.click()
        time.sleep(2)
        self.topic_url = self.driver.current_url
        return
    
    def get_total_pages(self) -> int:
        last_page_element_selector = SELECTORS["entry"]["total_page"]
        try:
            last_page_element = self.driver.find_element("css selector", last_page_element_selector)
            return int(last_page_element.text)
        except:
            return 1
        
    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    def scrape_page(self, page_num: int) -> List[Dict[str, str]]:
        container_class = SELECTORS["entry"]["container"]
        author_class = SELECTORS["entry"]["author"]
        date_class = SELECTORS["entry"]["date"]
        content_class = SELECTORS["entry"]["content"]

        url = self.topic_url if page_num == 1 else f"{self.topic_url}?p={page_num}"
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, container_class))
            )
        except Exception as e:
            print(f"[WARN] No entries found on page {page_num}: {e}")

        self.scroll_to_bottom()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        results = []

        entry_items = soup.select(container_class)
        for item in entry_items:
            content_div = item.select_one(content_class)
            author_a = item.select_one(author_class)
            date_a = item.select_one(date_class)

            entry = {
                "content": content_div.get_text(separator=" ", strip=True) if content_div else None,
                "author": author_a.text.strip() if author_a else None,
                "date": date_a.text.strip() if date_a else None,
            }
            results.append(entry)

        return results

    def scrape(self) -> List[Dict[str, str]]:
        try:
            self.open_search_page()
            self.submit_search()
            total_pages = self.get_total_pages()

            if self.max_page_limit is not None:
                page_count = min(self.max_page_limit, total_pages)
            else:
                page_count = total_pages

            if self.reverse:
                page_range = range(total_pages, total_pages - page_count, -1)
            else:
                page_range = range(1, page_count + 1)

            print(f"[INFO] Scraping topic: {self.topic_url} with {len(page_range)} pages")

            for page in page_range:
                page_entries = self.scrape_page(page)
                self.entries.extend(page_entries)
                print(f"[INFO] Scraped page {page}/{page_count}")
                
            return self.entries

        finally:
            self.browser.quit()