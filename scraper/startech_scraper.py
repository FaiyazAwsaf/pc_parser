import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import re
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
COMPONENT_FIELDS = {
        "CPU": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Series", "Socket", "Cores", "Threads", "Base frequency", "Maximum Turbo Frequency",
            "L2 Cache", "L3 cache", "Processor Graphics", "maximum memory.", "Include CPU cooler"
        ],
        "RAM": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Type", "Capacity", "Frequency"
        ],
        "GPU": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Chipset", "Type", "Memory", "Core Clock"
        ],
        "Storage": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Capacity", "Type", "Interface", "Read Speed", "Write Speed"
        ],
        "Motherboard": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Socket", "Form Factor", "Maximum memory", "Memory Slot"
        ],
        "Monitor": [
            "Image", "Manufacturer", "Name", "Product URL", "Price", "Availability",
            "Screen Size", "Resolution", "Refresh Rate", "Response Time", "Panel Type", "Aspect Ratio"
        ],
    }

class StarTechScraper:
    def __init__(self):
        self.base_url = "https://www.startech.com.bd"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'
        })
        self.categories = {
            "CPU": "component/processor",
            "RAM": "component/ram",
            "GPU": "component/graphics-card",
            "Storage": "component/ssd-hard-disk",
            "Motherboard": "component/motherboard",
            "Monitor": "monitor",
        }
    
    def get_page(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
                time.sleep(2 ** attempt)
        logger.error(f"Failed to fetch {url} after {max_retries} retries")
        return None

    def extract_brand(self, name):
        name_l = name.lower()
        for b in ("intel", "amd", "corsair", "gigabyte", "asus", "nzxt", "seagate", "kingston", "samsung", "g.skill", "team", "adata"):
            if b in name_l:
                return b.capitalize()
        return "Unknown"

    def extract_product_info(self, container, category_name):
        name_el = container.find(['h4','a'], class_='p-item-name')
        if not name_el:
            return None
        name = name_el.get_text(strip=True)
        link = container.find('a')
        url = urljoin(self.base_url, link['href']) if link else ""
        img = container.find('img')
        image = urljoin(self.base_url, img['src']) if img and img.get('src') else ""
        price_el = container.find(['span', 'div'], class_='price-new')
        if not price_el:
            price_el = container.find(['span', 'div'], class_='price')
        price = price_el.get_text(strip=True) if price_el else ""
        in_stock = bool(container.find('button', string=re.compile(r'Add to Cart|কার্টে যোগ করুন')))
        availability = "In Stock" if in_stock else "Out of Stock"
        item = {
            "Image": image,
            "Manufacturer": self.extract_brand(name),
            "Name": name,
            "Product URL": url,
            "Price": price,
            "Availability": availability,
            "Category": category_name
        }
        if url:
            try:
                details = self.scrape_product_details(url, category_name)
                item.update(details)
            except Exception as e:
                logger.warning(f"Failed to parse details for {url}: {e}")
        return item


    def _parse_spec_table(self, soup):
        specs = {}
        for tbl in soup.find_all('table'):
            for row in tbl.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    specs[key] = value
        return specs

    def _get(self, specs, keys):
        for k in keys:
            if k in specs:
                return specs[k]
        return None

    def scrape_product_details(self, url, category_name):
        details = {}
        resp = self.get_page(url)
        if not resp:
            return details
        soup = BeautifulSoup(resp.content, 'html.parser')
        specs = self._parse_spec_table(soup)
        cat = category_name.lower()

        if cat == "cpu":
            details["Series"] = self._get(specs, ["series"])
            details["Socket"] = self._get(specs, ["socket", "cpu socket"])
            details["Cores"] = self._get(specs, ["cores", "no. of cores", "core count"])
            details["Threads"] = self._get(specs, ["threads", "no. of threads", "thread count"])
            details["Base frequency"] = self._get(specs, ["base frequency", "base clock", "clock speed", "cpu speed"])
            details["Maximum Turbo Frequency"] = self._get(specs, ["maximum turbo frequency", "max turbo frequency", "turbo frequency", "boost clock"])
            details["L2 Cache"] = self._get(specs, ["l2 cache", "cache l2"])
            details["L3 cache"] = self._get(specs, ["l3 cache", "cache l3", "intel smart cache"])
            details["Processor Graphics"] = self._get(specs, ["processor graphics", "graphics", "gpu name", "integrated graphics"])
            details["maximum memory."] = self._get(specs, ["maximum memory", "max memory size", "max memory"])
            details["Cuppon"] = self._get(specs, ["coupon", "cuppon", "discount", "promo"])
            details["Include CPU cooler"] = self._get(specs, ["included cooling solution", "cpu cooler", "cooler"])
        elif cat == "ram":
            details["Type"] = self._get(specs, ["type", "memory type"])
            details["Capacity"] = self._get(specs, ["capacity", "memory size"])
            details["Frequency"] = self._get(specs, ["frequency", "speed", "clock speed", "bus speed"])
        elif cat == "gpu":
            details["Chipset"] = self._get(specs, ["chipset", "gpu chipset", "chipset manufacturer"])
            details["Type"] = self._get(specs, ["type", "card type", "gpu type"])
            details["Memory"] = self._get(specs, ["memory", "memory size", "video memory"])
            details["Core Clock"] = self._get(specs, ["core clock", "base clock", "engine clock"])
        elif cat == "storage":
            details["Capacity"] = self._get(specs, ["capacity", "storage", "size"])
            details["Type"] = self._get(specs, ["type", "drive type", "form factor"])
            details["Interface"] = self._get(specs, ["interface", "interface type", "bus type"])
            details["Read Speed"] = self._get(specs, ["read speed", "sequential read", "max read"])
            details["Write Speed"] = self._get(specs, ["write speed", "sequential write", "max write"])
        elif cat == "motherboard":
            details["Socket"] = self._get(specs, ["socket", "cpu socket", "supported socket"])
            details["Form Factor"] = self._get(specs, ["form factor", "board size"])
            details["Maximum memory"] = self._get(specs, ["maximum memory", "max memory", "memory support"])
            details["Memory Slot"] = self._get(specs, ["memory slot", "memory slots", "ram slot", "slots"])
        elif cat == "monitor":
            details["Screen Size"] = self._get(specs, ["screen size", "display size", "panel size"])
            details["Resolution"] = self._get(specs, ["resolution", "max resolution", "display resolution"])
            details["Refresh Rate"] = self._get(specs, ["refresh rate", "max refresh rate", "refresh"])
            details["Response Time"] = self._get(specs, ["response time", "gray-to-gray response time", "gtg response time"])
            details["Panel Type"] = self._get(specs, ["panel type", "display type", "panel"])
            details["Aspect Ratio"] = self._get(specs, ["aspect ratio", "ratio"])
        return details

    def scrape_category(self, category_name, path, max_pages=2):
        logger.info(f"Scraping category {category_name}")
        items = []
        for page in range(1, max_pages+1):
            page_url = f"{self.base_url}/{path}?page={page}"
            logger.info(f"→ {category_name} page {page}: {page_url}")
            resp = self.get_page(page_url)
            if not resp:
                break
            soup = BeautifulSoup(resp.content, 'html.parser')
            containers = soup.find_all('div', class_='p-item')
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

def save_to_excel(products, filename="startech_components.xlsx"):
    if not products:
        print("No products to save.")
        return
    df = pd.DataFrame(products)
    with pd.ExcelWriter(filename) as writer:
        for cat in df['Category'].unique():
            sheet_fields = COMPONENT_FIELDS.get(cat, df.columns.tolist())
            sub = df[df['Category'] == cat].copy()
            # Only keep columns that exist in this sheet's DataFrame
            cols = [col for col in sheet_fields if col in sub.columns]
            sub = sub[cols]
            sub.to_excel(writer, sheet_name=cat[:31], index=False)
    print(f"Saved {len(df)} products to {filename} (separate sheets for each category)")



if __name__ == "__main__":
    scraper = StarTechScraper()
    all_products = scraper.scrape_all(max_pages_each=2)
    save_to_excel(all_products)
