### src/malaysian_news_parser/scraper/scraper.py ###

# Main file that orchestrates which scraper to use (RSS, static, or dynamic with Selenium)

# Import libraries
from .rss_scraper import RssScraper # RSS Link Scraper
from .requests_scraper import RequestsScraper # Static Scraper
from .selenium_scraper import SeleniumScraper # Dynamic Scraper

class NewsScraper:
    '''
        NewsScraper class handles the decision-making process of which scraper 
        (RSS, static, or dynamic) to use based on the type of source (RSS feed, static site, or dynamic site).
    '''

    def __init__(self):
        '''
            Initialize the NewsScraper class.
        '''
        
        # Initialize RSS Scraper
        self.rss_scraper = RssScraper()

        # Initialize Static Scraper
        self.requests_scraper = RequestsScraper()

        # Initialize Dynamic Scraper
        self.selenium_scraper = SeleniumScraper()


    def scrape(self, source_type, url_or_driver):
        '''
            Chooses the appropriate scraping method based on the source type.

            Args:
                source_type (str): The type of source to scrape.
                url_or_driver (str or WebDriver): The URL of the page to scrape or a Selenium WebDriver instance.

            Returns:
                list: A list of article links extracted from the source.

        '''

        # Check if the source type is RSS
        if source_type == 'rss':

            # Call the RSS scraper when the source type is an RSS feed
            return self.rss_scraper.extract_links(url_or_driver)
        
        # Check if the source type is static
        elif source_type == 'static':

            # Call the static scraper when the source type is a static site
            return self.requests_scraper.extract_links(url_or_driver)

        # Check if the source type is dynamic
        elif source_type == 'dynamic':

            # Call the dynamic scraper when the source type is a dynamic site
            return self.selenium_scraper.extract_links(url_or_driver)
        
        # If the source type is not recognized raise a ValueError
        else:

            # Raise a ValueError if the source type is not recognized
            raise ValueError(f'Source type not recognized {source_type}. Please use either "rss", "static", or "dynamic".')
