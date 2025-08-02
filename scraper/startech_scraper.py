import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import re
import json
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DESIRED_CATEGORIES = {
    "CPU": "component/processor",
    "RAM": "component/ram",
    "Monitor": "monitor",
}


class StarTechScraper:
    def __init__(self):
        self.base_url = "https://www.startech.com.bd"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            }
        )
        self.categories = DESIRED_CATEGORIES

    def get_page(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
                time.sleep(2**attempt)
        logger.error(f"Failed to fetch {url} after {max_retries} retries")
        return None

    @staticmethod
    def clean_price(price_str):
        price_nums = re.findall(r"\d+", price_str.replace(",", ""))
        return int("".join(price_nums)) if price_nums else None

    def get_model_from_detail(self, product_url):
        resp = self.get_page(product_url)
        if not resp:
            return None
        soup = BeautifulSoup(resp.content, "html.parser")
        # 1. Check for 'li' elements under '.short-description'
        desc = soup.find("div", class_="short-description")
        if desc:
            for li in desc.find_all("li"):
                text = li.get_text(strip=True)
                if text.lower().startswith("model:"):
                    return text.split(":", 1)[1].strip()
        # 2. (Fallback) Look in any table rows (for other product types)
        for row in soup.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) >= 2:
                label = tds[0].get_text(strip=True).lower()
                value = tds[1].get_text(strip=True)
                if "model" in label or "part no" in label or "product code" in label:
                    return value
        return None

    def extract_product_info(self, container, category_name):
        name_el = container.find(["h4", "a"], class_="p-item-name")
        if not name_el:
            return None
        name = name_el.get_text(strip=True)
        link = container.find("a")
        url = urljoin(self.base_url, link["href"]) if link else ""
        img = container.find("img")
        image_url = urljoin(self.base_url, img["src"]) if img and img.get("src") else ""
        price_el = container.find(["span", "div"], class_="price-new")
        if not price_el:
            price_el = container.find(["span", "div"], class_="price")
        price_str = price_el.get_text(strip=True) if price_el else ""
        price = self.clean_price(price_str)
        in_stock = bool(
            container.find("button", string=re.compile(r"Add to Cart|কার্টে যোগ করুন"))
        )
        availability = "In Stock" if in_stock else "Out of Stock"

        model = self.get_model_from_detail(url) if url else None

        item = {
            "retailer": "startech",
            "retailer_name": name,
            "price": price,
            "url": url,
            "image_url": image_url,
            "availability": availability,
            "category": category_name,
            "model": model,
        }
        return item

    def scrape_category(self, category_name, path, max_pages=2):
        logger.info(f"Scraping category {category_name}")
        items = []
        for page in range(1, max_pages + 1):
            page_url = f"{self.base_url}/{path}?page={page}"
            logger.info(f"→ {category_name} page {page}: {page_url}")
            resp = self.get_page(page_url)
            if not resp:
                break
            soup = BeautifulSoup(resp.content, "html.parser")
            containers = soup.find_all("div", class_="p-item")
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

    def scrape_all(self, max_pages_each=2):
        all_prod = []
        for name, path in self.categories.items():
            prods = self.scrape_category(name, path, max_pages_each)
            all_prod.extend(prods)
        return all_prod


def save_to_json(products, filename="data/startech_products.json"):
    if not products:
        print("No products to save.")
        return
    # Ensure the parent directory exists
    dirpath = os.path.dirname(filename)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(products)} products to {filename}")


if __name__ == "__main__":
    scraper = StarTechScraper()
    all_products = scraper.scrape_all(
        max_pages_each=5
    )  # change to larger number for more pages
    save_to_json(all_products)
