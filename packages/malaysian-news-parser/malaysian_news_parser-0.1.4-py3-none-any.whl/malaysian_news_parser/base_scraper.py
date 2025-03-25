from requests.exceptions import RequestException
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper:

    def __init__(self, config):
        '''
            Initializes the BaseScraper with the provided configuration.

            Parameters:
                config (dict): Configuration dictionary for the scraper.
        '''
        self.config = config

    def validate_url(self, url):
        '''
            Validate the given URL.

            Parameters:
                url (str): The URL to validate

            Returns:
                bool: True if the URL is valid, False otherwise.
        '''

        # Check if the URL is valid with regex
        regex = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:\S+(?::\S*)?@)?'  # optional user:password@
            r'(?:[A-Za-z0-9.-]+|\[[A-Fa-f0-9:]+\])'  # domain or IP
            r'(?::\d{2,5})?'  # optional port
            r'(?:[/?#]\S*)?$', re.IGNORECASE)
        
        return re.match(regex, url) is not None

    def fetch_content(self, url):
        '''
            Extracts the links from the given URL.

            Parameters:
                url (str): The URL to extract links from.

            Returns:
                list: A list of extracted links.
        '''

        raise NotImplementedError("extract_links method must be implemented in the derived class.")
    
    def extract_article_links(self, url):
        '''
            Extract article links from the given URL.

            Parameters:
                url (str): The URL to extract article links from.

            Returns:
                list: A list of article links.
        '''

        raise NotImplementedError("extract_article_links method must be implemented in the derived class.")

    def get_links(self, url):
        '''
            Get article links from the given URL.

            Parameters:
                url (str): The URL to get article links from.

            Returns:
                list: A list of article links.
        '''

        # Validate the URL
        if not self.validate_url(url):
            logger.error("Invalid URL")
            return None
        
        try:
            logger.debug(f"Extracting links from {url}")
            page_content = self.fetch_content(url)

            if page_content:

                print(type(page_content))
                print(len(page_content))
                links = self.extract_article_links(page_content)

                logger.info(f"Found {len(links)} links")
                
                # if not self.validate_url(links[0]):
                #     logger.error("Invalid link found")
                #     return None

                return links
            
            else:
                logger.warning("No links found")
                return None
            
        except RequestException as e:
            logger.error(f"Request error for URL: {url} - {e}")
            raise

        except NotImplementedError as e:
            logger.error(f"Method not implemented: {e}")
            raise

        except Exception as e:
            logger.error(f"An error occurred while extracting links: {e}")
            raise

