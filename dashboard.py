
import os 
import dash
import dash.dependencies as dd 
import dash_core_components as dcc 
import dash_html_components as html 
import dash_table 

import aadharEDA as aeda

from dash.dependencies import Input, Output
from flask import send_from_directory

#init the dash app
app = dash.Dash(__name__);


app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#figures from aadharEDA file without any Input Output bounds
india_map_fig = aeda.india_map()
pie_chart_fig = aeda.pie_chart()
hist_fig = aeda.hist()
registrar_fig =  aeda.registrar()
gender_state_fig = aeda.gender()

app.layout = html.Div(className='card', id='main-div', 

	children=[
	html.H1('Data Analysis of Aadhaar Card Generation in India.'),

	html.Hr(),
		
	html.Div(className='card', id='div1', children=[
		html.H3("Aadhar Generated in each State."),
		dcc.Graph(figure=india_map_fig)
		]),

	html.Br(), 
	html.Br(), 
	html.Hr(),

	html.Div(className='card', id='div2', children=[
		html.H3('Distrbution of Aadhar Card generated based on Gender.'),
		dcc.Graph(figure=pie_chart_fig)
		]),

	html.Br(),
	html.Br(),
	html.Hr(),

	html.Div(className='card', id='div3', children=[
		html.H3('Age Histogram'),
		dcc.Graph(figure=hist_fig),
		]),

	html.Br(),
	html.Br(),
	html.Hr(),

	html.Div(className='card', id='div4', children=[
		html.H3('Top Registrar Offices in India.'),
		dcc.Graph(figure=registrar_fig),
		]),

	html.Br(),
	html.Br(),
	html.Hr(),

	html.Div(className='card', id='div5', children=[
		html.H3(title='Gender wise distribution of each state.'),
		dcc.Graph(figure=gender_state_fig, style={'height': '120vh'}),
		]),

	html.Br(),
	html.Br(),
	html.Hr(),

	html.Div(className='card', id='div6', children=[
		html.H3(),
		html.Label('Enter the State Name:'),
		dcc.Input(style={"textAlign":"center"},
		 type="text", id="state_name", placeholder="Maharashtra.."),
		dcc.Graph(id="district_wise_fig"),
		]),

	html.Br(),
	html.Br(),
	html.Hr(),

	html.Div(className='card', id='div7', children=[
		html.H3(),

		html.Label('Enter the State Name:'),
		dcc.Input(style={"textAlign":"center"},  type="text", id="state_name1", placeholder="Maharashtra"),

		html.Label('Enter the District Name:'),
		dcc.Input(style={"textAlign":"center"}, type="text", id="district_name", placeholder="Pune"),
		
		dcc.Graph(id="district_wise_fig2"),
		
		]),
])


@app.callback(
	Output('district_wise_fig', 'figure'),
	[Input('state_name', 'value')]
	)
def fig1(value):
	if value == None:
		value = 'Maharashtra';
	return aeda.district_wise(value)

@app.callback(
	Output('district_wise_fig2', 'figure'),
	[Input('state_name1', 'value'),
	Input('district_name', 'value')]
	)
def fig2(state, district):
	if state == None and district==None:
		state = 'Maharashtra';
		district = 'Mumbai Suburban';
	return aeda.enrollment_agencies(state, district)

@app.server.route('/assets/<path>')
def static_file(path):
	static_folder = os.path.join(os.getcwd(), 'assets')
	return send_from_directory(static_folder, path)

if __name__ == '__main__':
	app.run_server(debug=True)
