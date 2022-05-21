# LinkedIn Scraper

A scraper which doesn't depend upon XML structure and uses text based extraction for identifying the data and extracts it from public linkedin pages.

It is 100% written in Python3. The libraries used are:
- Selenium
- BeautifulSoup
- PyMongo

[Connection to DB](https://github.com/Heave6899/linkedin-scraper/blob/2a8f1fae6dae1bb16eace69b41401ed54b1f2064/test.py#L18): It connects to the DB of choice, replace the function to connect to a preferred database

## Features
- Authentication Wall Detection
- Error Handling for pages
- Free Proxy IP generator
- Automated scraping
- Save to CSV
- Cookie logic for bot detect prevention

## Roadmap
- [ ] Paid proxy support
- [ ] Incognito crawling with Authentication Wall prevention
- [ ] AWS deploy and docker image support
