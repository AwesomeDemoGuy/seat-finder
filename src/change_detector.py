import os
import time
from datetime import datetime, timezone, timedelta
import geckodriver_autoinstaller
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

# Set up Selenium WebDriver
def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Optional: run in headless mode
    service = Service(geckodriver_autoinstaller.install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver
# Extract the specific value from the page
def get_specific_value(driver, url):
    driver.get(url)
    try:
        # Locate the specific element
        instructor_element = driver.find_element(By.CSS_SELECTOR, '.focus:nth-child(2) > .seats > .text-nowrap')
        #seats_element = instructor_element.find_element(By.XPATH, '../../following-sibling::div[@class="class-results-cell seats"]/div[@class="text-nowrap"]')
        return instructor_element.text.strip()
    except Exception as e:
        print(f"Error locating element: {e}")
        return None

# Compare current value with the stored value
def check_for_seats(current_value):
    if (current_value != "0 of 150" and current_value != "None"):
        return True

# Store the current value for future comparisons
def store_current_value(current_value, value_file):
    with open(value_file, 'w') as file:
        file.write(current_value)

# Main function
def main():
    MST = timezone(timedelta(hours=-7))
    url = "https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&catalogNbr=355&honors=F&promod=F&searchType=all&subject=CSE&term=2251"
    value_file = 'specific_value.txt'
    check_interval = 120  #in seconds
    driver = setup_driver()
    print("Driver initialized.")

    try:
        while True:
            current_value = str(get_specific_value(driver, url))
            current_time_mst = datetime.now(timezone.utc).astimezone(MST)
            formatted_time_mst = current_time_mst.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            print(f"{formatted_time_mst}:Current value: {current_value}")
            if current_value is None:
                print("Unable to retrieve the specific value. Retrying...")
            elif check_for_seats(current_value):
                print(f"Seats open: {current_value}\n{url}")
            else:
                print("No changes detected.")

            store_current_value(current_value, value_file)
            time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
