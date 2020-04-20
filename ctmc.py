#THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
#COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
import dbconfig as cfg
import json
import pymysql
from flask_cors import cross_origin, CORS
import Execute as e

application = Flask(__name__)
cors = CORS(application)

con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])

@application.route("/")
@cross_origin()
def home():
    return "Hello! Welcome to the backend, please go to the frontend <a href=\"http://ctmc-js.herokuapp.com/\">here</a>"


@application.route("/getAllTeams")
@cross_origin()
def getAllTeams():
    with con:
        res = e.execute(con, "select distinct name from teams")

        print(res)

        return res


@application.route("/getAllPlayers",  methods=['GET', 'OPTIONS'])
@cross_origin()
def getAllBatters():
    with con:
        res = e.execute(con, "SELECT concat(nameFirst, ' ', nameLast) as name FROM people order by nameLast")

        print(res)

        return res


@application.route('/<playerID>/generalData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getGeneralData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from people where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/battingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getBattingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Batting where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/pitchingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPitchingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Pitching where playerID = " + filtered + ";")

        print(res)

        return res


@application.route('/<playerID>/fieldingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getFieldingData(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Fielding where playerID = " + filtered + ";")

        print(res)

        return res

@application.route('/getBirthdayBoys', methods=['GET', 'OPTIONS'])
@cross_origin()
def getBirthdayBoys():
    with con:
        res = e.execute(con, "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from people where birthMonth ="
                             "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) and finalGame like '%2018%' order by debut - finalGame desc;")
        

        if res == "[]":
            print("NO INITIAL RESPONSE")
            res = e.execute(con, "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from people where birthMonth ="
                             "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) order by debut - finalGame desc;")
        print(res)

        return res

@application.route('/<playerID>/getPlayerUrl', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerUrl(playerID):
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select url from playerUrls where playerID = " + filtered + ";")

        print(res)

        return res

@application.route('/<playerID>/getPlayerSalaries+Avg', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerSalaries(playerID):
    with con:
        filtered = "'" + playerID + "'"
        plSal = e.execute(con, "select distinct a.yearID, s.salary, a.salary as 'average' from salaries as s"
                               " join averages as a using(yearID) where playerID = " + filtered + ";")
        print(plSal)

        return plSal


if __name__ == "__main__":
    application.run(debug=True, port="5000")
