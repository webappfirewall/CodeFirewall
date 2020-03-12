import urllib.parse
from pymongo import MongoClient

username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&.12345')
client = MongoClient('mongodb://%s:%s@192.168.17.146' % (username, passwor))