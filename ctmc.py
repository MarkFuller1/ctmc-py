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
    with con:
        cur = con.cursor()
        cur.execute("select * from Teams")
        results = cur.fetchall()


@application.route("/getAllPlayers",  methods=['GET'])
@cross_origin(origin='*')
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

@application.route('/<playerID>/generalData', methods=['GET'])
@cross_origin(origin='*')
def getGeneralData(playerID):
    with con:
        cur = con.cursor()
        cur.execute("select * from People where playerID = %s", (playerID))
        field_names = [i[0] for i in cur.description]
        results = cur.fetchall()

    return jsonify({'colnames': field_names,
                    'generalData': results})


@application.route('/<playerID>/battingData', methods=['GET'])
@cross_origin(origin='*')
def getBattingData(playerID):
    with con:
        cur = con.cursor()
        cur.execute("select * from Batting where playerID = %s", (playerID))
        results = cur.fetchall()
    return jsonify({'data': results})


@application.route('/<playerID>/pitchingData', methods=['GET'])
@cross_origin(origin='*')
def getPitchingData(playerID):
    with con:
        cur = con.cursor()
        cur.execute("select * from Pitching where playerID = %s", (playerID))
        results = cur.fetchall()
    return jsonify({'data': results})

@application.route('/<playerID>/fieldingData', methods=['GET'])
@cross_origin(origin='*')
def getFieldingData(playerID):
    with con:
        cur = con.cursor()
        cur.execute("select * from Fielding where playerID = %s", (playerID))
        results = cur.fetchall()
    return jsonify({'data': results})

if __name__ == "__main__":
    application.run(debug=True, port="5000")
