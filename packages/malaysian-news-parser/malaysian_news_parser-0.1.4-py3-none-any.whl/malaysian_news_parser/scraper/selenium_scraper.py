### src/malaysian_news_parser/scraper/selenium_scraper.py ###
# A scraper that extracts article links from dynamic websites using Selenium.

# Import libraries
from selenium import webdriver # Selenium WebDriver
from selenium.webdriver.common.by import By # For selecting elements by attribute
from selenium.webdriver.support.ui import WebDriverWait # For waiting until elements are loaded
from selenium.webdriver.support import expected_conditions as EC # For defining expected conditions
from selenium.webdriver.chrome.service import Service # Chrome service
from selenium.webdriver.chrome.options import Options # Chrome options

from datetime import datetime

from bs4 import BeautifulSoup # HTML parsing

from ..base_scraper import BaseScraper # Base Scraper

import time # For adding delays
import logging # For logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumScraper(BaseScraper):
    '''
        SeleniumScraper class handles scraping dynamic websites that require JavaScript interaction
        by using Selenium to control a browser, interact with page elements, and extract article links.
    '''

    def fetch_content(self, url):
        '''
            Fetches the HTML content of the given URL using Selenium.
            
            Args:
                url (str): The URL to fetch content from.
            
            Returns:
                str: The HTML content of the page if the request is successful.
        '''

        # Configure the Chrome webdriver
        chrome_options = Options()

        # # Set driver to headless mode
        # chrome_options.add_argument("--headless")

        # # Disable driver GPU
        # chrome_options.add_argument("--disable-gpu")

        # Disable sandbox
        chrome_options.add_argument("--no-sandbox")

        # Set optimal usage of Chrome
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the Chrome service
        chrome_options.binary_location = self.config['chrome_path']

        # Start the Chrome service
        self.driver = webdriver.Chrome(options=chrome_options)

        # Get the configuration parameters for fetching content
        config = self.config['link_scrape_config']
        
        # Set the default values for the parameters
        iterate_pages = config.get('iterate_pages') # Whether to iterate through multiple pages
        max_pages = config.get('max_pages') # The maximum number of pages to iterate through
        simulate_click = config.get('simulate_click') # Whether to simulate a click to load more content
        max_clicks = config.get('max_clicks') # The maximum number of clicks to simulate

        # If the iterate_pages flag is set to True, iterate through multiple pages
        if iterate_pages:

            page_contents = []

            try:

                # Get the content for the page without a number
                current_url = self.clean_url(url)

                # Initialize the driver
                driver = self.driver

                # Load the URL
                driver.get(current_url)

                # Wait for the page to load
                time.sleep(5)

                # Get the page source
                html_content = driver.page_source

                # Append the page source to the list
                page_contents.append(html_content)

                # Close the Driver
                driver.close()

                # Quit the driver
                driver.quit()

                # Iterate through each page and add the page source that is rendered to the list
                page_contents.extend(self.iterate_pages_and_extract_content(url, max_pages))

                return page_contents
            
            except Exception as e:
                    
                    logger.error(f"Error fetching content: {e}")
    
                    return []
            
        elif simulate_click:

            page_contents = []

            try:


                # Add new content to the list
                page_contents.extend(self.simulate_see_more_and_extract_page_content(False, datetime(2017, 12, 31), url))

                page_contents = ''.join(page_contents)

                return page_contents

            except Exception as e:
                        
                logger.error(f"Error fetching content: {e}")
                return []




    def iterate_pages_and_extract_content(self, url, max_pages):
        '''
            Iterate through multiple pages and extract article links.
            
            Args:
                url (str): The base URL.
                max_pages (int): The maximum number of pages to scrape.
            
            Returns:
                list: A list of article link dictionary objects.
                format: [{'link': 'article_link'}, ...]
        '''

        # List to store the extracted links
        page_contents = []

        for pageNo in range(1, max_pages):

            # Construct the URL for the current page
            current_url = self.construct_url(url, pageNo)

            # Initialize the driver
            driver = self.driver

            # Load the URL
            driver.get(current_url)

            # Wait for the page to load
            time.sleep(5)

            # Get the page source
            html_content = driver.page_source

            # Append the page source to the list
            page_contents.append(html_content)

            # if max pages is reached, break the loop
            if pageNo >= max_pages:
                print(f'Maximum number of pages reached: {max_pages}')
                driver.close()
                driver.quit()
                break

            driver.close()
            driver.quit()

        return page_contents
    
 


    def construct_url(self, url, page):
        '''
            Construct the URL for the next page to scrape.
            
            Args:
                url (str): The base URL.
                pageNo (int): The page number.
            
            Returns:
                str: The constructed URL.
        '''

        # Get the configuration parameters for page iteration
        config = self.config['link_scrape_config']

        # Replace the placeholder "{pageNo}" in the page iterator template with the actual page number
        page_number = str(page)  # Ensure 'page' is a string

        page_path = config['page_iterator'].replace("{pageNo}", page_number)

        # Replace the placeholder "{page_iterator}" in the base URL with the constructed page path
        final_url = url.replace("{page_iterator}", page_path)

        # Return final_url
        return final_url
    
    def clean_url(self, url):
        '''
            Clean the URL by removing unwanted parameters.
            
            Args:
                url (str): The URL to clean.
            
            Returns:
                str: The cleaned URL.
        '''

        return url.replace("{page_iterator}", "")
    
    def parse_date(self, date_string):
        '''
            Parses a date string into a datetime object. Adjust the format as needed.

            :param date_string: Date string from the webpage.
            :return: Parsed datetime object.
        '''
        try:
            return datetime.strptime(date_string, "%b.%d, %Y")
        except ValueError as e:
            print(f"Error parsing date '{date_string}': {e}")
            return None
    

        
    def get_last_article_date(self, html_content, date_selector):
        '''
            Retrives the date of the last visible article on the page.

            :param html_content: The full HTML content of the page as a string.
            :param date_selector: CSS Selector for the article date.
            :return: Date of the last article as a datetime object, or None if parsing fails.
        '''
        try:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all elements matching the date selecto

            print(date_selector)
            date_elements = soup.find_all('div', attrs={'class': 'pub-date'})
            print(date_elements)
            
            if not date_elements:
                print("No date elements found")
                return None
            
            # Get the text of the last date element
            last_date_text = date_elements[-1].text.strip()
            
            return self.parse_date(last_date_text)
        
        except Exception as e:
            print(f"Error parsing last article date: {e}")
            return None
        



    
    def simulate_see_more_and_extract_page_content(self, clicks, cutoff_date: datetime, url):
        '''
            Simulates scrolling to the bottom of the page and clicking the 'See More' button.
            Uses multiple approaches to ensure the button is clicked successfully.
        '''

        # Get the configuration parameters for simulating a click
        config = self.config['link_scrape_config']['link_selector']


        if clicks:
            try:

                # Simulate a click to load more content
                for i in range(config['max_clicks']):

                    if config['type'] == 'class':

                        # Find the 'See More' button by class name
                        see_more_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, '{config['text']}')]"))
                        )

                    elif config['type'] == 'id':

                        # Find the 'See More' button by id
                        see_more_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//button[@id='{config['text']}']"))
                        )

                    elif config['type'] == 'css':
                            
                        # Find the 'See More' button by CSS selector
                        see_more_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, config['text']))
                        )

                    else:
                        logger.error("Invalid selector type. Please use either 'class', 'id', or 'css'.")

                    
                    # Click the 'See More' button
                    self.driver.execute_script("arguments[0].click();", see_more_button)

                    # Wait for content to load
                    time.sleep(3)

                # Get page source of the loaded content
                html_content = self.driver.page_source

                return html_content
            
            except Exception as e:

                logger.error(f"Error simulating click: {e}")

                return None
        else:

            # Initialize the driver
            driver = self.driver

            # Load the URL
            driver.get(url)

            print('1')


            if config['type'] == 'class':

                print(config['text'])
                # time.sleep(100)
                    # Find the 'See More' button by class name
                see_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME,  'click-more'))
                )

            elif config['type'] == 'id':

                # Find the 'See More' button by id
                see_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[@id='{config['text']}']"))
                )

            elif config['type'] == 'css':
                    
                # Find the 'See More' button by CSS selector
                see_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, config['text']))
                )

            else:
                logger.error("Invalid selector type. Please use either 'class', 'id', or 'css'.")

            while True:
                html_content = self.driver.page_source

                last_article_date = self.get_last_article_date(html_content, self.config['date_selector'])
                logger.info(f"Last article date {last_article_date} and the cutoff date {cutoff_date}.")
                    # If the date is older than the cutoff, continue clicking
                if last_article_date and last_article_date > cutoff_date:
                    print('true')
                    logger.info(f"Last article date {last_article_date} is older than the cutoff date {cutoff_date}. Clicking 'See More' again.")
                    # Click the 'See More' button
                    self.driver.execute_script("arguments[0].click();", see_more_button)

                    time.sleep(10)
                else:
                    print('false')
                    logger.info(f"Found articles with a recent date {last_article_date}. Stopping.")
                    break
            
            return html_content 
            
            
            
                                            # Close the Driver
            driver.close()

            # Quit the driver
            driver.quit()
                    
                 # Return the page content if the last article's date is not older than the cutoff date
                
            # except Exception as e:
            #     logger.error(f"Error simulating clicks: {e}")
            #     return None



    def extract_article_links(self, html_content):
        '''
            Extract article links from the current page.
            
            Returns:
                list: A list of article link dictionary objects.
                format: [{'link': 'article_link'}, ...]
        '''

        # Get the configuration parameters for extracting links
        config = self.config['link_scrape_config']['link_selector']

        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            # Empty list to store the extracted links
            links = []

            if config['type'] == 'class':

                # Find all articles by class name
                articles = soup.find_all(config['element'], class_=config['text'])
                print('hello')
            elif config['type'] == 'id':

                # Find all article links by id
                articles = soup.find_all(config['type'], id=config['text'])

            elif config['type'] == 'css':

                # Find all article links by CSS selector
                articles = soup.select(config['text'])

            else:

                logger.error("Invalid selector type. Please use either 'class', 'id', or 'css'.")
                return []
            
            print(articles[0])
            # Iterate through the article objects
            for article in articles:
                
                # Locate the <a> tag and extract the href attribute
                a_tag = article.find('a')

                # Extract the link
                link = a_tag['href']

                # Append the link to the list of links
                links.append({'link': "https://eng.yidaiyilu.gov.cn" + link, 'headline': a_tag.text.strip()})
            
            return links
        
        except Exception as e:

            logger.error(f"Error extracting links: {e}")

            return []
        
    def __del__(self):
        '''
            Close the Selenium WebDriver when the object is deleted.
        '''
        
        # Close the Selenium WebDriver
        self.driver.quit()

        # Close the webdriver
        self.driver.close()