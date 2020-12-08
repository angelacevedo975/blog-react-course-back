from flask import Flask
from flask_cors import CORS
import pymongo

connection_url= "mongodb+srv://testuser:qwerty12345678@blogclickit.pi9km.mongodb.net/blog?retryWrites=true&w=majority"
db_name="blog"

client= pymongo.MongoClient( connection_url )

database= client.get_database(db_name)