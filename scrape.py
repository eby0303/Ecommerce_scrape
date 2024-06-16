import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from autoscraper import AutoScraper

def scrape_data(url, wanted_list):
    # Setup Selenium
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    # Giving some time for the page to load
    driver.implicitly_wait(10)
    driver.maximize_window()

    # Extract page source
    html_content = driver.page_source
    driver.quit()

    # Setup AutoScraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)

    # Get results
    results = scraper.get_result_similar(html=html_content, grouped=True)

    # Identify keys
    product_name_keys, price_keys = identify_keys(results)

    # Ensure there is at least one product name key and one price key
    if not product_name_keys:
        raise ValueError("No product name keys found in the result.")
    if not price_keys:
        raise ValueError("No price keys found in the result.")

    # Get the second key-value items from the results
    product_names = results.get(product_name_keys[1])
    prices = results.get(price_keys[1])

    return {'Title': product_names, 'Price': prices}

def identify_keys(data):
    product_name_keys = []
    price_keys = []
    
    for key, values in data.items():
        if all(isinstance(value, str) and not value.startswith('₹') for value in values):
            product_name_keys.append(key)
        elif all(isinstance(value, str) and value.startswith('₹') for value in values):
            price_keys.append(key)
    
    return product_name_keys, price_keys
