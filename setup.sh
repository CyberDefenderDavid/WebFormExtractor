#!/bin/bash

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y wget unzip python3 python3-venv python3-pip xvfb libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libnspr4 libxrandr2 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libgtk-3-0 libxshmfence1

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get -f install

# Create a virtual environment and install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete. Activate the virtual environment using 'source venv/bin/activate' and run the script using 'python scrape_live_page.py'."
