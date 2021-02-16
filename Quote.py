class Quote:

  def __init__(self, tweet_id, text, author):
    self.id = f'{tweet_id}-{author}'
    self.tweet_id = tweet_id
    self.text = text
    self.author = author