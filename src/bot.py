import requests
import os
# Grab the url from the .env file
URL = os.getenv("URL")

def notify(class_name, current_value, url):
  requests.post(URL, json={ "content": f"<@180423023340290048> {class_name}: Seats open: {current_value}\n{url}"})

