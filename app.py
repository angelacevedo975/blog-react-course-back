from  flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
from db import database
import datetime

app = Flask(__name__)

CORS(app)

posts= database.posts

@app.route("/api/posts/<page>", methods=["GET"])
def get_posts(page):
   query= posts.find({}).sort("date", -1).skip(int(page)*9).limit(9)
   output = []
   for post in query:
       output.append(post)
       output[-1]["_id"]= str(output[-1]["_id"])
       output[-1]["text"] = output[-1]["text"][:150]+"..."
       
   if len(output) < 5:
       next=None
   else:
       next=int(page)+1
   return jsonify({"response":output, "page":{"current": int(page), "next": next}})


@app.route("/api/post/create", methods=["POST"])
def add_post():
    data= request.json
    date= datetime.datetime.now()

    try:
        db_object= { "title": data["title"], "text": data["text"], "author": data["author"], "date":date }
    except:
        return jsonify({"error": "Wrong attributes"})
    
    print(data.get("category"))

    try:
        posts.insert_one( db_object )
    except:
        return jsonify({ "error": "database connection error" })
    
    db_object["_id"]= str(db_object["_id"])
    return jsonify({ "response": db_object })


@app.route("/api/post/<id>", methods=["GET"])
def get_post(id):
    try:
        post_id= ObjectId(id)
    except:
        return jsonify({"error": "Invalid id passed"})
    
    try:
        post= posts.find_one( {"_id": post_id } )
    except:
        return jsonify({"error": "Failed to get from database"})
    
    if post:
        post["_id"]= str(post["_id"])
        return jsonify({"response": post})
    return jsonify({"error": "Post not found"})


@app.route("/api/post/<id>/update", methods=["PUT"])
def update_post(id):
    try:
        user_id= ObjectId(id)
    except:
        return jsonify({"error":"Invalid id passed"})

    data= request.json
    update_data=["title", "text","category","tags"]
    db_data={}
    for dat in update_data:
        try:
            db_data[dat] = data[dat]
        except:
            continue
    
    try:
        posts.update_one({"_id": user_id}, {"$set": db_data})
    except:
        return jsonify({"error": "database error"})
    
    updated_post= posts.find_one({"_id": user_id})
    updated_post["_id"]= str( updated_post["_id"] )
    return jsonify({"response": updated_post})


@app.route("/api/post/<id>/delete", methods=["DELETE"])
def delete_post(id):
    try:
        user_id= ObjectId(id)
    except:
        return jsonify({"error": "Invalid id passed" })
    
    try:
        deleted= posts.delete_one({"_id": user_id})
        print(deleted)
    except:
        return jsonify({"error": "Database error"})

    return jsonify({"response": "Done"})

@app.route("/", methods=["GET"])
def welcome():
    return "<h1>Welcome to blog react course backend</h1>"


if __name__=='__main__':
    app.run(debug=True)