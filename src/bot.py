import requests
import os
from dotenv import load_dotenv
load_dotenv()
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
#USER = os.getenv('USER')
USER = "<@180423023340290048>"

def notify(class_name, current_value, url):
  print(WEBHOOK_URL)
  requests.post(WEBHOOK_URL, json={ "content": f"{USER} {class_name}: Seats open: {current_value}\n{url}"})

