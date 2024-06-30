import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf

real_data = pd.read_csv('predictions/real.csv')
real_data['Date'] = pd.to_datetime(real_data['Date'])
predicted_data = pd.read_csv('predictions/predictions.csv')
predicted_data['Date'] = pd.to_datetime(predicted_data['Date'])

st.title("Aplikacja do przewidywania zużycia energii elektrycznej")

# Łączenie danych na podstawie kolumny 'Date'
merged_data = pd.merge(real_data, predicted_data, on='Date', suffixes=('_Real', '_Predicted'))

# Rysowanie wykresu za pomocą st.line_chart
st.line_chart(merged_data.set_index('Date')[['Power_consumption_Real', 'Power_consumption_Predicted']])
