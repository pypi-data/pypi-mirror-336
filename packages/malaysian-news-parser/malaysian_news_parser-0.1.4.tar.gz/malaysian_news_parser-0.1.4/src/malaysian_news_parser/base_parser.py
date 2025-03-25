from requests.exceptions import RequestException
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseParser:
    def __init__(self, config):
        '''
            Initializes the BaseParser with the provided configuration.

            Parameters:
                config (dict): Configuration dictionary for the parser.
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
            Fetches the content of the given URL.

            Parameters:
                url (str): The URL to fetch the content from.

            Returns:
                str: The HTML content of the page if the request is successful.
        '''

        raise NotImplementedError("fetch_content method must be implemented in the derived class.")
    
    def parse_content(self, html_content):
        '''
            Parses the HTML content to extract relevant data.

            Parameters:
                html_content (str): The HTML content of the page.

            Returns:
                dict: A dictionary containing the extracted data.
        '''

        raise NotImplementedError("parse_content method must be implemented in the derived class.")
    
    def get_article_data(self, url):
        '''
            Retrieves the article data from the given URL.

            Parameters:
                url (str): The URL of the article.

            Returns:
                dict: A dictionary containing the article if successful, None otherwise.
        '''

        # Validate the URL
        if not self.validate_url(url):
            logger.error("Invalid URL provided.")
            return None
        
        try:
            logger.debug("Fetching content from URL: %s", url)
            # Fetch the content of the URL
            content = self.fetch_content(url)
            logger.debug("Content fetched successfully")

            # Parse the content to extract the article data
            if content:
                logger.debug("Parsing content")
                return self.parse_content(content)
            else:
                logger.error("Failed to fetch content from the URL.")
                return None
            
        except NotImplementedError:
            raise  # Let NotImplementedError propagate
        
        except RequestException as e:
            logger.error(f"An error occurred while fetching the content: {e}")
            return None
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None