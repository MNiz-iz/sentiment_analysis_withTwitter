import tweepy # api twitter
import config
import re
import emoji # remove emoji
from pullDataFromMongoDB import tb

# keyword you want to collect data and categories data you need
def inp(keyword):
    # เชื่อมต่อกับtwitter
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)    
    
    kw = str(keyword)
    query = kw + ' -is:retweet -is:reply lang:en'

    count = 0 # เอาไว้นับจำนวนทวิต 
    thisdict = {} # เตรียมเก็บข้อมูลในรูป json เพื่อเอาลง mongo

    # for loop to pull data from twitter and clean string format client.search_recent_tweets:pull last content 7 days from twitter
    # query pull data by keyword,Don't focus max_result the real num result is limit
    for tweet in tweepy.Paginator(client.search_recent_tweets,query=query,max_results=100).flatten(limit=1000):
        item = tweet.text # ใส่ข้อมูลที่ดึงมาจากทวิต

        # clean data
        item = re.sub(r'@[A-Za-z0-9]+', '', item) # ตัดเมนชั่น
        item = re.sub(r'https?:\/\/\S+', '', item) # ตัดลิ้งต่างๆ
        item = item.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) #ตัดอักขระ
        item = item.replace("\n", "")
        # ตัดคำที่ไม่สื่อความหมาย
        item = re.sub("&amp;", "", item) 
        item = re.sub("&gt;", "", item) 
        item = re.sub("&lt;", "", item)
        item = ''.join([c for c in item if c not in emoji.EMOJI_DATA]) # ตัดอีโมจิ

        thisdict[item] = count # เก็บข้อมูลที่คลีนแล้วไว้ใน thisdict รูปแบบของ json แล้วให้ค่าของทวิตนั้นๆ เป็นลำดับทวิต
        count += 1 # เพิ่มลำดับทวิตเพื่อเอาไปใช้ต่อ

    # insert data to mongoDB
    tb.insert_one(thisdict)
    print('insert to mongoDB OK') # check