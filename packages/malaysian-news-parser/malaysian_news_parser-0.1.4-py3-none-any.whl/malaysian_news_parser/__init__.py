from .base_parser import BaseParser
from .parsers.static_parser import StaticParser
from .parsers.dynamic_parser import DynamicParser
from .parsers.rss_parser import RssParser
from .scraper.rss_scraper import RssScraper
from .scraper.requests_scraper import RequestsScraper
from .scraper.selenium_scraper import SeleniumScraper
from .config.publisher_config import PublisherConfigManager

config_manager = PublisherConfigManager()

def get_parser(publisher_name):
    config = config_manager.get_publisher_config(publisher_name)

    if not config:
        raise ValueError(f"Publisher {publisher_name} not found in the configuration.")
    
    if config['type'] == 'static':
        return StaticParser(config)
    elif config['type'] == 'dynamic':
        return DynamicParser(config)
    elif config['type'] == 'rss':
        return RssParser(config)
    else:
        raise ValueError(f"Unsupported parser type {config['type']} for publisher {publisher_name}.")
    
def get_scraper(publisher_name):
    config = config_manager.get_publisher_config(publisher_name)

    if not config:
        raise ValueError(f"Publisher {publisher_name} not found in the configuration.")
    
    if config['link_scrape_config']['type'] == 'static':
        return RequestsScraper(config)
    elif config['link_scrape_config']['type'] == 'dynamic':
        return SeleniumScraper(config)
    elif config['link_scrape_config']['type'] == 'rss':
        return RssScraper(config)
    else:
        raise ValueError(f"Unsupported parser type {config['type']} for publisher {publisher_name}.")