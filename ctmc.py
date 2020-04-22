# THIS FILE HOUSES MAIN APPLICATION AND ENDPOINTS
# COMPLEX CALCULATION AND DB QUERIES SHOULD BE MADE ELSEWHERE

from flask import Flask, jsonify
import dbconfig as cfg
import json
import pymysql
from flask_cors import cross_origin, CORS
import Execute as e

application = Flask(__name__)
cors = CORS(application)



@application.route("/")
@cross_origin()
def home():
    return "Hello! Welcome to the backend, please go to the frontend <a href=\"http://ctmc-js.herokuapp.com/\">here</a>"


@application.route("/getAllTeams")
@cross_origin()
def getAllTeams():
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        res = e.execute(con, "select distinct name from teams")

        print(res)
    con.close()
    return res



@application.route("/getAllPlayers",  methods=['GET', 'OPTIONS'])
@cross_origin()
def getAllBatters():
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        res = e.execute(con, "SELECT concat(nameFirst, ' ', nameLast) as name FROM people order by nameLast")

        print(res)

    con.close()
    return res


@application.route('/<playerID>/generalData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getGeneralData(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from people where playerID = " + filtered + ";")

        print(res)

    con.close()
    return res


@application.route('/<playerID>/battingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getBattingData(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Batting where playerID = " + filtered + ";")

        print(res)

    con.close()
    return res


@application.route('/<playerID>/pitchingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPitchingData(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Pitching where playerID = " + filtered + ";")

        print(res)

    con.close()
    return res


@application.route('/<playerID>/fieldingData', methods=['GET', 'OPTIONS'])
@cross_origin()
def getFieldingData(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select * from Fielding where playerID = " + filtered + ";")

        print(res)

    con.close()
    return res


@application.route('/getBirthdayBoys', methods=['GET', 'OPTIONS'])
@cross_origin()
def getBirthdayBoys():
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        res = e.execute(con,
                        "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from people where birthMonth ="
                        "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) and finalGame like '%2018%' order by debut - finalGame desc;")

        if res == "[]":
            print("NO INITIAL RESPONSE")
            res = e.execute(con,
                            "select concat(nameFirst, ' ' , nameLast) as name, birthYear as year, playerid from people where birthMonth ="
                            "MONTH(CURDATE()) and birthDay = DAY(CURDATE()) order by debut - finalGame desc;")
        print(res)

    con.close()
    return res


@application.route('/<playerID>/getPlayerUrl', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerUrl(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        res = e.execute(con, "select url from playerUrls where playerID = " + filtered + ";")

        # res = json.dumps(json.loads(res).append({"url": "https://pecb.com/conferences/wp-content/uploads/2017/10/no-profile-picture.jpg"}))

        print(res)

    con.close()
    return res


@application.route('/<playerID>/getPlayerSalaries+Avg', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerSalaries(playerID):
    con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with con:
        filtered = "'" + playerID + "'"
        plSal = e.execute(con, "select distinct a.yearID, s.salary, a.salary as 'average' from salaries as s"
                               " join averages as a using(yearID) where playerID = " + filtered + ";")
        print(plSal)
    con.close()
    return plSal


@application.route('/<playerID>/getPlayerTeams', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerTeams(playerID):
    connection = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with connection:
        filtered = "'" + playerID + "'"
        pl = e.execute(connection, "select distinct teamID as 'Team', count(distinct yearID, playerID) as 'Years'"
                            " from appearances where playerID = " + filtered + " group by teamID;")
        print(pl)
    connection.close()
    return pl

@application.route('/<playerID>/getBadges', methods=['GET', 'OPTIONS'])
@cross_origin()
def getPlayerBadges(playerID):
    connection = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with connection:
        filtered = "'" + playerID + "'"
        pl = e.execute(connection, "select inducted, awardID, a.yearid from halloffame h join awardsplayers a on"
                                   " h.playerID = a.playerID where h.playerID = "+ filtered + " and inducted ='Y' "
                                   "group by awardID, inducted having inducted = 'Y';")
        print(pl)
    connection.close()
    return pl

@application.route('/search/<search>', methods=['GET'])
@cross_origin(origin='*')
def search(search):
    connection = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    with connection:
        filtered = "" + search + ""
        plSal = e.execute(connection, "(select distinct concat(nameFirst, ' ', nameLast) as v, playerId as k, 'p' as type from people where concat(nameFirst, ' ' , nameLast) like '%" + search + "%' limit 10) union "
            "(select distinct name, teamId, 't'  from teams where name like '%" + search + "%' limit 10) "
            "union (select distinct parkname , id, 'f'  from parks where parkname like '%" + search + "%' or parkalias like '%" + search + "%' limit 10) ; ")
        print(plSal)

        return plSal


if __name__ == "__main__":
    application.run(debug=True, port="5000")
