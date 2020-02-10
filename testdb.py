from pymongo import MongoClient

Mongo_URI = 'mongodb://52.254.64.58'

client = MongoClient(Mongo_URI)

client['TestWAF']
