import pymysql
import json

def execute(con, query):
    cur = con.cursor()
    cur.execute(query)
    cur.close()

    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return json.dumps(json_data, indent=4, sort_keys=True, default=str)
