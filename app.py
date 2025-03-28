from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import random
import time
from requests.exceptions import RequestException
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Configure logging
logging.basicConfig(filename='product_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0",
]

def convert_to_rupees(price):
    try:
        price = float(price.replace(',', '')) * 83  # Assuming 1 USD = 83 INR
        return f"₹{price:,.2f}"
    except ValueError:
        return price

def get_amazon_product_details(product):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }
    search_url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.select("a.a-link-normal.s-no-outline")[:3]
        products = []
        for result in results:
            product_link = "https://www.amazon.com" + result["href"]
            time.sleep(2)
            response = requests.get(product_link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.select_one("#productTitle")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            price_tag = soup.select_one(".a-price-whole")
            price = price_tag.get_text(strip=True) if price_tag else "Not Available"
            if price != "Not Available":
                price = convert_to_rupees(price)

            image_tag = soup.select_one("#landingImage")
            image = image_tag["src"] if image_tag else "No Image"

            rating_tag = soup.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True) if rating_tag else "No Rating"

            products.append({"site": "Amazon", "title": title, "link": product_link, "price": price, "image": image, "rating": rating})
        
        return products
    except RequestException as e:
        logging.error(f"Amazon Error: {e}")
        return None

def get_flipkart_product_details(product):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    search_url = f"https://www.flipkart.com/search?q={product}"

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.select("a.CGtC98")[:3]
        products = []
        for result in results:
            product_link = "https://www.flipkart.com" + result["href"]
            response = requests.get(product_link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.select_one("span.VU-ZEz")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            price_tag = soup.select_one("div.Nx9bqj.CxhGGd")
            price = price_tag.get_text(strip=True) if price_tag else "Not Available"

            image_tag = soup.select_one("img.DByuf4.IZexXJ.jLEJ7H")
            image = image_tag["src"] if image_tag else "No Image"

            rating_tag = soup.select_one("div._3LWZlK")
            rating = rating_tag.get_text(strip=True) if rating_tag else "No Rating"

            details_tag = soup.select_one("div.XQDdHH")
            details = details_tag.get_text(strip=True) if details_tag else "No Details"

            products.append({"site": "Flipkart", "title": title, "link": product_link, "price": price, "image": image, "rating": rating, "details": details})
        
        return products
    except RequestException as e:
        logging.error(f"Flipkart Error: {e}")
        return None

@app.route('/search', methods=['GET'])
def search_product():
    product_name = request.args.get("product", "").replace(" ", "+")
    amazon_data = get_amazon_product_details(product_name)
    flipkart_data = get_flipkart_product_details(product_name)

    if not amazon_data and not flipkart_data:
        return jsonify({"message": "No product found"}), 404

    return jsonify(flipkart_data + amazon_data if amazon_data and flipkart_data else amazon_data or flipkart_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
