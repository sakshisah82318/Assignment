import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def scrape_product_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_data = []

    # Find all the product listings on the page
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        # Extract the required data for each product
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

        # Append the product data to the list
        product_data.append([product_url, product_name, product_price, rating, num_reviews])

    return product_data
def scrape_product_details(url):
    # Send a GET request to the product URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_details = []

    try:
        # Extract the required details from the product page
        description_element = soup.find('div', {'id': 'productDescription'})
        description = description_element.text.strip() if description_element else ''

        asin_element = soup.find('th', text='ASIN')
        asin = asin_element.find_next_sibling('td').text.strip() if asin_element else ''

        product_description_element = soup.find('h1', {'id': 'title'})
        product_description = product_description_element.text.strip() if product_description_element else ''

        manufacturer_element = soup.find('th', text='Manufacturer')
        manufacturer = manufacturer_element.find_next_sibling('td').text.strip() if manufacturer_element else ''

        # Append the product details to the list
        product_details.append([url, description, asin, product_description, manufacturer])

    except AttributeError:
        pass

    return product_details



# Scrape product listing pages
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
pages_to_scrape = 20  # Number of pages to scrape
product_list = []

for page in range(1, pages_to_scrape + 1):
    url = base_url + str(page)
    product_list.extend(scrape_product_data(url))

# Scrape product details
product_details_list = []

# Scrape a maximum of 200 product URLs
max_urls_to_scrape = 200
urls_scraped = 0

for product in product_list[:max_urls_to_scrape]:
    product_url = product[0]
    product_details_list.extend(scrape_product_details(product_url))
    urls_scraped += 1

    if urls_scraped >= max_urls_to_scrape:
        break

# Save the data to a CSV file
csv_filename = 'amazon_product_data.csv'

with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])

    for product in product_list:
        writer.writerow(product)

    writer.writerow([])  # Empty row for separation between sections

    writer.writerow(['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])

    for product_details in product_details_list:
        writer.writerow(product_details)

print('Scraping complete. Data saved to', csv_filename)
