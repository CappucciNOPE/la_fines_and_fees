import re
import plotly.express as px
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output, callback
import os, sys
import signal
import itertools

df = pd.read_csv('/Users/mmontgomery/fines_and_fees/final3.csv')
parishes1 = {'all':'All','acadia': 'Acadia Parish', 'allen': 'Allen Parish', 'ascension': 'Ascension Parish', 'assumption': 'Assumption Parish', 'avoyelles': 'Avoyelles Parish', 'beauregard': 'Beauregard Parish', 'bienville': 'Bienville Parish', 'bossier': 'Bossier Parish', 'caddo': 'Caddo Parish', 'calcasieu': 'Calcasieu Parish', 'caldwell': 'Caldwell Parish', 'cameron': 'Cameron Parish', 'catahoula': 'Catahoula Parish', 'claiborne': 'Claiborne Parish', 'concordia': 'Concordia Parish', 'desoto': 'De Soto Parish', 'eastbatonrouge': 'East Baton Rouge Parish', 'eastcarroll': 'East Carroll Parish', 'eastfeliciana': 'East Feliciana Parish', 'evangeline': 'Evangeline Parish', 'franklin': 'Franklin Parish', 'grant': 'Grant Parish', 'iberia': 'Iberia Parish', 'iberville': 'Iberville Parish', 'jackson': 'Jackson Parish', 'jefferson': 'Jefferson Parish', 'jeffersondavis': 'Jefferson Davis Parish', 'lafayette': 'Lafayette Parish', 'lafourche': 'Lafourche Parish', 'lasalle': 'LaSalle Parish[n]', 'lincoln': 'Lincoln Parish', 'livingston': 'Livingston Parish', 'madison': 'Madison Parish', 'morehouse': 'Morehouse Parish', 'natchitoches': 'Natchitoches Parish', 'ouachita': 'Ouachita Parish', 'plaquemines': 'Plaquemines Parish', 'pointecoupee': 'Pointe Coupee Parish', 'rapides': 'Rapides Parish', 'redriver': 'Red River Parish', 'richland': 'Richland Parish', 'sabine': 'Sabine Parish', 'stbernard': 'St. Bernard Parish', 'stcharles': 'St. Charles Parish', 'sthelena': 'St. Helena Parish', 'stjames': 'St. James Parish', 'stjohnthebaptist': 'St. John the Baptist Parish', 'stlandry': 'St. Landry Parish', 'stmartin': 'St. Martin Parish', 'stmary': 'St. Mary Parish', 'sttammany': 'St. Tammany Parish', 'tangipahoa': 'Tangipahoa Parish', 'tensas': 'Tensas Parish', 'terrebonne': 'Terrebonne Parish', 'union': 'Union Parish', 'vermillion': 'Vermilion Parish', 'vernon': 'Vernon Parish', 'washington': 'Washington Parish', 'webster': 'Webster Parish', 'westbatonrouge': 'West Baton Rouge Parish', 'westcarroll': 'West Carroll Parish', 'westfeliciana': 'West Feliciana Parish', 'winn': 'Winn Parish'}
parishes2 = {'acadia': 'Acadia Parish', 'allen': 'Allen Parish', 'ascension': 'Ascension Parish', 'assumption': 'Assumption Parish', 'avoyelles': 'Avoyelles Parish', 'beauregard': 'Beauregard Parish', 'bienville': 'Bienville Parish', 'bossier': 'Bossier Parish', 'caddo': 'Caddo Parish', 'calcasieu': 'Calcasieu Parish', 'caldwell': 'Caldwell Parish', 'cameron': 'Cameron Parish', 'catahoula': 'Catahoula Parish', 'claiborne': 'Claiborne Parish', 'concordia': 'Concordia Parish', 'desoto': 'De Soto Parish', 'eastbatonrouge': 'East Baton Rouge Parish', 'eastcarroll': 'East Carroll Parish', 'eastfeliciana': 'East Feliciana Parish', 'evangeline': 'Evangeline Parish', 'franklin': 'Franklin Parish', 'grant': 'Grant Parish', 'iberia': 'Iberia Parish', 'iberville': 'Iberville Parish', 'jackson': 'Jackson Parish', 'jefferson': 'Jefferson Parish', 'jeffersondavis': 'Jefferson Davis Parish', 'lafayette': 'Lafayette Parish', 'lafourche': 'Lafourche Parish', 'lasalle': 'LaSalle Parish[n]', 'lincoln': 'Lincoln Parish', 'livingston': 'Livingston Parish', 'madison': 'Madison Parish', 'morehouse': 'Morehouse Parish', 'natchitoches': 'Natchitoches Parish', 'ouachita': 'Ouachita Parish', 'plaquemines': 'Plaquemines Parish', 'pointecoupee': 'Pointe Coupee Parish', 'rapides': 'Rapides Parish', 'redriver': 'Red River Parish', 'richland': 'Richland Parish', 'sabine': 'Sabine Parish', 'stbernard': 'St. Bernard Parish', 'stcharles': 'St. Charles Parish', 'sthelena': 'St. Helena Parish', 'stjames': 'St. James Parish', 'stjohnthebaptist': 'St. John the Baptist Parish', 'stlandry': 'St. Landry Parish', 'stmartin': 'St. Martin Parish', 'stmary': 'St. Mary Parish', 'sttammany': 'St. Tammany Parish', 'tangipahoa': 'Tangipahoa Parish', 'tensas': 'Tensas Parish', 'terrebonne': 'Terrebonne Parish', 'union': 'Union Parish', 'vermillion': 'Vermilion Parish', 'vernon': 'Vernon Parish', 'washington': 'Washington Parish', 'webster': 'Webster Parish', 'westbatonrouge': 'West Baton Rouge Parish', 'westcarroll': 'West Carroll Parish', 'westfeliciana': 'West Feliciana Parish', 'winn': 'Winn Parish'}
drop2_opts = ['Transaction', 'Source_Type', 'Flow', 'Disbursement_Type', 'Receiving_Type']
colors = {"dark_blue":"#053F5C", 'light_blue':'#9FE7F5',
'mid_blue':'#429EBD','orange':'#F27F0C','yellow':'#F7AD19'}
dash.register_page(__name__)

layout = html.Div([
    html.H2(id='title_hist',style={'textAlign':'center'}),
    
    html.H5(children=['Select parishes to filter data or select all option to view data for all of Louisiana'],style={'textAlign':'center','color':colors['light_blue']}),

    
    dcc.Dropdown(options=parishes1,multi=True,value=['all'],id='parish_slct'),
    dcc.Dropdown(options=drop2_opts,value='Disbursement_Type',id='dyn_in'),
        
    dcc.Graph(id='content_hist',figure={})
])
    


@callback(
    Output('content_hist','figure'),
    Output('title_hist','children'),
    Output('parish_slct','multi'),
    Output('parish_slct','options'),
    Output('parish_slct',"value"),
    Input('dyn_in','value'),
    Input('parish_slct',"value")
)

def change_data(filter_val,parish):
    if type(parish) == str:
        parish = [parish]
    
    if filter_val in ['Receiving_Type','Source_Type','Transaction']:
        mult = False
        parish_opt = parishes2
        if parish == ['all'] or 'all' in parish:
            parish = ['acadia']
        else:
            parish = [parish[0]]
    else:
        mult = True
        parish_opt = parishes1
        parish = parish
    

    ddf =df.copy()
    if (parish == "all") or ("all" in parish):
        ddf = pd.DataFrame(ddf.groupby(['Parish',filter_val],as_index=False)['Total_Annual'].sum())
        
    else:
        ddf = pd.DataFrame(ddf.groupby(by = ['Parish',filter_val],as_index=False)['Total_Annual'].sum())
        ddf = ddf.loc[ddf["Parish"].isin(parish)]
    print (ddf)
    ret_graph = px.histogram(ddf,x='Parish',y="Total_Annual",barmode='group',height=800,width=1340,color=filter_val)
    ret_graph.update_layout(legend=dict(orientation='h',yanchor='bottom',y=-0.3))
    title = "{} for All Transactions by Parish in Louisiana".format(filter_val)
    if len(parish) == 1:
        return ret_graph,title,mult,parish_opt,parish[0]
    else:
        return ret_graph,title,mult,parish_opt,parish