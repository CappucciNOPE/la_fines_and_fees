import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output
import os, sys
import signal

#This is for the map - separate
from urllib.request import urlopen
import json

df = pd.read_csv('https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/main/final3.csv')
print(df.head())
working = df.copy()
totals = {}
tots = pd.DataFrame(df.groupby(['fips'],as_index = False,)['Total_Annual'].sum(),columns=['fips','Total_Annual'])
for i in range(0,len(tots)):
    totals[tots.at[i,'fips']] = tots.at[i,'Total_Annual']
print(totals)
#working = pd.DataFrame(working.groupby(['Parish','Flow'],as_index=False)['Total_Annual'].sum(), columns=['Parish','Flow','Total_Annual'])
#working.to_csv('/Users/mmontgomery/Documents/Louisiana Progress Fellowship/Crim Fines and Fees/bar_test.csv',index=False)
#df cols = ['Organizations', 'P1', 'P2', 'Total_Annual', 'Flow', 'Disbursement_Type', 'Parish']
'''not sure why this has to go at the top but okay'''
colors = {"dark_blue":"#053F5C", 'light_blue':'#9FE7F5',
'mid_blue':'#429EBD','orange':'#F27F0C','yellow':'#F7AD19'}

#Figure type: bar
parish_options = ['all','acadia','allen', 'ascension' ,'assumption', 'avoyelles', 'beauregard',
 'bienville' ,'bossier', 'caddo' ,'calcasieu' ,'caldwell' ,'cameron'
 'catahoula', 'claiborne', 'concordia' ,'desoto', 'eastbatonrouge',
 'eastcarroll', 'eastfeliciana' ,'evangeline', 'franklin', 'grant' ,'iberia',
 'iberville', 'jackson' ,'jefferson', 'jeffersondavis' ,'lafayette',
 'lafourche' ,'lasalle', 'lincoln', 'livingston', 'madison', 'morehouse',
 'natchitoches', 'ouachita', 'plaquemines', 'pointecoupee', 'rapides',
 'redriver' ,'richland' ,'sabine' ,'stbernard' ,'stcharles' ,'sthelena',
 'stjames' ,'stjohnthebaptist', 'stlandry' ,'stmartin' ,'stmary', 'sttammany',
 'tangipahoa', 'tensas' ,'terrebonne' ,'union' ,'vermillion', 'vernon',
 'washington', 'webster', 'westbatonrouge', 'westcarroll', 'westfeliciana',
 'winn']

fips_mapping= {'acadia': '22001', 'allen': '22003', 'ascension': '22005', 
'assumption': '22007', 'avoyelles': '22009', 'beauregard': '22011', 'bienville': '22013',
 'bossier': '22015', 'caddo': '22017', 'calcasieu': '22019', 'caldwell': '22021', 
 'cameron': '22023', 'catahoula': '22025', 'claiborne': '22027', 'concordia': '22029',
  'desoto': '22031', 'eastbatonrouge': '22033', 'eastcarroll': '22035', 'eastfeliciana': '22037',
   'evangeline': '22039', 'franklin': '22041', 'grant': '22043', 'iberia': '22045',
    'iberville': '22047', 'jackson': '22049', 'jefferson': '22051', 'jeffersondavis': '22053', 
    'lafayette': '22055', 'lafourche': '22057', 'lasalle': '22059', 'lincoln': '22061', 'livingston': '22063'
    , 'madison': '22065', 'morehouse': '22067', 'natchitoches': '22069', 'ouachita': '22073', 
    'plaquemines': '22075', 'pointecoupee': '22077', 'rapides': '22079', 'redriver': '22081',
     'richland': '22083', 'sabine': '22085', 'stbernard': '22087', 'stcharles': '22089',
      'sthelena': '22091', 'stjames': '22093', 'stjohnthebaptist': '22095', 'stlandry': '22097',
       'stmartin': '22099', 'stmary': '22101', 'sttammany': '22103', 'tangipahoa': '22105', 'tensas': '22107',
        'terrebonne': '22109', 'union': '22111', 'vermillion': '22113', 'vernon': '22115', 
        'washington': '22117', 'webster': '22119', 'westbatonrouge': '22121', 'westcarroll': '22123', 
        'westfeliciana': '22125', 'winn': '22127'}

parish_mapping = {'22001': 'acadia', '22003': 'allen', '22005': 'ascension', '22007': 'assumption', '22009': 'avoyelles', '22011': 'beauregard', '22013': 'bienville', '22015': 'bossier', '22017': 'caddo', '22019': 'calcasieu', '22021': 'caldwell', '22023': 'cameron', '22025': 'catahoula', '22027': 'claiborne', '22029': 'concordia', '22031': 'desoto', '22033': 'eastbatonrouge', '22035': 'eastcarroll', '22037': 'eastfeliciana', '22039': 'evangeline', '22041': 'franklin', '22043': 'grant', '22045': 'iberia', '22047': 'iberville', '22049': 'jackson', '22051': 'jefferson', '22053': 'jeffersondavis', '22055': 'lafayette', '22057': 'lafourche', '22059': 'lasalle', '22061': 'lincoln', '22063': 'livingston', '22065': 'madison', '22067': 'morehouse', '22069': 'natchitoches', '22073': 'ouachita', '22075': 'plaquemines', '22077': 'pointecoupee', '22079': 'rapides', '22081': 'redriver', '22083': 'richland', '22085': 'sabine', '22087': 'stbernard', '22089': 'stcharles', '22091': 'sthelena', '22093': 'stjames', '22095': 'stjohnthebaptist', '22097': 'stlandry', '22099': 'stmartin', '22101': 'stmary', '22103': 'sttammany', '22105': 'tangipahoa', '22107': 'tensas', '22109': 'terrebonne', '22111': 'union', '22113': 'vermillion', '22115': 'vernon', '22117': 'washington', '22119': 'webster', '22121': 'westbatonrouge', '22123': 'westcarroll', '22125': 'westfeliciana', '22127': 'winn'}
parishes = {'all':'all','acadia': 'Acadia Parish', 'allen': 'Allen Parish', 'ascension': 'Ascension Parish', 'assumption': 'Assumption Parish', 'avoyelles': 'Avoyelles Parish', 'beauregard': 'Beauregard Parish', 'bienville': 'Bienville Parish', 'bossier': 'Bossier Parish', 'caddo': 'Caddo Parish', 'calcasieu': 'Calcasieu Parish', 'caldwell': 'Caldwell Parish', 'cameron': 'Cameron Parish', 'catahoula': 'Catahoula Parish', 'claiborne': 'Claiborne Parish', 'concordia': 'Concordia Parish', 'desoto': 'De Soto Parish', 'eastbatonrouge': 'East Baton Rouge Parish', 'eastcarroll': 'East Carroll Parish', 'eastfeliciana': 'East Feliciana Parish', 'evangeline': 'Evangeline Parish', 'franklin': 'Franklin Parish', 'grant': 'Grant Parish', 'iberia': 'Iberia Parish', 'iberville': 'Iberville Parish', 'jackson': 'Jackson Parish', 'jefferson': 'Jefferson Parish', 'jeffersondavis': 'Jefferson Davis Parish', 'lafayette': 'Lafayette Parish', 'lafourche': 'Lafourche Parish', 'lasalle': 'LaSalle Parish[n]', 'lincoln': 'Lincoln Parish', 'livingston': 'Livingston Parish', 'madison': 'Madison Parish', 'morehouse': 'Morehouse Parish', 'natchitoches': 'Natchitoches Parish', 'ouachita': 'Ouachita Parish', 'plaquemines': 'Plaquemines Parish', 'pointecoupee': 'Pointe Coupee Parish', 'rapides': 'Rapides Parish', 'redriver': 'Red River Parish', 'richland': 'Richland Parish', 'sabine': 'Sabine Parish', 'stbernard': 'St. Bernard Parish', 'stcharles': 'St. Charles Parish', 'sthelena': 'St. Helena Parish', 'stjames': 'St. James Parish', 'stjohnthebaptist': 'St. John the Baptist Parish', 'stlandry': 'St. Landry Parish', 'stmartin': 'St. Martin Parish', 'stmary': 'St. Mary Parish', 'sttammany': 'St. Tammany Parish', 'tangipahoa': 'Tangipahoa Parish', 'tensas': 'Tensas Parish', 'terrebonne': 'Terrebonne Parish', 'union': 'Union Parish', 'vermillion': 'Vermilion Parish', 'vernon': 'Vernon Parish', 'washington': 'Washington Parish', 'webster': 'Webster Parish', 'westbatonrouge': 'West Baton Rouge Parish', 'westcarroll': 'West Carroll Parish', 'westfeliciana': 'West Feliciana Parish', 'winn': 'Winn Parish'}
app = Dash(__name__, use_pages=True,external_stylesheets=['https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/main/assets/app_style.css'])
server = app.server
app.layout = html.Div(style={'background':colors['dark_blue']},children=[
    dcc.Store(id='local'),
    html.H1(
        children='Tracking Money Across Louisiana\'s Criminal Justice System',
        style={'textAlign':'left',
        'color':colors['yellow']
        }
    ),
    html.Div([
            html.Button(dcc.Link(page['name']+"  |  ", href=page['path']))
            for page in dash.page_registry.values()]),
        dash.page_container       
])



'''To Crash when the the server won't stop'''
#os.kill(os.getpid(),signal.SIGTERM)
if __name__ =='__main__':
    app.run_server(debug=True)
    app.config.suppress_callback_exceptions = True