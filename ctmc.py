#THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
#COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
application = Flask(__name__)

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route('/testGet', methods=['GET'])
def retStuff():
    return jsonify({'hello': 'howdy'})

if __name__ == "__main__":
    application.run(debug=True, port="5000");