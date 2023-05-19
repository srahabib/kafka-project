# from pyspark.streaming.kafka import KafkaUtils
# from pyspark.streaming import StreamingContext
# from pyspark.sql import SparkSession
from confluent_kafka import Producer, Consumer
import praw
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


# Ignore all warnings
warnings.filterwarnings("ignore")


user_agent = "Scraper 1.0 by /u/Salt-Air7636"
reddit = praw.Reddit(
    client_id="RekRcuPSQYfexpm5Ww5ncg",
    client_secret="lsFUPApvy6XP5N_wNK724xRHK8fkNA",
    user_agent=user_agent
)

# hot new rising top
headlines = set()
for submission in reddit.subreddit('dogecoin').rising(limit=None):
    print(submission.title)
    print(submission.id)
    print(submission.author)
    print(submission.created_utc)
    print(submission.score)
    print(submission.upvote_ratio)
    print(submission.url)
    break
    headlines.add(submission.title)
print(len(headlines))

# hot new rising top
headlines = set()
for submission in reddit.subreddit('dogecoin').hot(limit=10):
    headlines.add(submission.title)

print(len(headlines))

df = pd.DataFrame(headlines)
# df.head(10)


producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'acks': 'all',
    'retries': 3
})

topic = 'topic_one'

for index, row in df.iterrows():
    # Serialize the data (e.g., convert to JSON or string)
    serialized_data = str(row.to_json())
    # print("I reached here")

    # Publish the data to the Kafka topic
    producer.produce(topic=topic, value=serialized_data)

# Flush and wait for the messages to be sent
producer.flush()

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumer_group_XX',
    'auto.offset.reset': 'earliest'
})

topic = 'topic_one'

# Subscribe to the Kafka topic
consumer.subscribe([topic])

while True:
    # Poll for new messages
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    # Process the received message
    data = msg.value()
    print(data)
    # Subscribe to 1 topic

consumer.close()
