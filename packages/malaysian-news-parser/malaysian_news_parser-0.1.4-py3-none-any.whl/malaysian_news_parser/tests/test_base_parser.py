import unittest
from malaysian_news_parser.base_parser import BaseParser
from unittest.mock import patch

class TestBaseParser(unittest.TestCase):

    def setUp(self):
        """
            Set up a sample configuration and BaseParser instance for testing.
        """
        self.config = {
            'type': 'static',
            'headers': {},
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
            }
        }
        self.parser = BaseParser(self.config)

    def test_validate_url(self):
        '''
            Test URL validation method.
        '''

        # Test valid URLs
        self.assertTrue(self.parser.validate_url('http://www.example.com'))
        self.assertTrue(self.parser.validate_url('https://www.example.com'))

        # Test invalid URLs
        self.assertFalse(self.parser.validate_url('www.example.com'))
        self.assertFalse(self.parser.validate_url('example.com'))

    def test_fetch_content(self):
        '''
            Test that fetch_content raises NotImplementedError.
        '''

        # Test that fetch_content raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.parser.fetch_content('http://www.example.com')

    def test_parse_content(self):
        '''
            Test that parse_content raises NotImplementedError.
        '''

        # Test that parse_content raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.parser.parse_content('<html></html>')

    @patch.object(BaseParser, 'fetch_content', side_effect=NotImplementedError)
    @patch.object(BaseParser, 'parse_content', side_effect=NotImplementedError)
    def test_get_article_data(self, mock_parse_content, mock_fetch_content):
        """
        Test that get_article_data calls fetch_content and parse_content, and handles errors.
        """
        # Configure the mock to raise NotImplementedError
        mock_fetch_content.side_effect = NotImplementedError
        mock_parse_content.side_effect = NotImplementedError

        # Validate URL to ensure the next part of the method is executed
        valid_url = 'http://example.com'
        self.assertTrue(self.parser.validate_url(valid_url))

        try:
            # Ensure NotImplementedError is raised by the method calls
            #self.parser.get_article_data(valid_url)
            print(self.parser.get_article_data(valid_url))
        except NotImplementedError as e:
            print(f"NotImplementedError was raised as expected: {e}")
        except Exception as e:
            print(f"Unexpected exception: {e}")

        # Check that fetch_content was called
        mock_fetch_content.assert_called_once_with(valid_url)
        # Check that parse_content was not called because fetch_content should raise the error first
        mock_parse_content.assert_not_called()

if __name__ == '__main__':
    unittest.main()


    