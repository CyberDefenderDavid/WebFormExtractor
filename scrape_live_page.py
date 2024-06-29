import os
import html
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-', '.'))

def extract_form_from_url(url, action):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed_url = urlparse(url)
    site_name = sanitize_filename(parsed_url.netloc)

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
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        if action == '2':
            forms = soup.find_all('form')
            if forms:
                form_count = 1
                for form in forms:
                    form_fields = []
                    element_counts = {
                        'inputs': len(form.find_all('input')),
                        'textareas': len(form.find_all('textarea')),
                        'selects': len(form.find_all('select')),
                        'buttons': len(form.find_all('button'))
                    }

                    for idx, input_tag in enumerate(form.find_all(['input', 'select', 'textarea', 'button']), start=1):
                        print(f"Processing element {idx}")
                        field = {
                            'type': input_tag.get('type') or input_tag.name,
                            'name': input_tag.get('name'),
                            'value': input_tag.get('value', ''),
                            'placeholder': input_tag.get('placeholder', ''),
                            'element': str(input_tag)
                        }

                        if input_tag.name == 'select':
                            select_element = driver.find_element(By.NAME, input_tag.get('name'))
                            field['options'] = [option.text for option in Select(select_element).options]
                        form_fields.append(field)

                    folder_path = f'./{site_name}'
                    os.makedirs(folder_path, exist_ok=True)
                    form_filename = f'{site_name}-form-{form_count}.html'
                    with open(f'{folder_path}/{form_filename}', 'w', encoding='utf-8') as file:
                        file.write(create_html_document(form_fields, element_counts))
                    print(f"Form {form_count} fields extracted and saved to {form_filename}.")
                    form_count += 1
            else:
                print("No form found in the web page")
        elif action == '1':
            folder_path = f'./{site_name}'
            os.makedirs(folder_path, exist_ok=True)
            full_filename = f'{folder_path}/{site_name}-full.html'
            with open(full_filename, 'w', encoding='utf-8') as file:
                file.write(page_source)
            print(f"Full page source saved to {full_filename}")

    finally:
        driver.quit()

def create_html_document(form_fields, element_counts):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Extracted Form</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; }}
            input, select, textarea, button {{ width: 100%; padding: 8px; box-sizing: border-box; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-left: 3px solid #ccc; margin-top: 5px; white-space: pre-wrap; }}
            section {{ margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Form Analysis</h1>
    """

    for idx, field in enumerate(form_fields, start=1):
        html_content += f"""
        <section id="element-{idx}">
            <h2>Element {idx}</h2>
            <div class="form-group">
                <label>Type: {field["type"]}</label>
                <label>Name: {field["name"]}</label>
                <label>Value: {field["value"]}</label>
                <label>Placeholder: {field["placeholder"]}</label>
                <pre>{html.escape(field["element"])}</pre>
        """
        if field['type'] == 'select':
            html_content += f'<select name="{field["name"]}">'
            for option in field['options']:
                html_content += f'<option>{option}</option>'
            html_content += '</select>'
        elif field['type'] == 'button' or field['type'] == 'submit':
            html_content += f'<button name="{field["name"]}" value="{field["value"]}">{field["value"]}</button>'
        else:
            html_content += f'<input type="{field["type"]}" name="{field["name"]}" value="{field["value"]}" placeholder="{field["placeholder"]}">'
        html_content += '</div></section>'

    html_content += "</body></html>"
    return html_content

if __name__ == "__main__":
    url = input("Enter the URL of the web page to scrape: ")
    action = input("Choose an action:\n1) Full scrape\n2) Extract form\nEnter 1 or 2: ")
    extract_form_from_url(url, action)
