import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

real_data = pd.read_csv('predictions/real.csv')
real_data['Date'] = pd.to_datetime(real_data['Date'])
predicted_data = pd.read_csv('predictions/predictions.csv')
predicted_data['Date'] = pd.to_datetime(predicted_data['Date'])

st.title("Aplikacja do przewidywania zużycia energii elektrycznej")

# Ustawianie zakresu dat dla suwaka
date_start = real_data['Date'].min().to_pydatetime()
date_end = real_data['Date'].max().to_pydatetime()

# Wybór zakresu dat za pomocą suwaka
selected_date_range = st.slider('Wybierz zakres dat, dla których wyświetlisz rzeczywiste zużycie energii:', min_value=date_start, max_value=date_end, value=(date_start, date_end), format="YYYY-MM-DD HH:mm")

# Dodanie przełącznika
toggle_filter = st.checkbox('Porównaj przewidywane zużycie energii z rzeczywistym')

# Obsługa checkboxa
if toggle_filter:
    filtered_real_data = real_data[real_data['Date'] >= selected_date_range[0]]
else:
    filtered_real_data = real_data[(real_data['Date'] >= selected_date_range[0]) & (real_data['Date'] <= selected_date_range[1])]

# Filtrowanie danych predicted_data od daty końcowej na suwaku do końca
filtered_predicted_data = predicted_data[predicted_data['Date'] >= selected_date_range[1]]

# Łączenie danych na podstawie kolumny 'Date'
merged_data = pd.merge(filtered_real_data, filtered_predicted_data, on='Date', how='outer', suffixes=('_Real', '_Pred'))

# Przygotowanie danych do wykresu
chart_data = merged_data[['Date', 'Power_consumption_Real', 'Power_consumption_Pred']].melt('Date', var_name='Type', value_name='Power_consumption')

# Tworzenie wykresu za pomocą Altair
chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X('Date:T', title='Data i godzina', axis=alt.Axis(format='%Y-%m-%d %H:%M')),
    y=alt.Y('Power_consumption:Q', title='Zużycie energii (MW)'),
    color='Type:N'
).properties(
    width=800,
    height=400
).interactive()

# Wyświetlanie wykresu w Streamlit
st.altair_chart(chart, use_container_width=True)

# Wyświetlanie liczby elementów w filtered_predicted_data pod wykresem
st.markdown(f"""
    <div style="font-size:20px; font-family:Arial; color:grey;">
        Liczba godzin na ile wyświetlana jest predykcja: {len(filtered_predicted_data)}
    </div>
""", unsafe_allow_html=True)

# Wyświetlanie liczby elementów w filtered_predicted_data pod wykresem
st.markdown(f"""
    <div style="font-size:20px; font-family:Arial; color:grey;">
        Liczba dni na ile wyświetlana jest predykcja: {len(filtered_predicted_data) // 23}
    </div>
""", unsafe_allow_html=True)

# Dodanie niestandardowego CSS do rozszerzenia szerokości aplikacji
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding-left: 5%;
        padding-right: 5%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
