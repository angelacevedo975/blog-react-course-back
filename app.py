from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<h1>Welcome to blog react course backend</h1>"

if __name__=="__main__":
    app.run(threaded=True, port=5000)