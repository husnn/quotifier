from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tweepy

from Quotifier import Quotifier
import images.rebuild_store
from config import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

quotifier = Quotifier(api)
quotifier.start()