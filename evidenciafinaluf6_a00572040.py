import streamlit as st
import pandas as pd
import altair as alt
#import numpy as np
#import plotly as px
#import plotly.figure_factory as ff
#from bokeh.plotting import figure
import matplotlib.pyplot as plt
from PIL import Image

imagen = Image.open('San_francisco.jpeg')

st.image(imagen, use_column_width=True)

st.title('Police Incident Reports from 2018 to 2020 in San Francisco')

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Year'] = df['Incident Year']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Supervisor'] = df['Supervisor District']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

with st.sidebar:
    st.header('Luis Pablo Padilla Barbosa')
    st.header('A00572040')
    st.markdown('Select the options you want to filter the data')

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
'Incident Category',
subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]
            
subset_data3 = subset_data
incident_input = st.sidebar.multiselect(
'Year',
subset_data.groupby('Year').count().reset_index()['Year'].tolist())
if len(incident_input) > 0:
    subset_data3 = subset_data[subset_data['Year'].isin(incident_input)]

subset_data3

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(subset_data3)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Police_Data.csv',
    mime='text/csv',
)



st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')    
st.divider()
st.markdown('Crime locations in San Francisco')
st.map(subset_data3)



st.divider()
data = subset_data3.Day.value_counts()
data = pd.DataFrame(data).reset_index()
st.markdown('Crimes ocurred per day of the week')
graf1=alt.Chart(data).mark_arc().encode(
    theta= alt.Theta(field= 'Day', type='quantitative'), 
    color = alt.Color(field='index', type='nominal', scale = alt.Scale(scheme='blueorange')),
)

st.altair_chart(graf1, use_container_width=True)


agree1 = st.button('Click to see Crimes ocurred per date')
if agree1:
    st.markdown('Crimes ocurred per date')
    st.line_chart(subset_data3['Date'].value_counts())


st.divider()
st.markdown('Crimes ocurred per Supervisor')

data3 = subset_data3.Supervisor.value_counts()
data3 = pd.DataFrame(data3).reset_index()
graf3=alt.Chart(data3).mark_bar(size=30).encode(
    x=alt.X(
        'index',
        title='Supervisor'),
      y =alt.Y(
          'Supervisor',
          title='Crimes ocurred'),
)

st.altair_chart(graf3, use_container_width=True)

agree2 = st.button('Click to see Type of crimes committed')
if agree2:
    st.markdown('Type of crimes committed')
    st.bar_chart(subset_data3['Incident Category'].value_counts())




st.divider()
st.markdown('Resolution status')

data1 = subset_data3.Resolution.value_counts()
data1 = pd.DataFrame(data1).reset_index()
graf2=alt.Chart(data1).mark_arc().encode(
    theta= alt.Theta(field= 'Resolution', type='quantitative'), 
    color = alt.Color(field='index', type='nominal', scale = alt.Scale(scheme='blueorange')),
)

st.altair_chart(graf2, use_container_width=True)


agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data3['Incident Subcategory'].value_counts())

with st.sidebar:
    imagen = Image.open('Logo.png')
    st.image(imagen)

st.balloons()
