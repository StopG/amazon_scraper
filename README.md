# Amazon Product Scraper 🛒

A Python-based Amazon product scraper built using **Playwright**.

This project uses Playwright's asynchronous API to automate a Chrome browser, scrape product information from Amazon, and export the collected data into an Excel file.

## 🚀 Features

- Scrapes Amazon product information
- Uses Playwright for browser automation
- Uses asynchronous Playwright (`async_playwright`)
- Handles dynamically loaded web content
- Extracts product details
- Stores scraped data in a structured format
- Exports the results to an Excel file

## 🛠️ Tech Stack

- Python
- Playwright
- Pandas
- Asyncio
- OpenPyXL
- Google Chrome
- Microsoft Excel

⚙️ Installation
1. Clone the repository
git clone https://github.com/StopG/amazon_scraper.git
2. Navigate to the project directory
cd amazon_scraper
3. Install the required Python packages
pip install playwright pandas openpyxl
4. Install Playwright
playwright install
▶️ How to Run

This scraper connects to Chrome using Chrome Remote Debugging.

1. Start Chrome with remote debugging

Open PowerShell and run:

& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-cdp-profile"

This starts Chrome with remote debugging enabled on port 9222.

2. Run the scraper

Open another terminal in the project directory and run:

python amazon_async_scraper.py

The scraper will connect to the Chrome instance running on port 9222, navigate through Amazon, collect the required product information, and export the scraped data to an Excel file.

🔄 Async Playwright

This project uses Playwright's asynchronous API.

The Playwright async API is imported using:

from playwright.async_api import async_playwright

The project also uses Pandas for handling and exporting the scraped data:

import pandas as pd
📊 Output

The scraped product data is exported to an Excel (.xlsx) file.

The collected information can include:

Product name
Product price
Product rating
Number of reviews
Product URL
Other available product information
📁 Project Structure
amazon_scraper/
│
├── amazon_async_scraper.py
├── .gitignore
└── README.md
⚠️ Disclaimer

This project was created for educational purposes to practice Python, Playwright, browser automation, and web data extraction.

Please make sure your use of the scraper complies with Amazon's terms of service and applicable laws.

🔮 Future Improvements
Improve error handling
Add configurable search queries
Improve scraping reliability
Add support for multiple Amazon pages
Add logging
Improve data validation
Add a command-line interface


## 📋 Requirements

Make sure you have **Python 3.9 or higher** installed.

You also need **Google Chrome** installed on your system.

Check your Python version:

```bash
python --version
