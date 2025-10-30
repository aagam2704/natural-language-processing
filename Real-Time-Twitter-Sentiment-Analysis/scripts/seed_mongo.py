import csv
from pymongo import MongoClient
import re

POS_WORDS = set(["good", "great", "happy", "love", "excellent", "best", "awesome", "nice", "win"])
NEG_WORDS = set(["bad", "sad", "hate", "terrible", "worst", "angry", "awful", "lose", "problem"])

def fallback_classify(text: str) -> str:
    toks = [t.lower() for t in re.findall(r"\w+", text)]
    pos = sum(1 for t in toks if t in POS_WORDS)
    neg = sum(1 for t in toks if t in NEG_WORDS)
    if pos == 0 and neg == 0:
        return "Neutral"
    return "Positive" if pos >= neg else "Negative"

client = MongoClient('localhost', 27017)
db = client['bigdata_project']
coll = db['tweets']

csv_path = 'Kafka-PySpark/twitter_validation.csv'
inserted = 0
with open(csv_path, encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row:
            continue
        tweet = row[-1]
        pred = fallback_classify(tweet)
        doc = { 'tweet': tweet, 'prediction': pred }
        coll.insert_one(doc)
        inserted += 1
print('Inserted', inserted, 'documents')
