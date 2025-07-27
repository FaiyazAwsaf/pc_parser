import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

options = uc.ChromeOptions()
# options.headless = True  # <-- COMMENT THIS OUT

driver = uc.Chrome(options=options)
driver.get("https://pcpartpicker.com/products/cpu/")
time.sleep(5)  # Wait a bit longer

soup = BeautifulSoup(driver.page_source, "html.parser")
print(soup.prettify()[:3000])

driver.quit()
