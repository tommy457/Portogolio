#!/usr/bin/python3
from portogolio import app
from models import storage

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

if __name__ == "__main__":
    """ Main Entry point """
    app.run(host='0.0.0.0', port=5000, debug=True)
