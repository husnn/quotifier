from config import *
from utils import read_from_file, save_to_file

class Watcher:

  @staticmethod
  def set_last_mention(mention):
    save_to_file(mention.id_str, LAST_MENTION_FILE)

  @staticmethod
  def get_last_mention_id():
    id = read_from_file(LAST_MENTION_FILE)
    return id if id else None

  def get_new_mentions(self):
    print('\nRetrieving new mentions...')

    mentions = []

    try:
      mentions = self.api.mentions_timeline(since_id=Watcher.get_last_mention_id(), count=10)
    except Exception as e:
      print(f'Could not retrieve mentions. {e}')

    return mentions

  def __init__(self, api):
    self.api = api