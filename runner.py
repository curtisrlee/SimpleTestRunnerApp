import os
from pymongo import MongoClient
import datetime as dt

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = MongoClient('localhost', 27017)['test_app']

entry = db['queue'].find_one_and_delete({})
print(entry)