import numpy as np
import pandas as pd
import datetime as dt
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

myDir = os.getcwd()
print (myDir)
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
print ("Done loading")
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/temp/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data for the last year"""
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    session.close()
    
    precip = {date: prcp for date, prcp in precipitation}
    
    # Return the JSON representation of your dictionary
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations."""
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    # Return a JSON list of stations from the dataset
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp observations for the previous year"""

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))

    # Return a JSON list of tobs for previous year
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min temp, the avg temp, and the max temp"""

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        session.close()

        temps = list(np.ravel(results))

        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)


    



   