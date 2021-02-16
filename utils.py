import requests
from config import DISCORD_WEBHOOK_URL

def save_to_file(text, filename):
  with open(filename, 'w') as file:
    file.write(text)

def read_from_file(filename):
  with open(filename, 'r') as file:
    return file.read()

def send_to_discord(msg):
  data = {
    'content': msg,
    'username': 'python'
  }

  requests.post(DISCORD_WEBHOOK_URL, json = data)