# Setup

## Flask
Do the following:

    $ cd wheres-carl
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Create a file called `config.py` in this directory containing the following:

    DATABASE_URL = "postgres://<username>:<password>@localhost:5432/<dbname>"
    
Dont forget to replace the bracketed statements with actual values.

## Database

Assuming you are in a psql prompt as <username> in <dbname>, build the table:
Build the table:

    CREATE TABLE checkins (
        id              serial PRIMARY KEY,
        name            text,
        message         text,
        lat             real,
        lon             real,
        checkin_time    timestamp NOT NULL DEFAULT statement_timestamp()
    );

# Running the server

Start your database, and run the server with:
    
    $ python app.py

Test posting with this:

    curl -X POST -i "http://localhost:5000/api/v1.0/checkins?name=Bob&message=mymessage&lat=9001&lon=2001&checkin_time=2014-04-09%2018%3A00%3A00.000000"

Test getting the latest checkins with this:

    curl -i "http://localhost:5000/api/v1.0/lastcheckins"