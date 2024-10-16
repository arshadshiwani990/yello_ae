import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# Initialize Selenium WebDriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-javascript")  # Disable JavaScript


driver = webdriver.Chrome(options=chrome_options)

class YelloScraper:
    base_url = 'https://www.yello.ae'

    def __init__(self):
        # Open CSV file to write data
        self.csv_file = open('scraped_data.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=[
            'company_name', 'company_tag', 'location', 'phone', 'mobile',
            'website', 'establishment_year', 'employees', 'company_manager'
        ])
        # Write the CSV headers
        self.csv_writer.writeheader()

    def start_requests(self):
        # Loop through a range of URLs to scrape
        for i in range(1000, 1500):
            url = f'https://www.yello.ae/location/dubai/{i}'
            print(f"Scraping: {url}")
            self.scrape_listing(url)

    def scrape_listing(self, url):
        # Use the WebDriver to load the page
        driver.get(url)
        try:
            # Wait until the page loads and elements are present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"company with_img")]/h4/a'))
            )
        except TimeoutException:
            print(f"Timeout on page: {url}")
            return

        # Find all the company links on the page
        company_link_list = []
        links = driver.find_elements(By.XPATH, '//div[contains(@class,"company with_img")]/h4/a')
        for link in links:
            company_link = link.get_attribute('href')
            company_link_list.append(company_link)

        # Scrape each company page
        for link in company_link_list:
            self.scrape_company(link)

    def scrape_company(self, company_link):
        print(f"Scraping company: {company_link}")
        driver.get(company_link)
        try:
            # Wait until the company page loads
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1'))
            )
        except TimeoutException:
            print(f"Timeout when loading company page: {company_link}")
            return

        # Try to extract each field from the company page
        try:
            company_name = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            company_name = None

        try:
            company_tag = driver.find_element(By.XPATH, '//div[@class="important_tag"]').text
        except NoSuchElementException:
            company_tag = None

        try:
            location = driver.find_element(By.XPATH, '//div[@class="text location"]').text
        except NoSuchElementException:
            location = None

        try:
            phone = driver.find_element(By.XPATH, '//div[@class="text phone"]/a').text
        except NoSuchElementException:
            phone = None

        try:
            mobile = driver.find_element(By.XPATH, "//div[contains(text(),'Mobile phone')]/following-sibling::div/a").text
        except NoSuchElementException:
            mobile = None

        try:
            website = driver.find_element(By.XPATH, "//div[contains(text(),'Website address')]/following-sibling::div/a").text
        except NoSuchElementException:
            website = None

        try:
            establishment_year = driver.find_element(By.XPATH, "//div[@class='info'][span[text()='Establishment year']]").text
        except NoSuchElementException:
            establishment_year = None

        try:
            employees = driver.find_element(By.XPATH, "//div[@class='info'][span[text()='Employees']]").text
        except NoSuchElementException:
            employees = None

        try:
            company_manager = driver.find_element(By.XPATH, "//div[@class='info'][span[text()='Company manager']]").text
        except NoSuchElementException:
            company_manager = None

        # Store the scraped data in a dictionary
        item = {
            'company_name': company_name,
            'company_tag': company_tag,
            'location': location,
            'phone': phone,
            'mobile': mobile,
            'website': website,
            'establishment_year': establishment_year,
            'employees': employees,
            'company_manager': company_manager
        }

        # Print the scraped data and write it to the CSV file
        print(item)
        self.csv_writer.writerow(item)

    def close(self):
        # Close the WebDriver and CSV file when finished
        driver.quit()
        self.csv_file.close()

# Initialize and start the scraper
if __name__ == '__main__':
    scraper = YelloScraper()
    scraper.start_requests()
    scraper.close()
