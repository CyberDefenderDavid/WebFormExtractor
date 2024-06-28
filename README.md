Scrape Live Page
This project is a Python script for scraping web pages using Selenium and BeautifulSoup. The script allows you to either save the full HTML source of a page or extract and save the forms present on a page.

Requirements
Python 3.7 or higher
Google Chrome browser
ChromeDriver
The following Python packages:
selenium
webdriver-manager
beautifulsoup4
Installation
Clone the repository:
sh
Copy code
git clone https://github.com/your-username/scrape-live-page.git
cd scrape-live-page
Install the required packages:
sh
Copy code
pip install selenium webdriver-manager beautifulsoup4
Usage
Run the script:
sh
Copy code
python scrape_live_page.py
Enter the URL of the web page to scrape when prompted.

Choose the action:

1: Save the full HTML source of the page.
2: Extract and save the forms present on the page.
Script Details
The script performs the following tasks:

Ensures the provided URL starts with http:// or https://.
Uses Selenium WebDriver with ChromeDriver to open the web page.
Waits for the page to load completely.
Parses the HTML content using BeautifulSoup.
Depending on the selected action:
Saves the full HTML source of the page.
Extracts form elements, including input fields, selects, and textareas, and saves them in a new HTML file with annotations.
Creates a folder named after the site to store the extracted files.
Example
After running the script and providing the necessary inputs, the script will save the extracted content in a folder named after the website (e.g., example.com).

Notes
Make sure you have Google Chrome installed on your machine.
The script runs the browser in headless mode, meaning it will not display the browser window during execution.
