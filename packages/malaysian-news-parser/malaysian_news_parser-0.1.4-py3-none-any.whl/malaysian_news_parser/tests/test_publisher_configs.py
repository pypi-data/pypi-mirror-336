import unittest
from config.publisher_config import PublisherConfigManager

class TestPublisherConfigs(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case with initial configurations.
        """
        self.manager = PublisherConfigManager()
        self.new_publisher = {
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
        self.manager.add_publisher('new_publisher', self.new_publisher)

    def tearDown(self):
        """
        Clean up after each test case.
        """
        if 'new_publisher' in self.manager.publisher_configs:
            self.manager.remove_publisher('new_publisher')

    def test_add_publisher(self):
        """
        Test adding a new publisher configuration.
        """
        self.assertIn('new_publisher', self.manager.publisher_configs)

    def test_update_publisher(self):
        """
        Test updating an existing publisher configuration.
        """
        update_config = {'body_selector': {'type': 'id', 'element': 'div', 'text': 'new_body'}}
        self.manager.update_publisher('new_publisher', update_config)
        self.assertEqual(self.manager.publisher_configs['new_publisher']['body_selector'], {'type': 'id', 'element': 'div', 'text': 'new_body'})

    def test_remove_publisher(self):
        """
        Test removing a publisher configuration.
        """
        self.manager.remove_publisher('new_publisher')
        self.assertNotIn('new_publisher', self.manager.publisher_configs)

    def test_get_publisher_config(self):
        """
        Test retrieving a publisher configuration.
        """
        config = self.manager.get_publisher_config('new_publisher')
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main()
