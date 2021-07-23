from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect Database into ORM class
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the home page! Available routes can be viewed here.<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation values by date:<br/>     /api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of stations in the data:<br/>     /api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature observations from the previous year of the most active station:<br/>     /api/v1.0/tobs<br/>"
        f"<br/>"
        f"Descriptive statistics for temperature given a start date (yyyy-mm-dd):<br/>     /api/v1.0/yyyy-mm-dd<br/>"
        f"<br/>"
        f"Descriptive statistics for temperature given a start date and end date (yyyy-mm-dd):<br/>     /api/v1.0/yyyy-mm-dd<start>/yyyy-mm-dd<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    # Query the desired data
    selection = [Measurement.date, Measurement.prcp]
    query = session.query(*selection).all()
    # Close Session
    session.close()
        
    #accumulate our data in proper format
    precip_values = []
    for date, precip in query:
        each_entry = {}
        each_entry["Date"] = date
        each_entry["Precip"] = precip
        precip_values.append(each_entry)
        
    #return a json of data
    return jsonify(precip_values)




@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    # Query the desired data
    selection = [Station.station, Station.name]
    query = session.query(*selection).all()
    # Close Session
    session.close()
    
    #accumulate our data in proper format
    station_values = []
    for station, name in query:
        each_entry = {}
        each_entry["Station ID"] = station
        each_entry["Name"] = name
        station_values.append(each_entry)
        
    #return a json of data
    return jsonify(station_values)




@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Find the most active station
    selection =[Measurement.station, func.count(Measurement.station)]
    most_active = session.query(*selection).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active_station = most_active[0]
    # Query the desired data from the past year
    selection2 = [Measurement.date, Measurement.tobs]
    query = session.query(*selection2).filter(Measurement.date >= year_ago).filter(Measurement.station == most_active_station).all()
    # Close Session
    session.close()

    #accumulate our data in proper format
    tobs_values = []
    for date, tobs in query:
        each_entry = {}
        each_entry["Date"] = date
        each_entry["Temperature"] = tobs
        tobs_values.append(each_entry)
        
    #return a json of data
    return jsonify(tobs_values)




@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    # Query the desired data
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    query = session.query(*selection).filter(Measurement.date >= start_date).all()
    # Close Session
    session.close()
    
    #accumulate our data in proper format
    date_values = []
    for min_temp, max_temp, avg_temp  in query:
        each_entry = {}
        each_entry["min_temp"] = min_temp
        each_entry["max_temp"] = max_temp
        each_entry["avg_temp"] = avg_temp
        date_values.append(each_entry)
        
    #return a json of data
    return jsonify(date_values)

    
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    # Query the desired data
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    query = session.query(*selection).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # Close Session
    session.close()
    
    #accumulate our data in proper format
    date_values = []
    for min_temp, max_temp, avg_temp  in query:
        each_entry = {}
        each_entry["min_temp"] = min_temp
        each_entry["max_temp"] = max_temp
        each_entry["avg_temp"] = avg_temp
        date_values.append(each_entry)
        
    #return a json of data
    return jsonify(date_values)    
    
    
    
if __name__ == "__main__":
    app.run(debug=True)