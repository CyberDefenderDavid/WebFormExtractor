import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def sanitize_filename(filename):
    # Allow alphanumeric characters, spaces, underscores, dashes, and periods
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-', '.')).rstrip()

def extract_form_from_url(url, action):
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # Parse the URL to get the site name
    parsed_url = urlparse(url)
    site_name = sanitize_filename(parsed_url.netloc)
    
    # Set up Selenium WebDriver with additional options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # Open the web page
        driver.get(url)

        # Wait for the page to load completely
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Get the page source
        page_source = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        if action == '2':
            # Extract all form elements
            forms = soup.find_all('form')
            if forms:
                form_count = 1
                for form in forms:
                    form_fields = []
                    for input_tag in form.find_all(['input', 'select', 'textarea']):
                        field = {}
                        if input_tag.name == 'select':
                            field['type'] = 'select'
                            field['name'] = input_tag.get('name')
                            field['options'] = [option.get_text() for option in input_tag.find_all('option')]
                        else:
                            field['type'] = input_tag.get('type') or input_tag.name
                            field['name'] = input_tag.get('name')
                            field['value'] = input_tag.get('value')
                            field['placeholder'] = input_tag.get('placeholder')
                        
                        form_fields.append(field)

                    form_action = form.get('action', '#')
                    form_method = form.get('method', 'post')

                    # Create a new HTML document with the extracted form fields
                    new_html = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Extracted Form</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                margin: 20px;
                            }}
                            .form-group {{
                                margin-bottom: 15px;
                            }}
                            label {{
                                display: block;
                                margin-bottom: 5px;
                            }}
                            input, select, textarea {{
                                width: 100%;
                                padding: 8px;
                                box-sizing: border-box;
                            }}
                            .annotation {{
                                font-size: 0.9em;
                                color: #555;
                                margin-top: 5px;
                            }}
                        </style>
                    </head>
                    <body>
                        <form method="{form_method}" action="{form_action}">
                    """

                    for field in form_fields:
                        new_html += f'<div class="form-group">'
                        if field['type'] == 'select':
                            new_html += f'<label for="{field["name"]}">{field["name"]}:</label>'
                            new_html += f'<select name="{field["name"]}">'
                            for option in field['options']:
                                new_html += f'<option value="{option}">{option}</option>'
                            new_html += '</select>'
                        else:
                            new_html += f'<label for="{field["name"]}">{field["name"]}:</label>'
                            new_html += f'<input type="{field["type"]}" name="{field["name"]}"'
                            if field['value']:
                                new_html += f' value="{field["value"]}"'
                            if field['placeholder']:
                                new_html += f' placeholder="{field["placeholder"]}"'
                            new_html += '>'
                        new_html += f'<div class="annotation">This field will be sent to: {form_action}</div>'
                        new_html += '</div>'

                    new_html += f"""
                        <button type="submit">Submit</button>
                        <div class="annotation">The form will be submitted to: {form_action}</div>
                        </form>
                    </body>
                    </html>
                    """

                    # Create a folder for the site
                    folder_path = f'./{site_name}'
                    os.makedirs(folder_path, exist_ok=True)

                    # Write the new HTML to a file
                    with open(f'{folder_path}/{site_name}-form-{form_count}.html', 'w', encoding='utf-8') as file:
                        file.write(new_html)

                    print(f"Form {form_count} fields extracted and saved to {site_name}-form-{form_count}.html")
                    form_count += 1
            else:
                print("No form found in the web page")
        elif action == '1':
            # Create a folder for the site
            folder_path = f'./{site_name}'
            os.makedirs(folder_path, exist_ok=True)

            # Save the full page source
            with open(f'{folder_path}/{site_name}-full.html', 'w', encoding='utf-8') as file:
                file.write(page_source)
                
            print(f"Full page source saved to {site_name}-full.html")

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    # Prompt the user for the URL
    url = input("Enter the URL of the web page to scrape: ")
    action = input("Choose an action:\n1) Full scrape\n2) Extract form\nEnter 1 or 2: ")
    extract_form_from_url(url, action)
