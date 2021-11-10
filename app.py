import joblib
import pandas as pd
import numpy as np
import streamlit as st
import time
from math import pi, radians, cos, sin, asin, sqrt
import datetime
import pickle
import xgboost

def calc_haversine(lon1, lat1, lon2, lat2, is_deg=True):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    if is_deg:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = (sin(dlat/2)**2) + ((cos(lat1) * cos(lat2)) * sin(dlon/2)**2)
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km
model_filename = 'xgb_reg.pkl'
model = pickle.load(open(model_filename, "rb"))
def main():
    st.title('Seoul Bike Trip Duration Prediction')
    st.markdown('Just Enter the following details and we will predict the Duration of Bike Trip')
    st.warning('Only Enter Numeric Values in the Following Fields')

    # Input values
    distance = st.text_input("Total Distance")

    pickup_lat = st.text_input("Pickup latitude in degrees")
    pickup_long = st.text_input("Pickup Longitude in degrees")
    drop_lat = st.text_input("Drop Latitude in degrees")
    drop_long = st.text_input("Drop Longitude in degrees")

    pickuphour = st.text_input("Pickup Hour(Between 0 to 23)")
    pickupmin = st.text_input("Pickup Min(Between 0 to 59)")
    dropmin= st.text_input("Drop Min(Between 0 to 59)")
    
    wind = st.text_input("Wind")
    humid = st.text_input("Humid")
    solar = st.text_input("Solar")
    groundtemp = st.text_input("Ground Temperature")
    dust = st.text_input("Dust Concentration")

    bool = (distance and pickup_lat and pickup_long and drop_lat and drop_long and dropmin and pickupmin and pickuphour and \
        wind and humid and solar and groundtemp and dust)

    submit = st.button('Predict Duration')
    if submit: 
        if bool:
            with st.spinner('Predicting...'):
                time.sleep(2)
                distance, pickuphour, pickupmin, dropmin = int(distance), int(pickuphour), int(pickupmin), int(dropmin)
                wind, humid, solar, groundtemp, dust = float(wind), float(humid), float(solar), float(groundtemp), float(dust)
                pickup_lat, pickup_long, drop_lat, drop_long = float(pickup_lat), float(pickup_long), float(drop_lat), float(drop_long)
                haversine = calc_haversine(pickup_long,pickup_lat,drop_long,drop_lat)
                # ['Distance','Haversine','Phour','Pmin','Dmin','Wind','Humid','Solar','GroundTemp','Dust']
                x_test = np.array([[distance, haversine, pickuphour, pickupmin, dropmin,wind,humid,solar,groundtemp,dust]])
                prediction = model.predict(x_test)
                st.info(f"Your Duration is {np.round(prediction[0],2)} seconds")
        else:
            st.error('Please Enter All the Details')

if __name__ == '__main__':
    main()