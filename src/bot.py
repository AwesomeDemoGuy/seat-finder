import requests

URL = "https://discord.com/api/webhooks/1309044790821785660/Nb_VWUae-weMRtGGk3Kc_YheYjQ4zpUrdlqkKlHPtdXaWNKlybQLUZgurNt1v9BnnscU"

def notify(class_name, current_value, url):
  requests.post(URL, json={ "content": f"<@180423023340290048> {class_name}: Seats open: {current_value}\n{url}"})

