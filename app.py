from flask import Flask, jsonify
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes - Menu
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome API!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp_with_start_date:yyyy-mm-dd/<br/>"
        f"/api/v1.0/temp_with_start_and_end_date:yyyy-mm-dd/<br/>"
    )

# Flask Route Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
                        
    rain_days = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    session.close()
    dict_prec = list(np.ravel(rain_days))
    return jsonify(dict_prec)
   

# Flask Route Station   
@app.route("/api/v1.0/stations")
def stations():
    stationlist = session.query(Station.station, Station.name).all()
    dict_stat = list(np.ravel(stationlist))
    return jsonify(dict_stat)

# Flask Route Tobs   
@app.route("/api/v1.0/tobs")
def tobs():

    temp_obs = session.query(Measurement.date,  Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.date<="2017-08-23").all()
    dict_tobs = list(np.ravel(temp_obs))
    return jsonify(dict_tobs)


# Flask Route Temp_Start   
@app.route("/api/v1.0/<date>")
def temp_with_start_date(date):
    temp_me = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs).filter(Measurement.date)>=date).all()


    dict_temp = []

    for t in temp_me:
        start_dict = {}
        start_dict["Date"] = t.Date
        start_dict["Avg"] = t.func.avg(Measurement.tobs)
        start_dict["Min"] = t.func.min(Measurement.tobs)
        start_dict["Max"] = t.func.max(Measurement.tobs)
        dict_temp.append(start_dict)


    return jsonify(dict_temp)

if __name__ == '__main__':
    app.run(debug=True)