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





# date_start = real_data['Date'].iloc[22].to_pydatetime() #23 element
# date_end = real_data['Date'].iloc[-1].to_pydatetime() #przedosttni aby istniała predykcja

# # selected_date_end = st.slider('Wybierz datę końca okresu:', min_value=date_start, max_value=date_end)

# # Wybór daty końca okresu z dokładnością do godziny
# selected_date_end = st.slider('Wybierz datę końca okresu:', min_value=date_start, max_value=date_end, value=date_start, format="YYYY-MM-DD HH:mm")

# # hours_diff = (real_data['Date'].max().to_pydatetime() - selected_date_end).hours
# hours_diff = int((real_data['Date'].max().to_pydatetime() - selected_date_end).total_seconds() // 3600)
# # dodanie pola do wprowadzania liczby dni dla prognozy
# hours_count = st.number_input('Wybierz liczbę godzin na ile ma się wyświetlić predykcja:', min_value=2, max_value=hours_diff, value=2, step=1)

# # wybór prognozowanych danych
# start_index = real_data[real_data['Date'] == selected_date_end].index[0] - 22
# predicted = predicted_data.iloc[start_index : start_index + hours_count]

# selected_date_end = selected_date_end + pd.Timedelta(hours=hours_count)

# # wybór danych z ostatnich 23 godzin !sprawdzić!
# mask = (real_data['Date'] >= (selected_date_end - pd.Timedelta(hours=22))) & (real_data['Date'] <= selected_date_end)
# selected_data = real_data.loc[mask]

# # rysowanie wykresu za pomocą st.line_chart
# chart_data = pd.concat([selected_data.set_index('Date')['Power_consumption'], predicted.set_index('Date')['Power_consumption']], axis=1)
# chart_data.columns = ['Real', 'Predicted']
# st.line_chart(chart_data)