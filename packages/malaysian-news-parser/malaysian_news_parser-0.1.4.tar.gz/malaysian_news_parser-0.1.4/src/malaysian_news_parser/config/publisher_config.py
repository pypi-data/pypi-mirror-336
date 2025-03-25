import os
from dotenv import load_dotenv

load_dotenv()

class PublisherConfigManager:
    def __init__(self):
        self.publisher_configs = {
            "belt_and_road": {
                "link_scrape_config": {
                    "type": "dynamic",
                    "url": 'https://eng.yidaiyilu.gov.cn/news',
                    "has_content": False,
                    "simulate_click": True,
                    "iterate_pages": False,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "media-body"
                    }
                },
                "chrome_path": os.getenv('CHROME_PATH'),
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "desc-left"
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "news-details-content"
                }
            },
            "astro_awani": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://rss.astroawani.com/rss/national/public"],
                    "has_content": False,
                },
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "article",
                    "text": "styledComponents__ArticleContent-sc-1ym9iti-12"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "styledComponents__ArticleDate-sc-1ym9iti-8",
                },
                "author_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "styledComponents__Author-sc-1ym9iti-7"
                },
                "sleep_time": 10,
            },
            "malay_mail": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://www.malaymail.com/feed/rss/malaysia"],
                    "has_content": True,
                },
                "type": "rss",
                "selectors": {
                    "title": "title",
                    "link": "link",
                    "content": "content:encoded",
                    "date": "pubDate",
                }
            },
            "star": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://www.thestar.com.my/news/latest?{page_iterator}tag=Nation#Latest"],
                    "page_iterator": "?pgno={pageNo}&",
                    'max_pages': 5,
                    "iterate_pages": True,
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "h2",
                        "text": "f18"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "story-body"
                },
                "date_selector": {
                    "type": "class",
                    "element": "p",
                    "text": "date",
                }
            },
            "sun_daily": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://www.thesundaily.my/rss/local"],
                    "has_content": True,
                },
                "type": "rss",
                "selectors": {
                    "title": "title",
                    "link": "link",
                    "content": "description",
                    "date": "pubDate",
                }
            },
            "fmt": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://cms.freemalaysiatoday.com/feed/"],
                    "has_content": True,
                },
                "type": "rss",
                "selectors": {
                    "title": "title",
                    "link": "link",
                    "content": "content:encoded",
                    "date": "pubDate",
                    "author": "dc:creator",
                }
            },
            "sinar_harian": {
                "link_scrape_config": {
                    "type": "dynamic",
                    "url": ["https://www.sinarharian.com.my/nasional"],
                    "has_content": False,
                    "simulate_click": True,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "article-title",
                    },
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "articleText",
                },
                "date_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "timespan",
                },
                "author_selector": {
                    "type": "class",
                    "element": "a",
                    "text": "authorName",
                },
            },
            "berita_harian": {
                "link_scrape_config": {
                    "type": "dynamic",
                    "url": [
                        "https://www.bharian.com.my/berita/kes",
                        "https://www.bharian.com.my/berita/nasional/{page_iterator}",
                        "https://www.bharian.com.my/berita/politik",
                        "https://www.bharian.com.my/berita/wilayah",
                    ],
                    "page_iterator": "?page={pageNo}",
                    "has_content": False,
                    "iterate_pages": True,
                    "max_pages": 5,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "article-teaser"
                    }
                },
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content"
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div > span > a",
                },
                "sleep_time": 5,
            },
            "roti_kaya": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://rotikaya.com/"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "h4",
                        "text": "post-title"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "article",
                    "text": "the-content",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > main > section > div > div > div > section > div:nth-of-type(2)",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > main > section > div > div > div > section > div:nth-of-type(1) > strong",
                },
            },
            "nst": {
                "link_scrape_config": {
                    "type": "static",
                    "url": [
                        "https://www.nst.com.my/news/nation/{page_iterator}", 
                        "https://www.nst.com.my/news/nst-viral", 
                        "https://www.nst.com.my/news/politics",
                    ],
                    "has_content": False,
                    "page_iterator": "?page={pageNo}",
                    "iterate_pages": True,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "article-listing"
                    }
                },
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div > span > a",
                },
                "sleep_time": 5,
            },
            "the_vibes": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://www.thevibes.com/articles/news{page_iterator}"],
                    "has_content": False,
                    "page_iterator": "?page={pageNo}",
                    "iterate_pages": True,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "item"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "body",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > section > div:nth-of-type(1) > div > div > p:nth-of-type(2)",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > section > div:nth-of-type(1) > div > div > p:nth-of-type(1)",
                },
            },
            "world_of_buzz": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://worldofbuzz.com/latest-news/"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "li",
                        "text": "mvp-blog-story-wrap"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "mvp-content-main",
                },
                "date_selector": {
                    "type": "css",
                    "text": "#mvp-post-head > div > div.mvp-author-info-text.left.relative > div.mvp-author-info-date.left.relative > span.mvp-post-date.updated > time",
                },
                "author_selector": {
                    "type": "css",
                    "text": "#mvp-post-head > div > div.mvp-author-info-text.left.relative > div.mvp-author-info-name.left.relative > span > a",
                }
            },
            "bernama": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://www.bernama.com/en/rssfeed.php"],
                    "has_content": False
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "css",
                    "text": "#body-row > div > div.container.px-0.my-0 > div > div.col-12.col-sm-12.col-md-12.col-lg-8",
                },
                "date_selector": {
                    "type": "css",
                    "text": "#body-row > div > div.container.px-0.my-0 > div > div.col-12.col-sm-12.col-md-12.col-lg-8 > div.col-12.mt-3.mb-3 > div"
                }
            },
            "cili_sos": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://cilisos.my/category/current/"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "h3",
                        "text": "entry-title"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "entry-content",
                },
                "date_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "entry-meta-date"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "author"
                }
            },
            # "coconuts": {
            #     "link_scrape_config": {
            #         "type": "static",
            #         "url": ["https://coconuts.co/kl/news/"],
            #         "has_content": False,
            #         "link_selector": {
            #             "type": "class",
            #             "element": "h3",
            #             "text": "entry-title"
            #         }
            #     },
            #     "type": "static",
            #     "headers": {
            #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            #         # 'Accept-Language': 'en-US,en;q=0.9',
            #         # 'Accept-Encoding': 'gzip, deflate, br',
            #         # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #         # 'Connection': 'keep-alive',
            #         # 'Upgrade-Insecure-Requests': '1',
            #     },
            #     "body_selector": {
            #         "type": "class",
            #         "element": "div",
            #         "text": "coco_post-content",
            #     },
            #     "date_selector": {
            #         "type": "class",
            #         "element": "span",
            #         "text": "post-timeago",
            #     },
            #     "author_selector": {
            #         "type": "css",
            #         "text": "#main-content > div > main > div.post-sheet > div.section-wrap > div > div > div.col-md-8.col-content.main-stream-content.pos-relative > div.coco_post-meta.d-md-flex.justify-content-between.align-items-center > div > span > a",
            #     },
            # },
            # "the_edge": {
            #     "link_scrape_config": {
            #         "type": "dynamic",
            #         "url": ["https://www.theedgemarkets.com/categories/malaysia"],
            #         "has_content": False,
            #         "link_selector": {
            #             ""
            #     "type": "dynamic",
            #     "chrome_path": os.getenv('CHROME_PATH'),
            #     "body_selector": {
            #         "type": "class",
            #         "element": "div",
            #         "text": "news-detail_newsTextDataWrap__PkAu5",
            #     },
            #     "date_selector": {
            #         "type": "css",
            #         "text": "#__next > div > div > div > div > div.news-detail_articleContainerWrapper__pE31f > div:nth-child(1) > div > div.news-detail_pageWrapperContent__QWIfQ > div > div.news-detail_newsdetailsContent__Fey_B > div.news-detail_newsDetailsItemWrap___HS1t > div.news-detail_newsdetailsItemInfo__g9Hsi > div.news-detail_newsInfo__dv0be > span",
            #     },
            #     "sleep_time": 5,
            # },
            "hmetro": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://www.hmetro.com.my/mutakhir.xml"],
                    "has_content": False,
                },
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "published-date"
                },
                "author_selector": {
                    "type": "css",
                    "text": "#main > div > div.row > div.col > div:nth-child(1) > div > div > div.d-block.d-lg-flex.mb-3 > div.article-meta.mb-2.mb-lg-0.d-flex.align-items-center > div > span > a",
                },
            },
            "malaysia_gazette": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://malaysiagazette.com/category/nasional/{page_iterator}"],
                    "page_iterator": "page/{pageNo}/",
                    "iterate_pages": True,
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "td-module-thumb"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "td-post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "entry-date updated td-module-date"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "td-post-author-name"
                },
            },
            "harakah_daily": {
                "link_scrape_config": {
                    "type": "static",
                    "url": ["https://harakahdaily.net/index.php/terkini/"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "td-module-thumb"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "td-post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "entry-date updated td-module-date"
                },
            },
            "borneo_post": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ["https://www.theborneopost.com/feed/"],
                    "has_content": True,
                    "selectors": {
                        "title": "title",
                        "link": "link",
                        "content": "content:encoded",
                        "date": "pubDate",
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "value-title"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "reviewer"
                },
            },
            "malaysiakini":{
                "link_scrape_config": {
                    "type": "static",
                    "url":["https://www.malaysiakini.com/news"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "cursor-pointer"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "published"
                },
                "author_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "author"
                },
            },
            "malaysian_insight":{
                "link_scrape_config": {
                    "type": "rss",
                    "url":["https://www.themalaysianinsight.com/feed"],
                    "has_content": False,
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "published"
                },
                "author_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "author"
                },
            },
            "leaders_online": {
                "link_scrape_config": {
                    "type": "static",
                    "url":["https://theleaders-online.com/category/malaysia/page/{pageNo}/"],
                    "has_content": False,
                    "link_selector": {
                        "type": "class",
                        "element": "div",
                        "text": "item-content"
                    }
                },
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "entry-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "entry-date published"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "author vcard"
                },
            },
            "utusan": {
                "link_scrape_config": {
                    "type": "rss",
                    "url": ['https://www.utusan.com.my/feed/'],
                    "has_content": True,
                },
            },
            
        }


    def add_publisher(self, name, config):
        '''
            Adds a new publisher configuration.

            Parameters:
                name (str): The name of the publisher.
                config (dict): The configuration for the publisher.
        '''

        # Add the new publisher configuration
        if name in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' already exists.")
        
        #print(self.publisher_configs[name])
        self.publisher_configs[name] = config

    def update_publisher(self, name, config):
        '''
            Updates an existing publisher configuration

            Parameters:
                name (str): The name of the publisher.
                config (dict): The new configuration for the publisher.
        '''

        # Update the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        self.publisher_configs[name].update(config)

    def remove_publisher(self, name):
        '''
            Removes a publisher configuration.

            Parameters:
                name (str): The name of the publisher.
        '''

        # Remove the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        del self.publisher_configs[name]

    def get_publisher_config(self, name):
        '''
            Returns the configuration for the specified publisher.

            Parameters:
                name (str): The name of the publisher.

            Returns:
                dict: The configuration for the specified publisher.
        '''

        # Get the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        return self.publisher_configs[name]

