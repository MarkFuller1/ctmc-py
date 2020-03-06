from flask import Flask
import dbconfig as cfg
import pymysql

application = Flask(__name__)
con= pymysql.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['db'])
    
@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    application.run(debug=True, port="5000")