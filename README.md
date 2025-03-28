# 🚀 Flipkart Product Scraper - Backend

## 📌 Overview
This backend service scrapes product details from Flipkart, including title, price, rating, and images, using web scraping techniques.

## 🛠️ Tech Stack
- Python 🐍
- Flask 🌐
- BeautifulSoup 🍜
- Requests 📡

## 🔧 Installation & Setup
```bash
# Clone the repository
git clone https://github.com/your-repo.git
cd your-repo

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\\Scripts\\activate'

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

## 🚀 API Endpoints
### 🔍 Fetch Product Details
```http
GET /api/products?query=mobile
```
#### Response:
```json
{
  "site": "Flipkart",
  "title": "Product Name",
  "link": "https://flipkart.com/product-link",
  "price": "₹9,999",
  "image": "https://image-link.jpg",
  "rating": "4.3",
  "details": "Product description here"
}
```

## 📜 Features
✅ Scrapes Flipkart product details dynamically  
✅ Handles request exceptions & errors gracefully  
✅ Lightweight & fast response time ⚡  
 
