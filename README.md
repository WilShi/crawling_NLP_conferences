# crawling_NLP_conferences
Crawl three internationally renowned `Natural Language Processing` (NLP) conferences and analyze the diversity of participants in the three conferences over the past 10 years.

This software calls `Beautiful Soup 4`, `requests` and `pandas` library to parse the HTML code of the website, and automatically recognizes the navigation bar of the website to analyze pages that may contain names. After finding a website that may contain a name, it automatically crawls the names and related information on the page. After the software confirms to crawl the webpage information of the year, it will automatically find the previous conference websites of the conference, and crawl the information year by year (10 years). 

The current crawling targets of the software are three conferences:

`Association for Computational Linguistics (ACL)`: https://www.aclweb.org/anthology/venues/acl/

`Empirical Methods in Natural Language Processing (and forerunners) (EMNLP)`: https://www.aclweb.org/anthology/venues/emnlp/

`North American Chapter of the Association for Computational Linguistics (NAACL)`: https://www.aclweb.org/anthology/venues/naacl/

The software consists of three python programs: `scraping_nlp.py`, `analysis_nlp.py` and `hypothesis_test.py`. 

`scraping_nlp.py` will automatically crawl the aforementioned webpage information, and when the result is obtained, it will print the person’s name and information to the terminal command line. 

`analysis_nlp.py` is mainly used to analyze the data obtained by `scraping_nlp.py`.

# How to install
Clone `scraping_nlp.py`, `analysis_nlp.py` and `hypothesis_test.py` from git hub

`Requisites`: Need Python 3.0 or later to run software

`Install Beautiful Soup 4`: `pip install beautifulsoup4` (Some `pip` may be named `pip3` respectively if you’re using Python 3)
recent version of Debian or Ubuntu Linux : `apt-get install python3-bs4`

`Install requests`: `pip install requests` (Some `pip` may be named `pip3` respectively if you’re using Python 3)

`Install pandas`: `sudo apt-get install python3-pandas` (pip might cause errors)


# License Information
Copyright (c) 2020 Wenbo Shi
