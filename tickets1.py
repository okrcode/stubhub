import requests
import cloudscraper
import logging
import random
import math
import csv
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("script.log"),
        logging.StreamHandler()
    ]
)




def make_csv(data, file_path):
    """Write data to a CSV file."""
    keys = data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def fetch_total_pages(url, headers):
    """Fetch total pages from the initial request."""
    try:
        response = requests.get(url, headers=headers,  timeout=120)
        response.raise_for_status()
        total_count = int(response.text.split('"totalCount"')[1].split(',')[0].replace(':', ''))
        total_pages = math.ceil(total_count / 20)
        logging.info(f"Total pages calculated: {total_pages}")
        return total_pages
    except Exception as e:
        logging.error(f"Error fetching total pages: {e}")
        return 13  # Default to 13 pages in case of failure

def fetch_data_from_pages(base_url, headers, total_pages):
    """Fetch data from all pages."""
    all_urls = []
    

    for page in range(total_pages):
        params = {
            'gridFilterType': '0',
            'sortBy': '0',
            'dates': '0,1970-01-01T00:00:00.000Z,9999-12-31T23:59:59.999Z',
            'location': '12.86,74.84',
            'nearbyGridRadius': '50',
            'eventViewType': '0',
            'eventBooleanFilters': '{"0":0,"1":0}',
            'pageIndex': str(page),  # Dynamically setting the pageIndex
            'method': 'GetFilteredEvents',
            'venueId': '3708',
            'searchGuid': 'null',
            'from': '1970-01-01T00:00:00.000Z',
            'to': '9999-12-31T23:59:59.999Z',
            'lat': '12.86',
            'lon': '74.84',
            'genreId': 'undefined',
            'radiusFrom': '80467',
            'radiusTo': 'null',
            'eventCountryType': '0',
        }
        try:
            response = requests.post(base_url, headers=headers, params=params, timeout=120)
            response.raise_for_status()
            data = response.json()
            urls = [item['url'] for item in data['items'] if 'url' in item]
            all_urls.extend(urls)
            logging.info(f"Fetched {len(urls)} URLs from page {page + 1}.")
        except Exception as e:
            logging.error(f"Error fetching data from page {page + 1}: {e}")

    return all_urls

def scrape_data(urls):
    headers = {
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7,ja;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.stubhub.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.stubhub.com/new-york-knicks-new-york-tickets-1-29-2025/event/154258373/?quantity=0',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
    """Scrape data from individual URLs."""
    final_data = []
    scraper = cloudscraper.create_scraper()
    for url in urls:
        json_data = {
            'ShowAllTickets': True,
            'HideDuplicateTicketsV2': False,
            'Quantity': 0,
            'IsInitialQuantityChange': False,
            'PageVisitId': '9BFF2752-4B8C-46C0-A5DF-8E075E8EB45B',
            'PageSize': 20,
            'CurrentPage': 0,
            'SortBy': 'NEWPRICE',
            'SortDirection': 0,
            'Sections': '',
            'Rows': '',
            'Seats': '',
            'SeatTypes': '',
            'TicketClasses': '',
            'ListingNotes': '',
            'InstantDelivery': False,
            'EstimatedFees': False,
            'BetterValueTickets': False,
            'PriceOption': '',
            'HasFlexiblePricing': False,
            'ExcludeSoldListings': False,
            'RemoveObstructedView': False,
            'NewListingsOnly': False,
            'PriceDropListingsOnly': False,
            'SelectBestListing': False,
            'ConciergeTickets': False,
            'Favorites': False,
            'Method': 'IndexSh',
        }
        try:
            response = scraper.post(url, headers=headers, json=json_data, timeout=120)
            print(url)
            if response.status_code == 200:
                j_data = response.json()
                total_pages = j_data['totalCount'] // 20
                if j_data['totalCount'] % 20 != 0:
                    total_pages += 1
                print(f"Total pages for category_id: {total_pages}")
                for page_num in range(0, total_pages + 1):
                    json_data['CurrentPage'] = str(page_num)
                    print(json_data['CurrentPage'])

                    response = scraper.post(url, headers=headers, json=json_data, timeout=120)
                    if response.status_code != 200:
                        break

                    print(f"Processing category page {page_num}")
                    data = response.json()

                    for item in data['items']:
                        record = {
                            "section_name": item.get('sectionMapName', ''),
                            "zone": item.get('ticketClassName', ''),
                            "price": item.get('price', ''),
                            "listingId": item.get('listingId', ''),
                            "ticketClass": item.get('ticketClass', ''),
                            "img": item.get('vfsUrl', '')
                        }
                        final_data.append(record)
                logging.info(f"Successfully scraped data from {url}.")
        except Exception as e:
            logging.error(f"Error scraping data from {url}: {e}")
    return final_data

def main():
    base_url = "https://www.stubhub.com/madison-square-garden-tickets/venue/1282/"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7,ja;q=0',
        'cache-control': 'no-cache',
        # 'content-length': '0',
        'content-type': 'application/json',
        'origin': 'https://www.stubhub.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.stubhub.com/madison-square-garden-tickets/venue/1282/?restPage=1',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'Connection': 'keep-alive',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-csrf-token': 'VppC330C-Gomrn1E8nXvjnykk9o8QCKdBJt7HaeW5YHb234LpvG13qBSO6QUlqvTVqypAolF0ilj4G4IcwBNO5YaU9kakv31OPPNUn3uy241',
    }

    logging.info("Starting data scraping script.")
    # Step 1: Fetch total pages
    total_pages = fetch_total_pages(base_url, headers)

    # Step 2: Fetch data URLs from all pages
    urls = fetch_data_from_pages(base_url, headers, total_pages)

    # Step 3: Scrape data from individual URLs
    scraped_data = scrape_data(urls)

    # Step 4: Save data to a CSV file
    output_file = "scraped_data.csv"
    if scraped_data:
        make_csv(scraped_data, output_file)
        logging.info(f"Data successfully saved to {output_file}.")
    else:
        logging.warning("No data scraped. CSV file not created.")

if __name__ == "__main__":
    main()