import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output, callback
import os, sys
import signal
import itertools

df = pd.read_csv('https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/main/final3.csv')
parishes = {'all':'All','acadia': 'Acadia Parish', 'allen': 'Allen Parish', 'ascension': 'Ascension Parish', 'assumption': 'Assumption Parish', 'avoyelles': 'Avoyelles Parish', 'beauregard': 'Beauregard Parish', 'bienville': 'Bienville Parish', 'bossier': 'Bossier Parish', 'caddo': 'Caddo Parish', 'calcasieu': 'Calcasieu Parish', 'caldwell': 'Caldwell Parish', 'cameron': 'Cameron Parish', 'catahoula': 'Catahoula Parish', 'claiborne': 'Claiborne Parish', 'concordia': 'Concordia Parish', 'desoto': 'De Soto Parish', 'eastbatonrouge': 'East Baton Rouge Parish', 'eastcarroll': 'East Carroll Parish', 'eastfeliciana': 'East Feliciana Parish', 'evangeline': 'Evangeline Parish', 'franklin': 'Franklin Parish', 'grant': 'Grant Parish', 'iberia': 'Iberia Parish', 'iberville': 'Iberville Parish', 'jackson': 'Jackson Parish', 'jefferson': 'Jefferson Parish', 'jeffersondavis': 'Jefferson Davis Parish', 'lafayette': 'Lafayette Parish', 'lafourche': 'Lafourche Parish', 'lasalle': 'LaSalle Parish[n]', 'lincoln': 'Lincoln Parish', 'livingston': 'Livingston Parish', 'madison': 'Madison Parish', 'morehouse': 'Morehouse Parish', 'natchitoches': 'Natchitoches Parish', 'ouachita': 'Ouachita Parish', 'plaquemines': 'Plaquemines Parish', 'pointecoupee': 'Pointe Coupee Parish', 'rapides': 'Rapides Parish', 'redriver': 'Red River Parish', 'richland': 'Richland Parish', 'sabine': 'Sabine Parish', 'stbernard': 'St. Bernard Parish', 'stcharles': 'St. Charles Parish', 'sthelena': 'St. Helena Parish', 'stjames': 'St. James Parish', 'stjohnthebaptist': 'St. John the Baptist Parish', 'stlandry': 'St. Landry Parish', 'stmartin': 'St. Martin Parish', 'stmary': 'St. Mary Parish', 'sttammany': 'St. Tammany Parish', 'tangipahoa': 'Tangipahoa Parish', 'tensas': 'Tensas Parish', 'terrebonne': 'Terrebonne Parish', 'union': 'Union Parish', 'vermillion': 'Vermilion Parish', 'vernon': 'Vernon Parish', 'washington': 'Washington Parish', 'webster': 'Webster Parish', 'westbatonrouge': 'West Baton Rouge Parish', 'westcarroll': 'West Carroll Parish', 'westfeliciana': 'West Feliciana Parish', 'winn': 'Winn Parish'}

colors = {"dark_blue":"#053F5C", 'light_blue':'#9FE7F5',
'mid_blue':'#429EBD','orange':'#F27F0C','yellow':'#F7AD19'}
dash.register_page(__name__)

layout = html.Div([
    html.H2(id='title_ice',style={'textAlign':'center'}),
    
    html.P(children=['Select parishes to filter data or select all option to view data for all of Louisiana. Select \'Receiving\' to explore the composition of parties who receive criminal fines and fees by parish. Select \'Source\' to explore the source of the money disbursement.'],style={'textAlign':'left','color':colors['light_blue']}),

    html.Div(children=[
        dcc.RadioItems(options=['Receiving','Source'],value='Receiving',id='ordering'),
        dcc.Dropdown(options=parishes,multi=True,value=['ascension'],id='parish_slct'),
        
        
        dcc.Graph(id='content_ice',figure={})])
])
    
@callback(
    Output('content_ice','figure'),
    Output('title_ice','children'),
    Input('ordering','value'),
    Input('parish_slct',"value")
)

def ice_graph(order,sel_parish):
    ddf = df.copy()
    if sel_parish == 'all' or 'all' in sel_parish:
        ddf = ddf
    else:
        ddf = ddf.loc[ddf['Parish'].isin(sel_parish)]
    if order == "Receiving":
        ddf = ddf.loc[ddf["Flow"]=='less']
        ord = "Receiving Entities"
        ret_graph = px.treemap(ddf,path=['Parish','Disbursement_Type','Transaction'],values='Total_Annual',height=800,width=1340)
        ret_graph.update_layout(
            plot_bgcolor=colors['dark_blue'],
            paper_bgcolor = colors['dark_blue'],
            font_color = colors['light_blue'],
            uniformtext=dict(minsize=10, mode='hide')
        )
    elif order == "Source":
        ord = "Source Flows"
        ret_graph = px.treemap(ddf,path=['Parish','Flow','Source_Type','Transaction'],values='Total_Annual',height=800,width=1340)
        ret_graph.update_layout(
            plot_bgcolor=colors['dark_blue'],
            paper_bgcolor = colors['dark_blue'],
            font_color = colors['light_blue'],
            uniformtext=dict(minsize=10, mode='hide')
        )
    title = "Composition of {} by Parish".format(ord)
    return ret_graph,title