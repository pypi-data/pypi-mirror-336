from setuptools import setup, find_packages

setup(
    name='malaysian_news_parser', # change to appropriate name
    version='0.1.4',
    author='Squimptech',
    author_email='enquiry@squimptech.com',
    description= 'A python library for parsing news articles',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/squimptech/Malaysian_News_Parser',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium'
    ],
    tests_require=[
        'unittest',
        'mock'
    ],
    test_suite='src.tests'
)