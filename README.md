# Stubhub.com Scraper

This Python script scrapes ticket details data from stubhub.com, specifically focusing on details such as zone, section,price and images. The data is saved in a csv format.

## Features

- Scrapes ticket information from stubhub.com for a specific date range.
- Extracts details like zone, section,price and images.
- Logs the scraping process and errors.
- Saves the scraped data to a CSV file.

## Requirements

- Python 3.x
- `requests` - To send HTTP requests and retrieve HTML content.
- `lxml` - For parsing HTML and XML documents.
- `json` - For handling JSON data.
- `logging` - To log the scraping process.
- `urllib3` - For HTTP requests with suppressed SSL warnings.
- `cloudscraper'` - To bypass anti-bot mechanisms like Cloudflare.
- `random` - To add randomized behavior to requests and delays.

You can install the required libraries using:

```bash
pip install requests lxml
```


## Usage

- Clone or download the repository containing the script.

- Install the required dependencies:

```bash
pip install requests lxml
```

- Run the script by executing it in the command line:
```bash
python tickets1.py
```


- After execution, the data will be saved in a csv file called scraped_data.csv in the same directory as the script.



