from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from ..base_parser import BaseParser
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicParser(BaseParser):

    def fetch_content(self, url):
        '''
            Fetches the HTML content of the given URL using Selenium.

            Parameters:
                url (str): The URL to fetch content from.

            Returns:
                str: The HTML content of the page if the request is successful.
        '''

        # Configure the Chrome webdriver
        chrome_options = Options()

        # Set driver to headless mode
        chrome_options.add_argument("--headless")

        # Disable driver GPU
        chrome_options.add_argument("--disable-gpu")

        # Disable sandbox
        chrome_options.add_argument("--no-sandbox")

        # Set optimal usage of Chrome
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set the path to the Chrome driver
        chrome_options.binary_location = self.config['chrome_path']

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Load the URL
            driver.get(url)

            # Wait for the page to load
            time.sleep(self.config.get('sleep_time', 5))

            # Get the page source
            html_content = driver.page_source

            # Close the Driver
            driver.close()

            # Quit the driver
            driver.quit()



            return html_content
        
        except Exception as e:
            logger.error(f"An error occurred while fetching the content: {e}")
            driver.quit()
            driver.close()
            return None
        
    def parse_content(self, html_content):
        '''
            Parses the HTML content to extract the article's title, body, author, and date.

            Parameters:
                html_content (str): The HTML content of the page.

            Returns:
                dict: A dictionary containing the article's title, body, author, and date.
        '''

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the article's title
        title = soup.title.string if soup.title else 'No Title'

        # Set article body to None
        body = "No body content found"

        # Set article author to None
        author = "No author found"

        # Set article date to None
        date = "No date found"

        # Extract the article's body
        try:
            body_selector = self.config['body_selector']
            
            if body_selector['type'] == 'class':
                body_element = soup.find(body_selector['element'], class_ = body_selector['text'])
            elif body_selector['type'] == 'id':
                body_element = soup.find(body_selector['element'], id = body_selector['text'])
            elif body_selector['type'] == 'css':
                body_element = soup.select(body_selector['text'])
            else:
                logger.error("Invalid body selector type. Please use 'class', 'id', or 'css'.")
            

            if body_element:
                # Extract the content of the article
                if body_element.find_all('p'):
                    body = ' '.join(p.get_text(separator=' ', strip=True) for p in body_element.find_all('p'))
                else:
                    body = ' '.join(div.get_text(separator=' ', strip=True) for div in body_element.find_all('div'))

            else:
                logger.warning("Body element not found.")

        except Exception as e:
            logger.error(f"An error occurred while extracting the body: {e}")

        # Extract the article's author
        if "author_selector" in self.config:
            try:
                author_selector = self.config['author_selector']

                if author_selector['type'] == 'class':
                    author_element = soup.find(author_selector['element'], class_ = author_selector['text'])
                elif author_selector['type'] == 'id':
                    author_element = soup.find(author_selector['element'], id = author_selector['text'])
                elif author_selector['type'] == 'css':
                    author_element = soup.select_one(author_selector['text'])
                else:
                    logger.error("Invalid author selector type. Please use 'class', 'id', or 'css'.")
                

                if author_element:
                    # Extract the author of the article
                    author = author_element.get_text(strip=True)
                else:
                    logger.warning("Author element not found.")
            except Exception as e:
                logger.error(f"An error occurred while extracting the author: {e}")

        # Extract the article's date
        if "date_selector" in self.config:
            try:
                date_selector = self.config['date_selector']

                if date_selector['type'] == 'class':
                    date_element = soup.find(date_selector['element'], class_ = date_selector['text'])
                elif date_selector['type'] == 'id':
                    date_element = soup.find(date_selector['element'], id = date_selector['text'])
                elif date_selector['type'] == 'css':
                    date_element = soup.select_one(date_selector['text'])
                else:
                    logger.error("Invalid date selector type. Please use 'class', 'id', or 'css'.")
                

                if date_element:
                    # Extract the date of the article
                    date = date_element.get_text(strip=True)
                else:
                    logger.warning("Date element not found.")
            except Exception as e:
                logger.error(f"An error occurred while extracting the date: {e}")

        return {
            "title": title,
            "body": body,
            "author": author,
            "date": date
        }