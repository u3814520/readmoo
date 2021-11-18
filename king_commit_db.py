from pymongo import MongoClient
import json

client = MongoClient(host='10.2.14.10',port=27017)
db = client.userstar
coll = db.king_commit



with open (,'r',encoding='utf-8') as f:
    for a in f:
        ccc=json.loads(a)
        coll.insert([ccc])