import unittest
from unittest.mock import patch, MagicMock
from parsers.dynamic_parser import DynamicParser

class TestDynamicParser(unittest.TestCase):

    def setUp(self):
        """
            Set up a sample configuration and DynamicParser instance for testing.
        """
        self.config = {
            'type': 'dynamic',
            'chrome_path': '/path/to/chrome',
            'body_selector': {
                'type': 'class',
                'element': 'div',
                'text': 'article-body'
            },
            'date_selector': {
                'type': 'class',
                'element': 'div',
                'text': 'article-date'
            },
            'author_selector': {
                'type': 'class',
                'element': 'div',
                'text': 'article-byline'
            },
            'sleep_time': 1
        }
        self.parser = DynamicParser(self.config)

    @patch('selenium.webdriver.Chrome')
    def test_fetch_content(self, mock_driver):
        """
            Test fetch_content method.
        """
        # Mock the driver
        driver = MagicMock()
        mock_driver.return_value = driver

        # Mock the driver.get method
        driver.get.return_value = None

        # Mock the driver.page_source
        driver.page_source = 'HTML content'

        # Test fetch_content method
        self.assertEqual(self.parser.fetch_content('http://www.example.com'), 'HTML content')

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