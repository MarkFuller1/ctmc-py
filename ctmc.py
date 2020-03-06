from flask import Flask
import dbconfig as cfg
import pymysql
import json

application = Flask(__name__)
con = pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@application.route("/getAllPlayers")
def getAllBatters():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM People")

        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    application.run(debug=True, port="5000")
