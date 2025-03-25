### src/malaysian_news_parser/scraper/requests_scraper.py ###
# A scraper that extracts article links from static websites using requests and BeautifulSoup.

# Import libraries
import requests # HTTP requests
from ..base_scraper import BaseScraper # Base Scraper
from bs4 import BeautifulSoup # HTML parsing

class RequestsScraper(BaseScraper):
    '''
        RequestsScraper class handles scraping static websites by sending HTTP requests and
        using BeautifulSoup to parse the HTML and extract article links.
    '''

    def fetch_content(self, url):
        '''
            Fetches the HTML content of the given URL using requests.

            Args:
                url (str): The URL of the page to fetch.

            Returns:
                str: The HTML content of the page if the request is successful.
        '''

        # Load Scrape Configs
        scrapeConfigs = self.config['link_scrape_config']

        # Get the iterate_pages flag from the scrapeConfigs
        iterate_pages = scrapeConfigs['iterate_pages']

        # empty list for page content
        page_content = []

        try:
                
                # if the iterate_pages flag is set to True, iterate through multiple pages
                if iterate_pages:

                    # Get the maximum number of pages to iterate through
                    max_pages = scrapeConfigs['max_pages']
    
                    # Iterate through each page in the range of max pages
                    for pageNo in range(max_pages):
    
                        # construct the url
                        new_url = self.construct_url(url, pageNo)
    
                        # Send a GET request to the URL
                        response = requests.get(new_url)
    
                        # Raise an exception if the status code is not 200
                        response.raise_for_status()
    
                        # Append the HTML content of the page to the list of page content
                        page_content.append(response.text)
    
                        # if max pages is reached, break the loop
                        if pageNo >= max_pages:
                            print(f'Maximum number of pages reached: {max_pages}')
                            break

                    return page_content
    
                else:
                        
                    # Send a GET request to the URL
                    response = requests.get(url)
    
                    # Raise an exception if the status code is not 200
                    response.raise_for_status()
    
                    # Append the HTML content of the page to the list of page content
                    page_content.append(response.text)

                    return page_content
    
                
        
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors (e.g., 404, 500)
            print(f"HTTP error occurred: {http_err}")
            return []

        except Exception as e:
            # Handle any other errors (network, parsing, etc.)
            print(f"Error occurred while scraping {url}: {e}")
            return []
    

    def extract_article_links(self, html_content):
        '''
            Extracts article links from the parsed HTML content using BeautifulSoup.

            Args:
                soup (BeautifulSoup): The parsed HTML content of the page.

            Returns:
                list: A list of article link dictionary objects.
                format: [{'link': 'article_link', 'content': 'article_content'}, ...]
        '''
        
        # Get config paramaters for link scraping
        config = self.config['link_scrape_config']['link_selector']

        # Initialize soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize empty list of links
        links = []

        # if the selector is a class
        if config['selector_type'] == 'class':

            # Find all elements with the specified class
            articles = soup.find_all(config['element'], class_=config['text'])
        
        # else if the selector is an id
        elif config['selector_type'] == 'id':

            # Find the element with the specified id
            articles = soup.find_all(config['element'], id=config['text'])

        # else if the selector is a css selector
        elif config['selector_type'] == 'css':

            # Find all elements that match the CSS selector
            articles = soup.select(config['text'])

        # Extract article links using BeautifulSoup
        for article in articles:

            # find the article a tag
            a_tag = article.find('a')

            # if the a tag and href attribute exist
            if a_tag and a_tag['href']:

                # Append the link to the list of links
                links.append({'link': a_tag['href']})

        return links


    def construct_url(self, url, page):
        '''
            Constructs a URL for a specific page number by replacing the page number in the URL.

            Args:
                url (str): The base URL with a placeholder for the page number.
                page (int): The page number to insert into the URL.

            Returns:
                str: The constructed URL with the page number.
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
