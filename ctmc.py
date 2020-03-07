#THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
#COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
import dbconfig as cfg
import pymysql
import json
from flask_cors import cross_origin

application = Flask(__name__)
con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])

@application.route("/")
@cross_origin()
def hello():
    return "<h1 style='color:blue'>If your looking for the DB project this is the backend</h1>"

@application.route('/testGet', methods=['GET'])
@cross_origin(origin= '*')
def retStuff():
    with con:
        cur = con.cursor()
        cur.execute("select * from Teams")
        results = cur.fetchall()
    return jsonify({'data': results})


@application.route("/getAllPlayers",  methods=['GET'])
@cross_origin(origin= '*')
def getAllBatters():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Batting")

        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    application.run(debug=True, port="5000")
