import os
import time
import logging
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DESIRED_CATEGORIES = {
    "CPU": "desktop-component-processor",
    "RAM": "desktop-component-desktop-ram",
    "Monitor": "monitor-all-monitor",
}


class RyansScraper:
    def __init__(self, headless=True):
        self.base_url = "https://www.ryans.com/category/"
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.categories = DESIRED_CATEGORIES

    @staticmethod
    def clean_price(price_str):
        price_nums = re.findall(r"\d+", price_str.replace(",", ""))
        return int("".join(price_nums)) if price_nums else None

    def extract_product_info(self, container, category_name):
        img = container.find("img", alt=True)
        if not img:
            return None
        name = img["alt"].strip()
        imgsrc = img.get("src", "")
        image_url = (
            imgsrc
            if imgsrc.startswith("http")
            else urljoin("https://www.ryans.com", imgsrc.lstrip("./"))
        )
        link = container.find("a", href=True)
        url = urljoin("https://www.ryans.com", link["href"]) if link else ""
        # Find price in anchor with pr-text class
        price_tag = container.find("a", class_=lambda c: c and "pr-text" in c)
        price = None
        if price_tag:
            m = re.search(r"Tk\s*([\d,]+)", price_tag.get_text(strip=True))
            if m:
                price = int(m.group(1).replace(",", ""))
        in_stock = "Add to Cart" in container.get_text()
        availability = "In Stock" if in_stock else "Out of Stock"

        item = {
            "retailer": "ryans",
            "retailer_name": name,
            "price": price,
            "url": url,
            "image_url": image_url,
            "availability": availability,
            "category": category_name,
        }
        return item

    def scrape_category(self, category_name, slug, max_pages=1):
        logger.info(f"Scraping category {category_name}")
        items = []
        for page in range(1, max_pages + 1):
            page_url = f"{self.base_url}{slug}?page={page}"
            logger.info(f"→ {category_name} page {page}: {page_url}")
            self.driver.get(page_url)
            # Wait for JS to render
            time.sleep(3)
            # Optionally, scroll to bottom to load more (uncomment if needed)
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(2)
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            containers = soup.find_all(
                "div", class_=lambda c: c and "category-single-product" in c
            )
            if not containers:
                logger.info("No more products found.")
                break
            for cont in containers:
                info = self.extract_product_info(cont, category_name)
                if info:
                    items.append(info)
            time.sleep(1)
        logger.info(f"Found {len(items)} items in {category_name}")
        return items

    def scrape_all(self, max_pages_each=1):
        all_prod = []
        for name, slug in self.categories.items():
            prods = self.scrape_category(name, slug, max_pages_each)
            all_prod.extend(prods)
        self.driver.quit()
        return all_prod


def save_to_json(products, filename="ryans_products.json"):
    if not products:
        print("No products to save.")
        return
    dirpath = os.path.dirname(filename)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(products)} products to {filename}")


if __name__ == "__main__":
    scraper = RyansScraper(headless=True)
    all_products = scraper.scrape_all(
        max_pages_each=1
    )  # Increase for more pages per category
    save_to_json(all_products, "ryans_products.json")
