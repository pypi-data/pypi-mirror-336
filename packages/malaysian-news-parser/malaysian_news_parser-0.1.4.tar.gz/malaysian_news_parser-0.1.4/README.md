# Malaysian News Parser

![Python Version](https://img.shields.io/badge/python3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

The Malaysian News Parser, is a python library for extracting and parsing news articles from multiple
publishers. It supports both static and dynamic content parsing using BeautifulSoup and Selenium.
This parser was developed with a focus on Malaysian news publishers, but this may work with other
news organizations provided it is allowed.

<p align="center">
  <img src="https://your-image-url-here.png" alt="Parser Dev Logo" width="200"/>
</p>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [Initializing the Config Manager](#initializing-the-config-manager)
    - [Adding a Publisher](#adding-a-publisher)
    - [Updating a Publisher](#updating-a-publisher)
    - [Removing a Publisher](#removing-a-publisher)
    - [Retrieving Article Data](#retrieving-article-data)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)


## Installation

<p>You can install the library using pip</p>

```sh
pip install parser_dev
```

## Usage

### Initializing the Config Manager

<p>Before using the library, you need to initialize the `PublisherConfigManager`:</p>

<p>This can be done by importing the manager from `publisher_configs`, and then initializing an instance of the manager</p>

```python
from parser_dev.publisher_config import PublisherConfigManager # Import Manager

# Initialize Manager instance
config_manager = PublisherConfigManager()
```

<p>This was set as a global variable in the usage tests</p>

### Adding a Publisher

<p>There are slight format differences between setting the publisher configuration for static and dynamic sites.</p>

<p>Static Publisher Config Format: </p>

```python
static_publisher_config = {
    'type': 'static', # For static, set this to static
    'headers': { # Only present for website types that are static. Omitted for Dynamic
        'header_name': 'header_value'
    },
    'body_selector': { # Article Body Selector info for beautiful soup
        'type': 'class, id, css'
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    },
    'date_selector': { # Article Date Selector info for beautiful soup
        'type': 'class, id, css',
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    },
    'author_selector': { # Article Author Selector info for beautiful soup
        'type': 'class, id, css',
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    }
}
```

<p>Dynamic Publisher Config Format: </p>

```python
# Headers omitted, chrome_path and sleep_time added.
dynamic_publisher_config = {
    'type': 'dynamic', # For dynamic, set this to dynamic
    'chrome_path': os.getenv('CHROME_PATH') # your path to your Selenium compatible webdriver (set in your .env file)
        'body_selector': { # Article Body Selector info for beautiful soup
        'type': 'class, id, css'
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    },
    'date_selector': { # Article Date Selector info for beautiful soup
        'type': 'class, id, css',
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    },
    'author_selector': { # Article Author Selector info for beautiful soup
        'type': 'class, id, css',
        'element': '<div>, <article>, etc..., not required for css selector',
        'text': 'selector_text'
    },
    'sleep_time': 10, # set how long the webdriver should wait to render page, dtype: int
}
```

<p>To add a new publisher configuration:</p>

```python
from parser_dev.publisher_config import PublisherConfigManager # Import Manager

# Initialize Manager instance
config_manager = PublisherConfigManager()

# desired new publisher configuration
new_publisher_config = {
    'type': 'static',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },
    'body_selector': {
        'type': 'css',
        'element': 'div',
        'text': '#new-body-selector',
    },
    'date_selector': {
        'type': 'css',
        'element': 'div',
        'text': '#new-date-selector',
    }
}

config_manager.add_publisher('new_publisher', new_publisher_config)
```

### Updating a Publisher

<p>To update an existing publisher configuration: </p>

```python
update_publisher_config = {
    'body_selector': {
        'type': 'css',
        'text': 'body > main > section > div > div > div > section > div:nth-of-type(1) > strong',
    }
}

config_manager.update_publisher('new_publisher', update_publisher_config)
```

### Remove a Publisher

<p>To remove a publisher configuration: </p>

```python
config_manager.remove_publisher('new_publisher')
```

### Retrieving Article Data

<p>The existing publisher config names</p>

<table>
    <tr>
        <th>
            Publisher
        </th>
        <th>
            Name in Config
        </th>
    </tr>
    <tr>
        <td>
            Astro Awani
        </td>
        <td>
            astro_awani
        </td>
    </tr>
    <tr>
        <td>
            Malay Mail
        </td>
        <td>
            malay_mail
        </td>
    </tr>
    <tr>
        <td>
            Star
        </td>
        <td>
            star
        </td>
    </tr>
    <tr>
        <td>
            Sun Daily
        </td>
        <td>
            sun_daily
        </td>
    </tr>
    <tr>
        <td>
            FMT (Free Malaysia Today)
        </td>
        <td>
            fmt
        </td>
    </tr>
    <tr>
        <td>
            Sinar Harian
        </td>
        <td>
            sinar_harian
        </td>
    </tr>
    <tr>
        <td>
            Berita Harian
        </td>
        <td>
            berita_harian
        </td>
    </tr>
    <tr>
        <td>
            Roti Kaya
        </td>
        <td>
            roti_kaya
        </td>
    </tr>
    <tr>
        <td>
            New Straits Times
        </td>
        <td>
            nst
        </td>
    </tr>
    <tr>
        <td>
            The Vibes
        </td>
        <td>
            the_vibes
        </td>
    </tr>
    <tr>
        <td>
            World of Buzz
        </td>
        <td>
            world_of_buzz
        </td>
    </tr>
    <tr>
        <td>
            Bernama
        </td>
        <td>
            bernama
        </td>
    </tr>
    <tr>
        <td>
            Cili Sos
        </td>
        <td>
            cili_sos
        </td>
    </tr>
    <tr>
        <td>
            Coconuts
        </td>
        <td>
            coconuts
        </td>
    </tr>
    <tr>
        <td>
            The Edge
        </td>
        <td>
            the_edge
        </td>
    </tr>
    <tr>
        <td>
            HMetro
        </td>
        <td>
            hmetro
        </td>
    </tr>
    <tr>
        <td>
            Malaysian Gazette
        </td>
        <td>
            malaysia_gazette
        </td>
    </tr>
    <tr>
        <td>
            Harakah Daily
        </td>
        <td>
            harakah_daily
        </td>
    </tr>
    <tr>
        <td>
            Borneo Post
        </td>
        <td>
            borneo_post
        </td>
    </tr>
</table>

<p>To retrieve article data from a given URL: </p>

```python
from parser_dev import get_parser

# url of article
url = 'https://www.astroawani.com/berita-malaysia/pelajar-cemerlang-spm-dijamin-tempat-matrikulasi-atau-program-kpt-kpm-477101'

# publisher name
publisher_name = 'astro_awani'

# Get appropriate parser
parser = get_parser(publisher_name)

# Extract and parse article data
article_data = parser.get_article_data(url)

if article_data:
    print(f"Title: {article_data['title']}")
    print(f"Author: {article_data['author']}")
    print(f"Date: {article_data['date']}")
    print(f"Body: {article_data['body'][:1000]}")  # Print the first 1000 characters to keep it concise
else:
    print("Failed to fetch or parse article data.")
```

## Testing

<p>To run the tests, navigate to the project directory and use `unittest`:</p>

```sh
python -m unittest discover -s src/tests
```

## Contributing

<p>We welcome contributions! Please follow these steps:</p>

<ol>
    <li>Fork the Repository</li>
    <li>Create a new branch: `git checkout -b feature/your-feature-name</li>
    <li>Make your changes and commit them: `git commit -m 'Add some feature'</li>
    <li>Push to the branch: `git push origin feature/your-feature-name`</li>
    <li>Submit a pull request.</li>
</ol>

<p>Please make sure to update tests as appropriate.</p>

## License

<p>This project is licensed under the MIT License. See the LICENSE file for details.</p>