### src/malaysian_news_parser/parsers/rss_parser.py ###

# In situations where the content is on the RSS feed this 
# parser can be used directly to extract links, content, and other relevant details

# Import libraries
import feedparser # RSS feed parser
import re # Regular expression operations
from ..base_parser import BaseParser # Base Parser

class RssParser(BaseParser):
    '''
        RssParser class handles parsing RSS feeds and extracting article content.
    '''
    def fetch_content(self, url):
        '''
            Fetches the RSS feed content from the given URL using feedparser.

            Args:
                url (str): The URL of the RSS feed.

            Returns:
                dict: The parsed RSS feed content.
        '''

        try:

            # Parse the RSS feed from the URL
            feed = feedparser.parse(url)

            return feed
        
        except Exception as e:

            # Print the exception if an error occurs
            print(f"Error fetching RSS feed content: {e}")
            print("error in fetch content")
            return None
        
    def parse_content(self, rss_content):
        '''
            Parse the RSS feed content to extract article details.

            Args:
                rss_content (dict): The parsed RSS feed content.

            Returns:
                list: A list of article dictionary objects.
                format: [{'title': 'article_title', 'content': 'article_content'}, ...]
        '''
        print(type(rss_content))
        try:

            # Extract article details from the parsed feed content
            articles = []

            # declare feed entries
            entries = rss_content.entries

            # iterate through feed entries
            for entry in entries:

                # create a list of tags in the entry
                tags = entry.keys()
                
                # if 'content' is in the tags
                if 'content' in entry:

                    # Get the tag that has the word 'content' in it
                    content_tag = [tag for tag in tags if 'content' in tag][0]
                    print('content found')

                # if 'description' is in the tags
                elif 'description' in entry:

                    # Get the tag that has the word 'description' in it
                    content_tag = [tag for tag in tags if 'description' in tag][0]
                    print('description found')

                # if 'summary' is in the tags
                elif 'summary' in entry:

                    # Get the tag that has the word 'summary' in it
                    content_tag = [tag for tag in tags if 'summary' in tag][0]
                    print('summary found')

                else:

                    print('No content found')
                    content_tag = None

                # if a content tag is found
                if content_tag:

                    # extract the title
                    title = entry.title

                    # extract the content with the content tag
                    content = entry[content_tag]

                    # remove html tags from the content
                    content = self.remove_html_tags(content)

                    print(content)

                # append the extracted details to the articles list
                articles.append({'title': title, 'content': content})

            return articles
        
        except Exception as e:

            # Print the exception if an error occurs
            print(f"Error parsing RSS feed content: {e}")
            print("error in parse content")
            return []

    def remove_html_tags(self, text):
        '''
            Remove HTML tags from the text.

            Args:
                text (str): The text containing HTML tags.

            Returns:
                str: The text with HTML tags removed.
        '''


        # Remove HTML tags using regex
        text = re.sub('<.*?>', '', text[0]['value'])

        # Replace multiple newlines with a single newline
        text = re.sub(r'\s*\n\s*', '\n', text)

        # Strip leading/trailing whitespace and remove any extra newlines at the start/end
        text = text.strip()

        return text