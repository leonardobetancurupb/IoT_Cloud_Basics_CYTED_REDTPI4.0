import math
import pandas as pd
import numpy as np
import dash
from dash import html, dcc, Output, Input
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
from flask import Flask, request, jsonify
from flask_cors import CORS
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def calculate_aqi(pm25):
    if pm25 <= 12.0:
        aqi = math.ceil((pm25 / 12.0) * 50)
        name = "Good"
        color = (0, 228, 0)
        # color = (0/255, 228/255, 0/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "None"
        caution_info = "None"
    elif pm25 <= 35.4:
        aqi = math.ceil(((pm25 - 12.1) / (35.4 - 12.1)) * (100 - 51) + 51)
        name = "Moderate"
        color = (255, 255, 0)
        # color = (255/255, 255/255, 0/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Unusually sensitive people should consider reducing prolonged or heavy exertion."
        caution_info = "Unusually sensitive people should consider reducing prolonged or heavy exertion."
    elif pm25 <= 55.4:
        aqi = math.ceil(((pm25 - 35.5) / (55.4 - 35.5)) * (150 - 101) + 101)
        name = "Unhealthy for Sensitive Groups"
        color = (255, 126, 0)
        # color = (255/255, 126/255, 0/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Increasing likelihood of respiratory symptoms in sensitive individuals, aggravation of heart or lung disease and premature mortality in persons with cardiopulmonary disease and the elderly."
        caution_info = "People with respiratory or heart disease, the elderly and children should limit prolonged exertion."
    elif pm25 <= 150.4:
        aqi = math.ceil(((pm25 - 55.5) / (150.4 - 55.5)) * (200 - 151) + 151)
        name = "Unhealthy"
        color = (255, 0, 0)
        # color = (255/255, 0/255, 0/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Increased aggravation of heart or lung disease and premature mortality in persons with cardiopulmonary disease and the elderly; increased respiratory effects in general population."
        caution_info = "People with respiratory or heart disease, the elderly and children should avoid prolonged exertion; everyone else should limit prolonged exertion."
    elif pm25 <= 250.4:
        aqi = math.ceil(((pm25 - 150.5) / (250.4 - 150.5)) * (300 - 201) + 201)
        name = "Very Unhealthy"
        color = (143, 63, 151)
        # color = (143/255, 63/255, 151/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Significant aggravation of heart or lung disease and premature mortality in persons with cardiopulmonary disease and the elderly; significant increase in respiratory effects in general population."
        caution_info = "People with respiratory or heart disease, the elderly and children should avoid any outdoor activity; everyone else should avoid prolonged exertion."
    elif pm25 <= 350.4:
        aqi = math.ceil(((pm25 - 250.5) / (350.4 - 250.5)) * (400 - 301) + 301)
        name = "Hazardous"
        color = (126, 0, 35)
        # color = (126/255, 0/255, 35/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Serious aggravation of heart or lung disease and premature mortality in persons with cardiopulmonary disease and the elderly; serious risk of respiratory effects in general population."
        caution_info = "Everyone should avoid any outdoor exertion; people with respiratory or heart disease, the elderly and children should remain indoors."
    elif pm25 <= 500.4:
        aqi = math.ceil(((pm25 - 350.5) / (500.4 - 350.5)) * (500 - 401) + 401)
        name = "Hazardous"
        color = (126, 0, 35)
        # color = (126/255, 0/255, 35/255)
        sensitive_info = "People with respiratory or heart disease, the elderly and children are the groups most at risk."
        health_info = "Serious aggravation of heart or lung disease and premature mortality in persons with cardiopulmonary disease and the elderly; serious risk of respiratory effects in general population."
        caution_info = "Everyone should avoid any outdoor exertion; people with respiratory or heart disease, the elderly and children should remain indoors."
    else:
        aqi = None
        name = "Invalid"
        sensitive_info = "Invalid"
        health_info = "Invalid"
        caution_info = "Invalid"
    
    return aqi, name, sensitive_info, health_info, caution_info

customer_json_file ='http://siata.gov.co/EntregaData1/Datos_SIATA_Aire_AQ_pm25_Last.json'
datos = pd.read_json(customer_json_file, convert_dates=True)
customers_json = pd.json_normalize(datos['measurements'])
customers_json = customers_json[customers_json['value']>=0]
customers_json['date.local'] = pd.to_datetime(customers_json['date.local'])
customers_json = customers_json[customers_json['date.local'] == customers_json['date.local'].max()]
latitudes = customers_json['coordinates.latitude'].tolist()
longitudes = customers_json['coordinates.longitude'].tolist()
m = customers_json['value'].tolist()

# en la variable m esta el nivel de la ultima fecha
#creo una malla de 100 x 100 en el area
m=np.array(m)
ysuperior=max(latitudes)
yinferior=min(latitudes)
xinferior=min(longitudes)
xsuperior=max(longitudes)
grid_x, grid_y = np.meshgrid(np.linspace(xinferior,xsuperior,100), np.linspace(yinferior,ysuperior,100))

grid_z0 = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='nearest')
grid_z1 = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='linear')
grid_z2 = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='cubic')

# Llenar los datos NaN con el valor de nearest para completar los datos en z1 y z2
grid_z1 = np.where(np.isnan(grid_z1), grid_z0, grid_z1)
grid_z2 = np.where(np.isnan(grid_z2), grid_z0, grid_z2)

x = grid_x.ravel()
y = grid_y.ravel()
z = grid_z2.ravel()

aqi_data = [calculate_aqi(i) for i in z]
aqi = np.array([data[0] for data in aqi_data])
name = np.array([data[1] for data in aqi_data])
sensitive_info = np.array([data[2] for data in aqi_data])
health_info = np.array([data[3] for data in aqi_data])

text = ['<b>AQI:</b> {}\n<br><b>PM 2.5:</b> {}\n<br><b>Name:</b> {}\n<br><b>Sensitive Info:</b> {}\n<br><b>Health Info:</b> {}'.format(*t) for t in zip(aqi, z, name, sensitive_info, health_info)]

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def assign_color(aqi):
    if aqi is None:
        return rgb_to_hex((0, 0, 0))
    elif aqi <= 50:
        return rgb_to_hex((0, 228, 0))  # green
    elif aqi <= 100:
        return rgb_to_hex((255, 255, 0))  # yellow
    elif aqi <= 150:
        return rgb_to_hex((255, 126, 0))  # orange
    elif aqi <= 200:
        return rgb_to_hex((255, 0, 0))  # red
    elif aqi <= 300:
        return rgb_to_hex((143, 63, 151))  # purple
    else:  # AQI > 300
        return rgb_to_hex((126, 0, 35))  # maroon

colors = np.array([assign_color(aqi_value) for aqi_value in aqi])

fig = go.Figure(go.Scattermapbox(
    lat=y,
    lon=x,
    mode='markers',
    marker=dict(
        size=10,
        color=colors,
    ),
    text=text,
))

fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=180)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

server = Flask(__name__)

CORS(server)

@server.route('/aqi', methods=['POST'])
def get_aqi():
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']

    dist = np.sqrt((grid_x - lon)**2 + (grid_y - lat)**2)
    nearest = dist.argmin()

    aqi_value = int(aqi[nearest])
    color = colors[nearest]
    name_value = name[nearest]
    sensitive_info_value = sensitive_info[nearest]
    health_info_value = health_info[nearest]

    return jsonify({
        'aqi': aqi_value,
        'color': color,
        'name': name_value,
        'sensitive_info': sensitive_info_value,
        'health_info': health_info_value,
    })

app = dash.Dash(server=server,routes_pathname_prefix="/")
app.layout = html.Div([
    dcc.Graph(figure=fig, id="mimapa"),
])

app.run_server(debug=True, use_reloader=False, host='0.0.0.0',port=80)
