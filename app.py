#!flask/bin/python
import config
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import urlparse
from flask import Flask, request, abort, jsonify
app = Flask(__name__)

def get_db_connection():    
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(config.DATABASE_URL)

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/')
def hello_world():
    with get_db_connection() as conn:
        pass
    return 'Hello World!'

@app.route('/api/v1.0/checkins', methods = ["POST"])
def checkin():
    '''
    Add the checkin to the db and return the new checkin record as json
    '''
    try:
        name = request.args['name']
        message = request.args['message']
        lat = request.args['lat']
        lon = request.args['lon']
        checkin_time = request.args['checkin_time']
    except KeyError:
        abort(400)
    
    # Add this checkin to the database 
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query_string = '''INSERT INTO checkins (name, message, lat, lon, checkin_time) VALUES (%s, %s, %s, %s, %s) RETURNING id, name, message, lat, lon, checkin_time;;'''
            cur.execute(query_string, (name, message, lat, lon, checkin_time))
            record = cur.fetchone()
            
            # turn the datetime.datetime into a string
            record["checkin_time"] = str(record["checkin_time"])
            
            return jsonify(record)

    
@app.route("/api/v1.0/lastcheckins", methods = ["GET"])
def get_latest_checkins():
    # For each name, get the latest checking
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query_string = ''' SELECT id, name, message, lat, lon, checkin_time FROM (
                                    SELECT id, name, message, lat, lon, checkin_time, MAX(checkin_time) OVER (PARTITION BY name) AS max_checkin_time FROM checkins
                                ) AS temp_table WHERE checkin_time = max_checkin_time;'''
            cur.execute(query_string)
            records = cur.fetchall()
            
            # Turn all the datetime.datetimes into strings
            for record in records:
                record["checkin_time"] = str(record["checkin_time"])
                
            return jsonify({"checkins":records})



if __name__ == '__main__':
    app.run(debug = True)