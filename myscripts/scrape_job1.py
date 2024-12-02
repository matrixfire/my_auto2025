
"""
This script collects data from the LEGO Ideas website and saves it to an Excel file. 

1. **Initialize WebDriver**: Uses Selenium WebDriver to automate browser interactions (e.g., Firefox).
2. **Navigate and Scroll**: Visits the LEGO Ideas webpage and scrolls down to load more projects.
3. **Extract Data**: Scrapes project details including image URL, title, author, release date, number of supporters, and the detailed page URL.
4. **Avoid Duplicates**: Tracks URLs to avoid processing duplicates.
5. **Save to Excel**: Prompts the user for an Excel file name, creates a workbook, and writes the collected data into it.
6. **Close WebDriver**: Properly closes the WebDriver after completing the data collection.

Dependencies:
- Selenium for browser automation.
- OpenPyXL for handling Excel files.
- PyInputPlus for user input with default options.
"""
import time
import random
import pyinputplus as pyip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

def collect_lego_data():
    driver = None
    data = []

    try:
        # Initialize the WebDriver (e.g., for Firefox)
        driver = webdriver.Firefox()

        # Navigate to the desired webpage
        driver.get('https://ideas.lego.com/')  # Replace with the actual URL

        # Wait for the cards holder to be present
        wait = WebDriverWait(driver, 10)
        cards_holder = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="whats-up-app"]/div[2]/div[1]/div/div[2]')))

        # Initialize a set to keep track of seen project URLs
        seen_urls = set()

        # Scroll down to load more images
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2 * random.random())
        time.sleep(2 + random.randint(3, 10))

        # Locate all card elements within the cards holder
        cards = cards_holder.find_elements(By.XPATH, './/div[@data-test="project-tile"]')

        for card in cards:
            try:
                # 1. Get the image URL
                img_element = card.find_element(By.XPATH, './/img[@data-test="card-image"]')
                img_url = img_element.get_attribute('src')

                # 2. Get the title
                title_element = card.find_element(By.XPATH, './/h3[@data-test="card-title"]/a')
                title = title_element.text

                # 3. Get the author's name
                author_element = card.find_element(By.XPATH, './/div[@class="user-alias text-truncate"]/a')
                author = author_element.text

                # 4. Get the release date
                date_element = card.find_element(By.XPATH, './/div[@class="card-published"]/time')
                release_date = date_element.get_attribute('title')

                # 5. Get the number of supporters
                supporters_element = card.find_element(By.XPATH, './/a[@data-test="project-support-value"]')
                supporters = supporters_element.text

                # 6. Construct the detailed page URL
                detailed_page_url = title_element.get_attribute('href')

                # Check if this URL has already been processed
                if detailed_page_url in seen_urls:
                    print("Found duplicate.")
                    continue

                # Add the URL to the seen set
                seen_urls.add(detailed_page_url)

                # Append the extracted information to the data list
                data.append([img_url, title, author, release_date, supporters, detailed_page_url])

                # Optionally print the extracted information
                print(f"Image URL: {img_url}")
                print(f"Title: {title}")
                print(f"Author: {author}")
                print(f"Release Date: {release_date}")
                print(f"Supporters: {supporters}")
                print(f"Detailed Page URL: {detailed_page_url}")
                print("="*50)
            
            except Exception as e:
                print(f"Error extracting data from card: {e}")

    except Exception as e:
        print(f"Error in main data collection: {e}")

    finally:
        # Prompt to close the WebDriver
        if driver:
            close_driver = pyip.inputChoice(prompt="Do you want to close the WebDriver? (yes/no): ", choices=['yes', 'no'], default='yes')
            if close_driver.lower() == 'yes':
                driver.quit()

        # Prompt for the Excel file name with a default option
        excel_filename = pyip.inputStr(prompt="Enter the Excel file name (default is 'lego_imgs.xlsx'): ", default='lego_imgs.xlsx')
        
        # Use default if the input is empty or whitespace
        if not excel_filename.strip():
            excel_filename = 'lego_imgs.xlsx'

        # Create an Excel workbook and worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Lego Ideas Data'

        # Write the header
        headers = ['Image URL', 'Title', 'Author', 'Release Date', 'Supporters', 'Detailed Page URL']
        sheet.append(headers)

        # Write the data
        for row in data:
            sheet.append(row)

        # Save the workbook
        workbook.save(excel_filename)
        print(f"Data successfully written to {excel_filename}")

if __name__ == "__main__":
    collect_lego_data()



