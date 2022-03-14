import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 
import warnings
import json

# get_ipython().run_line_magic('matplotlib', 'inline')
# plt.style.use('dark_background')

mapbox_access_token =  'pk.eyJ1IjoiYmxhY2tpc2hncmF5IiwiYSI6ImNrbzQ2eDlzNTBtcW8ydXBkbGo2ODBxejUifQ.j-pYET58qvPgO9og--uQ-g'
px.set_mapbox_access_token(mapbox_access_token)

warnings.simplefilter(action='ignore')

df = pd.read_csv(r'UIDAI-ENR-DETAIL-20170308.csv')
data = df.copy()

# for i in data.columns:
#     print(f"For {i.upper()} the value counts is {len(data[i].value_counts())} and unique values is {len(data[i].unique())}")

labels = ["Male", 'Female', 'Transgender']

def pie_chart():
    fig = px.pie(data_frame=data, values=data['Gender'].value_counts(), names=labels)
    fig.update_layout(template='plotly_dark')
    fig.update_traces(hovertemplate="%{label}: %{value}", hoverlabel=dict(
        bgcolor = 'white',
        font_size=20,
        font_family='Arial',
    ))
    return fig

# pie_chart()

data["State"] = data["State"].replace('Dadra and Nagar Haveli','Dadra and Nagar Havelli')
a = data['State'].value_counts().index

geojson = open(r"states_india.geojson")
geojson_India = json.load(geojson)
featues = geojson_India['features']
list_of_states = []
for i in range(36):
    list_of_states.append(featues[i]["properties"]["st_nm"])
    
list_of_states = np.asarray(list_of_states)

new_df = data.groupby(by='State').count().sort_values(by='Gender', ascending=False).reset_index()

def india_map():
    fig = px.choropleth_mapbox(data_frame=new_df,
                        geojson=geojson_India,
                        featureidkey='properties.st_nm',
                        locations='State',
                        color='Aadhaar generated',
                        color_continuous_scale = 'viridis',
                        mapbox_style="carto-positron",
                        center = {'lat':19.7515, 'lon':75.7139},
                        zoom=3,
                        opacity=1,
                       
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":50,"b":0},  title='Aadhaar Generated in each State.', template='plotly_dark')
    return fig

# india_map()

def hist():
    fig = px.histogram(data, x='Age')
    fig.update_layout(template='plotly_dark', hovermode='x')
    fig.update_traces(hoverlabel=dict(
        bgcolor='white',
        font_size=20,
        font_family='Arial'
    ), hovertemplate='%{y}')
    fig.update_xaxes(title='Age')
    fig.update_yaxes(title='Count')
    return fig

# hist()

registrar_df = data.groupby(by='Registrar').count().sort_values(by="Aadhaar generated", ascending=False).reset_index()

def registrar():
    fig = px.bar(data_frame=registrar_df, x=registrar_df['Registrar'][:20], y=registrar_df['Aadhaar generated'][:20])
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(title='Registrars in India.')
    fig.update_yaxes(title='Count')
    fig.update_traces(hovertemplate='%{y}', hoverlabel=dict(
        bgcolor='white',
        font_size=20,
        font_family='Arial',
    ))
    return fig

# registrar()

def district_wise(state):
    state_wise = data.groupby(by=['State', 'District']).count().sort_values(by='Aadhaar generated', ascending=False).reset_index()
    district_df = state_wise[state_wise['State']==state.capitalize()][:20]
    
    fig = px.bar(data_frame=district_df, x='District', y='Aadhaar generated', template='plotly_dark')
    fig.update_layout(title=f'Top 20 Districts in {state.capitalize()} with most Aadhaar Cards generated.')
    fig.update_traces(hovertemplate='%{y}', hoverlabel=dict(
    bgcolor='white',
    font_size=20,
    font_family='Arial',
))
    return fig


# district_wise("Maharashtra")

gender_state_df = data.groupby(by=['State', 'Gender']).count().sort_values(by='Aadhaar generated', ascending=False).reset_index()

def gender():
    fig = px.bar(gender_state_df, x='State', y='Aadhaar generated', facet_row='Gender')
    fig.update_layout(template='plotly_dark')
    fig.update_traces(hovertemplate='%{x}: %{y}', hoverlabel=dict(
        bgcolor='white',
        font_size=20,
        font_family='Arial',
    ))
    fig.update_yaxes(title='Aadhar Generated')
    return fig
# gender()

enrollment_state_df = data.groupby(by=['State', 'Enrolment Agency', 'District']).count().sort_values(by='Aadhaar generated', ascending=False).reset_index()

def enrollment_agencies(state, district):
    df1 = enrollment_state_df[(enrollment_state_df['State']==state) & (enrollment_state_df['District']==district)][:20]
    
    fig = px.bar(df1, x='Enrolment Agency', y='Aadhaar generated', template='plotly_dark')
    fig.update_layout(title='Top 10 Enrollment Agencies in the District of {district}')
    fig.update_traces(hovertemplate='%{y}', hoverlabel=dict(
    bgcolor='white',
    font_size=20,
    font_family='Arial',
))
    return fig

# enrollment_agencies("Maharashtra", 'Mumbai Suburban')




