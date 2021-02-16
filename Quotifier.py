import os
import re
import sys
import time
import json
import random
import shutil
import difflib
import textwrap
import datetime
from PIL import Image, ImageFont, ImageDraw

from Watcher import Watcher
from Quote import Quote
from config import *
from utils import send_to_discord

class Quotifier:

  def clean_text(self, text):
    return re.sub('@\w+|http\S+', '', text, flags=re.IGNORECASE).strip()

  def reply_with_image(self, filename, tweet):
    print('\nResponding with image...')
    
    self.api.update_with_media(
      filename,
      f'@{tweet.user.screen_name}',
      in_reply_to_status_id = tweet.id
    )
    
    if (DISCORD_WEBHOOK_URL): send_to_discord('New tweet posted.')

    print('Posted')
    

  def get_similar_key(self, matchable, collection):
    highest_similarity = 0
    match = None

    for key in collection:
      similarity = difflib.SequenceMatcher(None, matchable.lower(), key.lower()).ratio()

      if (similarity >= MIN_MATCH_SIMILARITY) and (similarity > highest_similarity):
        highest_similarity = similarity
        match = key
        
        print(f'Key similarity ({key}): {similarity}')

    return match

  def get_image_by_id(self, id):
    image = None
    for key in self.images:
      for file in self.images.get(key).get('files'):
        if file['id'] == id:
          image = file['path']
    return IMAGES_DIR + image

  def get_background_image(self, key=DEFAULT_IMAGE_KIND):
    file = random.choice(self.images.get(key).get('files'))
    return IMAGES_DIR + file['path']

  def get_background_image_for_author(self, author):
    key = self.get_similar_key(author, self.images)
    return self.get_background_image(key) if key else self.get_background_image()

  def does_quote_exist(self, quote):
    return quote.id in self.quotes

  def generate_quote_image(self, quote, background_image):
    print('\nGenerating new quote...')

    font = ImageFont.truetype(f'{FONTS_DIR}Raleway-Black.ttf', QUOTE_FONT_SIZE)
    author_font = ImageFont.truetype(f'{FONTS_DIR}Raleway-Bold.ttf', AUTHOR_FONT_SIZE)
    watermark_font = ImageFont.truetype(f'{FONTS_DIR}Raleway-Medium.ttf', WATERMARK_FONT_SIZE)

    image = Image.open(background_image).convert('RGB')

    draw = ImageDraw.Draw(image)

    max_w, max_h = image.size

    max_chars_per_line = int(max_w / (font.getsize(quote.text)[0] / len(quote.text)))
    if max_chars_per_line >= MAX_CHARS_PER_LINE: max_chars_per_line = MAX_CHARS_PER_LINE

    paragraph = textwrap.wrap(quote.text, width = max_chars_per_line)

    y_offset = 0

    for line in paragraph:
      line_w, line_h = font.getsize(line)

      x = (max_w - line_w) / 2
      y = (max_h - line_h) / 2

      draw.text((x, y + y_offset), line, font = font, fill=TEXT_COLOR)

      y_offset += QUOTE_FONT_SIZE

    draw.text(
      (
        (max_w - author_font.getsize(quote.author)[0]) / 2,
        (max_h / 2) + GAP_SIZE + y_offset
      ),
      f' - {quote.author}',
      font=author_font,
      fill=TEXT_COLOR
    )

    # Watermark
    watermark_w, watermark_h = watermark_font.getsize(WATERMARK_TEXT)
    draw.text(
      (
        (max_w - (watermark_w * 1.25)),
        (max_h - (watermark_h * 2))
      ),
      WATERMARK_TEXT,
      font=watermark_font,
      fill=TEXT_COLOR
    )

    image.save(f'{QUOTES_DIR}{quote.id}.{IMAGE_EXT}')

  def get_quote_image(self, quote, background_image):
    if not self.does_quote_exist(quote):
      self.generate_quote_image(quote, background_image)

    return f'{QUOTES_DIR}{quote.id}.{IMAGE_EXT}'

  def quotify(self, original_tweet, mention):
    author = f'@{original_tweet.user.screen_name}'
    is_author_named = False

    if 'by' in mention.text.lower():

      quoted = re.search('(?<= by )["\'”](.*?)["\'”]', mention.text, re.IGNORECASE)

      if quoted:
        author = quoted.group(1)
        is_author_named = True

      value = re.search('(?<= by )(\w+)', mention.text, re.IGNORECASE)

      if value:
        author = value.group(1)
        is_author_named = True

    quote = Quote(
      original_tweet.id_str,
      self.clean_text(original_tweet.text),
      author.strip()
    )

    bg = None

    if '--bg' in mention.text.lower():
      id = re.search('(?<=--bg )(\w+)', mention.text, re.IGNORECASE)
      if id: bg = self.get_image_by_id(id.group(1))

    if not bg and is_author_named:
      bg = self.get_background_image_for_author(author)

    if not bg:
      bg = self.get_background_image()

    DETACHED_FLAGS = ['--detached', '-D']

    if any(flag in mention.text for flag in DETACHED_FLAGS):
      if mention.user.screen_name.lower() == USERNAME:
       self.api.destroy_status(mention.id)

      mention = original_tweet

    image_file = self.get_quote_image(quote, bg)
    self.reply_with_image(image_file, mention)

    self.quotes.append(quote.id)

  def is_mention_expired(self, mention):
    return (datetime.datetime.now() - mention.created_at).seconds >= MENTION_EXPIRY_TIME_IN_SECONDS

  def start(self):
    print('Started')
    
    while (True):
      new_mentions = self.watcher.get_new_mentions()

      for mention in reversed(new_mentions):
        self.watcher.set_last_mention(mention)

        if self.is_mention_expired(mention):
          print(f'Mention by @{mention.user.screen_name} has expired.')
          continue

        try:
          print(f'\nNew mention by @{mention.user.screen_name}')

          if f'@{USERNAME} this' in mention.text.lower():
            original_tweet = self.api.get_status(mention.in_reply_to_status_id)
            print(f'Tweet: {original_tweet.text}')
            self.quotify(original_tweet, mention)
        except Exception as e:
          print(e)

      time.sleep(MENTION_CHECK_INTERVAL_IN_SECONDS)

  def init_paths(self):
    # quotes/
    if os.path.exists(QUOTES_DIR):
      shutil.rmtree(QUOTES_DIR)
    os.makedirs(QUOTES_DIR)

    # last_mention
    if not os.path.isfile(LAST_MENTION_FILE):
      open(LAST_MENTION_FILE, 'w').close()

  def load_quotes(self):
    if not os.path.exists(QUOTES_DIR): return
    self.quotes = [os.path.splitext(x)[0] for x in os.listdir(QUOTES_DIR)]

  def load_image_store(self):
    try:
      with open(IMAGE_STORE_FILE) as store_file:
        self.images = json.load(store_file)
    except ValueError as e:
      print(f'Could not read JSON file. {e}')
      sys.exit(0)

  def __init__(self, api):
    self.quotes = []
    
    self.api = api
    self.watcher = Watcher(api)
    self.images = None
    
    self.init_paths()
    self.load_quotes()
    self.load_image_store()
