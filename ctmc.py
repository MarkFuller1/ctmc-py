#THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
#COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
application = Flask(__name__)
import dbconfig as cfg
import pymysql

application = Flask(__name__)
con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    
@application.route("/")
def hello():
    return "<h1 style='color:blue'>If your looking for the DB project this is the backend</h1>"

@application.route('/testGet', methods=['GET'])
def retStuff():
    with con:
        cur = con.cursor()
        cur.execute("select * from Teams")
        results = cur.fetchall()
    return jsonify({'data': results})

if __name__ == "__main__":
    application.run(debug=True, port="5000")