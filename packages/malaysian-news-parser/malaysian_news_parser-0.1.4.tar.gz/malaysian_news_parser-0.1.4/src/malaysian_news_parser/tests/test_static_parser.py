import unittest
import requests_mock
from parsers.static_parser import StaticParser

class TestStaticParser(unittest.TestCase):

    def setUp(self):
        '''
            Set up a sample configuration and StaticParser instance for testing.
        '''

        self.config = {
            'type': 'static',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            },
            'body_selector': {
                "type": "class",
                "element": "div",
                "text": "article-body"
            },
            "date_selector": {
                "type": "class",
                "element": "div",
                "text": "article-date"
            },
            "author_selector": {
                "type": "class",
                "element": "div",
                "text": "article-byline"
            }
        }

        self.parser = StaticParser(self.config)

    @requests_mock.Mocker()
    def test_fetch_content(self, m):
        '''
            Test fetch_content method.
        '''

        # Mock the request
        m.get('http://www.example.com', text='<html></html>')

        # parse content
        html_content = self.parser.fetch_content('http://www.example.com')

        # Test fetch_content method
        self.assertEqual(html_content, '<html></html>')

    def test_parse_content(self):
        """
        Test parsing HTML content to extract title, body, author, and date.
        """
        html_content = '''
        <html>
            <head><title>Test Title</title></head>
            <body>
                <div class="article-body"><p>Test Body</p></div>
                <div class="article-date">Test Date</div>
                <div class="article-byline">Test Author</div>
            </body>
        </html>
        '''
        expected_output = {
            'title': 'Test Title',
            'body': 'Test Body',
            'author': 'Test Author',
            'date': 'Test Date'
        }
        self.assertEqual(self.parser.parse_content(html_content), expected_output)

if __name__ == '__main__':
    unittest.main()