#THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
#COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
import dbconfig as cfg
import pymysql
from flask_cors import cross_origin
import Execute as e

application = Flask(__name__)
con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])

@application.route("/")
@cross_origin()
def home():
    return "Hello! Welcome to the backend, please go to the frontend <a href=\"http://ctmc-js.herokuapp.com/\">here</a>"


@application.route("/getAllTeams")
@cross_origin(origin='*')
def getAllTeams():
    with con:
        res = e.execute(con, "select name from Teams")

        print(res)

        return res


@application.route("/getAllPlayers",  methods=['GET'])
@cross_origin(origin='*')
def getAllBatters():
    with con:
        res = e.execute(con, "SELECT concat(nameFirst, ' ', nameLast) as name FROM People order by nameLast")

        print(res)

        return res


@application.route('/<playerID>/generalData', methods=['GET'])
@cross_origin(origin='*')
def getGeneralData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from People where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/battingData', methods=['GET'])
@cross_origin(origin='*')
def getBattingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Batting where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/pitchingData', methods=['GET'])
@cross_origin(origin='*')
def getPitchingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Pitching where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/fieldingData', methods=['GET'])
@cross_origin(origin='*')
def getFieldingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Fielding where playerID = " + filtered + ";")

        print(res)

        return res

@application.route('/getBirthdayBoys', methods=['GET'])
@cross_origin(origin='*')
def getBirthdayBoys():
    with con:
        res = e.execute(con, "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from People where birthMonth ="
                             "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) and finalGame like '%2018%' order by debut - finalGame desc;")
        

        if res == "[]":
            print("NO INITIAL RESPONSE")
            res = e.execute(con, "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from People where birthMonth ="
                             "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) order by debut - finalGame desc;")
        print(res)

        return res

@application.route('/<playerID>/getPlayerUrl', methods=['GET'])
@cross_origin(origin='*')
def getplayerurl(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select url from playerUrls where playerID = " + filtered + ";")

        print(res)

        return res

if __name__ == "__main__":
    application.run(debug=True, port="5000")
