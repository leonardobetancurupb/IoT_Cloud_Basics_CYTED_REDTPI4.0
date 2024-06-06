import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as bdc
import plotly.graph_objs as go
from dash.dependencies import Input, Output 

app = dash.Dash(__name__, external_stylesheets=[bdc.themes.BOOTSTRAP])

app.layout = html.Div([
   bdc.NavbarSimple(
       brand= "Mi proyecto de IoT la planta con maceta inteligente",
       dark = True,
       color="primary",
       children=[bdc.NavItem(bdc.NavLink("Inicio",href="/inicio")),bdc.NavItem(bdc.NavLink("sensores",href="/sensores")),bdc.NavItem(bdc.NavLink("informacion",href="/informacion"))]
   ),
   dcc.Location(id='url'),
   html.Div(id='contenido'),
   html.Footer("Mi proyecto (c) 2024")
])

inicio_layout = html.Div([
    html.H2("pagina para la informacion del proyecto"),
    html.P("Este es un proyecto de internet d elas cosas que permite bla bla bla bla"),
    html.H2("Begonia Conchita"),
    html.P("esta planta es una flor de colores etc etc etc"),
    html.Img(src='./assets/fotoplanta.png',alt='Plantica')

])

sensores_layout = html.Div([
    html.H2("pagina para graficar los sensores"),
    dcc.Graph(
        id = 'temperaturavstiempo',
        figure = {
            'data':[ go.Scatter(x=[0, 1, 2, 3, 4],y=[24.2, 23.3, 25.5, 26.9, 24.3],name='Temperatura')],
            'layout': go.Layout(title='Temperatura vs Tiempo',xaxis={'title':'Tiempo'},yaxis={'title':'Temperatura'})
        }
    ),
    dcc.Graph(
        id = 'hunedadvstiempo',
        figure = {
            'data':[ go.Scatter(x=[0, 1, 2, 3, 4],y=[67, 70, 68, 72, 77],name='Humedad')],
            'layout': go.Layout(title='Humedad vs Tiempo',xaxis={'title':'Tiempo'},yaxis={'title':'Humedad'})
        }
    )
])

informacion_layout = html.Div([
    html.H2("pagina para mostrar las fotos de las plantas y el historico de resutlados")
])

@app.callback(Output('contenido','children'),Input('url','pathname'))
def mostrarcontenido(pathname):
    if pathname == '/inicio' or pathname == '/':
        return inicio_layout
    elif pathname == '/sensores':
        return sensores_layout
    elif pathname == '/informacion':
        return informacion_layout
    else:
        return "error 500"


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80)
