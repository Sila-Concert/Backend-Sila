import pandas as pd
import snscrape.modules.twitter as sntwitter
import re
import string
scraper = sntwitter.TwitterSearchScraper("เดอะทอย")
tweets = []
for i,tweet in enumerate(scraper.get_items()):
  if tweet.lang == 'th':
    data = [
        tweet.date, 
        tweet.username,
        tweet.content,
        tweet.retweetCount,
        tweet.likeCount,
        tweet.viewCount,
        tweet.replyCount
        
        ]
    tweets.append(data)
  if i > 100:
    break  
tweet_df = pd.DataFrame(tweets, columns=['date','username','content','retweet','likecount','viewcount','reply'])
tweet_df['content']

type(tweet_df)


emoji = re.compile("["
                   u"\U0001F600-\U0001F64F"  
                   u"\U0001F300-\U0001F5FF"  
                   u"\U0001F680-\U0001F6FF" 
                   u"\U0001F1E0-\U0001F1FF"  
                   u"\U00002500-\U00002BEF"  
                   u"\U00002702-\U000027B0"
                   u"\U00002702-\U000027B0"
                   u"\U000024C2-\U0001F251"
                   u"\U0001f926-\U0001f937"
                   u"\U00010000-\U0010ffff"
                   u"\u2640-\u2642"
                   u"\u2600-\u2B55"
                   u"\u200d"
                   u"\u23cf"
                   u"\u23e9"
                   u"\u231a"
                   u"\ufe0f"  
                   u"\u3030"
                   "]+", flags = re.UNICODE) 

from pythainlp import word_tokenize
word = []
for i in range(len(tweet_df)):
  text = tweet_df['content'][i]
  newText = re.sub(r'(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', text)
  newText = re.sub(emoji, '', newText)
  newText = re.sub(r'@([a-zA-Z0-9_]+)', '', newText)
  newText = re.sub(r'#([a-zA-Z0-9ก-๙_]+)', '', newText)
  newText = newText.translate(str.maketrans('', '', string.punctuation))
  tweet_df['content'].replace({
        tweet_df['content'][i]:newText
    }, inplace=True)
  
print(tweet_df)