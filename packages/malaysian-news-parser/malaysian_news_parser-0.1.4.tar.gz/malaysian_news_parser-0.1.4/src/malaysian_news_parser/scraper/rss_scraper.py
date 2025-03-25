### src/malaysian_news_parser/scraper/rss_scraper.py ###

# A scraper that extracts article links from RSS feeds using the 'feedparser' library.

# Import libraries
import feedparser # RSS feed parser
from ..base_scraper import BaseScraper # Base Scraper

class RssScraper(BaseScraper):
    '''
        RssScraper class handles scraping RSS feeds and extracting article links.
    '''

    def fetch_content(self, rss_url):
        '''
            Fetches the RSS feed content from the given URL using feedparser.

            Args:
                rss_url (str): The URL of the RSS feed.

            Returns:
                dict: The parsed RSS feed content.
        '''

        try:

            # Parse the RSS feed from the URL
            feed = feedparser.parse(rss_url)

            return feed
        
        except Exception as e:

            # Print the exception if an error occurs
            print(f"Error fetching RSS feed content: {e}")
            return
        
    def extract_article_links(self, rss_content):
        '''
            Extract article links from the parsed RSS feed content.

            Args:
                rss_content (dict): The parsed RSS feed content.

            Returns:
                list: A list of article link dictionary objects.
                format: [{'link': 'article_link', 'content': 'article_content'}, ...]
        '''

        try:

            # Extract article links from the parsed feed content
            entries = [entry.link for entry in rss_content.entries]

            return entries
        
        except Exception as e:

            # Print the exception if an error occurs
            print(f"Error extracting article links from RSS feed content: {e}")
            return []