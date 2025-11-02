import streamlit as st
import pickle
import pandas as pd
import datetime

# Load model
model = pickle.load(open('flight_rf.pkl', 'rb'))

# Streamlit Page Config
st.set_page_config(page_title="Flight Price Prediction", page_icon="✈️", layout="wide")

# CSS Styling
page_bg = """
<style>
/* App background */
[data-testid="stAppViewContainer"] {
    background-color: #e6f0ff;
}

/* Input container background */
div.block-container {
    background-image: url("https://plus.unsplash.com/premium_photo-1674343000769-204bb2026a8c?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YWVyb3BsYW5lfGVufDB8fDB8fHww&auto=format&fit=crop&q=60&w=500");
    background-size: cover;
    background-position: center;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.2);
}

/* Transparent overlay for readability */
div.block-container::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.85);
    z-index: -1;
}

/* Title styling */
h1, h5 {
    text-align: center;
    color: #003366;
}

/* Input fields and buttons */
.stSelectbox, .stNumberInput, .stTimeInput, .stDateInput {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 10px !important;
    padding: 8px;
}

button[kind="primary"] {
    background: linear-gradient(to right, #003366, #004080) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Page Header
st.markdown("<h1>✈️ Flight Price Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h5>Enter flight details below to get an estimated price</h5>", unsafe_allow_html=True)
st.write("")

# Input Layout
col1, col2, col3 = st.columns(3)

with col1:
    airline = st.selectbox('Airline', [
        'Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 
        'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers Premium economy',
        'Jet Airways Business', 'Vistara Premium economy', 'Trujet'
    ])
    source = st.selectbox('Source', ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    total_stops = st.selectbox('Total Stops', [0, 1, 2, 3, 4])

with col2:
    destination = st.selectbox('Destination', ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
    journey_date = st.date_input("Date of Journey", datetime.date.today())
    dep_time = st.time_input("Departure Time")

with col3:
    arrival_time = st.time_input("Arrival Time")
    duration_hours = st.number_input("Duration (hours)", min_value=0, max_value=30, value=2)
    duration_mins = st.number_input("Duration (minutes)", min_value=0, max_value=59, value=30)

# Feature extraction
journey_day = journey_date.day
journey_month = journey_date.month
Dep_hour = dep_time.hour
Dep_min = dep_time.minute
Arrival_hour = arrival_time.hour
Arrival_min = arrival_time.minute

# Base data
data = {
    'Total_Stops': total_stops,
    'Journey_day': journey_day,
    'Journey_month': journey_month,
    'Dep_hour': Dep_hour,
    'Dep_min': Dep_min,
    'Arrival_hour': Arrival_hour,
    'Arrival_min': Arrival_min,
    'Duration_hours': duration_hours,
    'Duration_mins': duration_mins,
}

# One-hot encoding
airlines = [
    'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
    'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
    'Trujet', 'Vistara', 'Vistara Premium economy'
]
sources = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
destinations = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']

for a in airlines:
    data['Airline_' + a] = 1 if a == airline else 0
for s in sources:
    data['Source_' + s] = 1 if s == source else 0
for d in destinations:
    data['Destination_' + d] = 1 if d == destination else 0

# Convert to DataFrame
final_df = pd.DataFrame([data])

# Prediction
st.markdown("---")
if st.button('Predict Flight Price 💰'):
    prediction = model.predict(final_df)
    output = round(prediction[0], 2)
    st.success(f"Estimated Flight Price: $ {output}")
    st.balloons()
