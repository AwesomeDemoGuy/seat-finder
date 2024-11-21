import os
import time
from datetime import datetime, timezone, timedelta
import geckodriver_autoinstaller
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import re
import bot


# Set up Selenium WebDriver
def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Optional: run in headless mode
    service = Service(geckodriver_autoinstaller.install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver
# Extract the specific value from the page
def get_specific_value(driver, url, css_identifier):
    driver.get(url)
    try:
        # Locate the specific element
        instructor_element = driver.find_element(By.CSS_SELECTOR, css_identifier)
        #seats_element = instructor_element.find_element(By.XPATH, '../../following-sibling::div[@class="class-results-cell seats"]/div[@class="text-nowrap"]')
        return instructor_element.text.strip()
    except Exception as e:
        print(f"Error locating element: {e}")
        return None

# Compare current value with the stored value
def check_for_seats(current_value):
    match = re.match(r"(\d+) of (\d+)", current_value)
    if match:
        available_seats, total_seats = match.groups()
        if available_seats != "0":
            return True
    return False

# Store the current value for future comparisons
def store_current_value(current_value, name, file):
        string = f"{name}: {current_value}"
        file.write(string)

# Main function
def print_result(current_value, url, class_name, timezone = timezone(timedelta(hours=-7))):
    current_time_mst = datetime.now(timezone.utc).astimezone(timezone)
    formatted_time_mst = current_time_mst.strftime('%Y-%m-%d %H:%M:%S %Z%z')

    print(f"{formatted_time_mst}:Current value: {current_value}")
    if current_value is None:
        print("Unable to retrieve the specific value. Retrying...")
    elif check_for_seats(current_value):
        print(f"{class_name}: Seats open: {current_value}\n{url}")
        bot.notify(class_name, current_value, url)
    else:
        print(f"{class_name}: No changes detected.")
        

def main():
    CSE355_url = "https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&catalogNbr=355&honors=F&promod=F&searchType=all&subject=CSE&term=2251"
    CSE355_css_identifier = '.focus:nth-child(2) > .seats > .text-nowrap'
    CSE340_url = "https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&catalogNbr=340&honors=F&promod=F&searchType=all&subject=CSE&term=2251"
    CSE340_css_identifier1 = '.focus:nth-child(2) > .seats > .text-nowrap'
    CSE340_css_identifier2 = '.focus:nth-child(5) > .seats > .text-nowrap'
    CSE340_css_identifier3 = '.focus:nth-child(11) > .seats > .text-nowrap'
    value_file = 'specific_value.txt'
    check_interval = 75  #in seconds
    driver = setup_driver()
    print("Driver initialized.")

    file = open(value_file, 'w')

    try:
        while True:
            current_value = str(get_specific_value(driver, CSE355_url, CSE355_css_identifier))
            print_result(current_value, CSE355_url, "CSE 355")
            store_current_value(current_value, "CSE 355", file)
            time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again
            current_value = str(get_specific_value(driver, CSE340_url, CSE340_css_identifier1))
            print_result(current_value, CSE340_url, "CSE340")
            store_current_value(current_value, "CSE 340", file)
            time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again
            current_value = str(get_specific_value(driver, CSE340_url, CSE340_css_identifier2))
            print_result(current_value, CSE340_url, "CSE340")
            store_current_value(current_value, "CSE 340", file)
            time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again
            current_value = str(get_specific_value(driver, CSE340_url, CSE340_css_identifier3))
            print_result(current_value, CSE340_url, "CSE340")
            store_current_value(current_value, "CSE 340", file)
            time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again
            
            #time.sleep(check_interval + random.randint(0, 20) - 10)  # Wait before checking again

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
