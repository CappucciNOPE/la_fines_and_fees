import re
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import os, sys
import signal
import itertools

#This is for the map - separate
from urllib.request import urlopen
import json


#Data Loading
#df = pd.read_csv('https://github.com/CappucciNOPE/la_fines_and_fees/blob/e85e2a10df4a6cf62a8308088e9cc3707b0e0f34/final3.csv',index_col=False, usecols=['Organizations','Organization','Source','P2','P2','Total_Annual','Flow','Disbursement_Type','Parish','Type','Source_Type','Receiving','Year'])
df = pd.read_csv(r'https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/master/final3.csv',index_col=False, usecols=['Organizations','Organization','Source','P2','P2','Total_Annual','Flow','Disbursement_Type','Parish','Type','Source_Type','Receiving','Year'])

working = df.copy()
totals = {}
tots = pd.DataFrame(df.groupby(['Parish'],as_index = False,)['Total_Annual'].sum(),columns=['Parish','Total_Annual'])
for i in range(0,len(tots)):
    totals[tots.at[i,'Parish']] = tots.at[i,'Total_Annual']
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
app = Dash(__name__)
server = app.server
app.layout = html.Div(style={'background':colors['dark_blue']},children=[
    dcc.Store(id='local'),
    html.H1(
        children='Tracking Money Across Louisiana\'s Criminal Justice System',
        style={'textAlign':'left',
        'color':colors['yellow']
        }
    ),

    dcc.RadioItems(['Civil','Criminal','All'],'All',id='src',style={'color':colors['light_blue']}),
    html.H5(children='Select parishes to filter data or select all option to view data for all of Louisiana', style={'textAlign':'left','color':colors['light_blue']}),
    html.Div(children=[dcc.Dropdown(options=parishes,multi=True,value=['all'],id='parish_slct',style={'color':colors['dark_blue']})],hidden=False,id='check_hider'),
    html.H5(children='',style={'textAlign':'left','color':colors['yellow']},id='tracker'),

    dcc.Tabs(id='tabs',value='hist',children = [
            dcc.Tab(label='Flows',value='hist'),
            dcc.Tab(label='Explore by Parish',value='ice'),
            dcc.Tab(label='Map',value='map'),
    ]),
    html.Div(children=[dcc.Dropdown(options=['more','less','receipts','Disbursements to governments & nonprofits','Disbursements to individuals/3rd party collection or processing agencies','Amounts retained by collection agency'],value='more',id='flows'),
    dcc.RadioItems(['Percent','Total'],'Percent',id='quanti')],hidden=True,id='flow_hider',style={'color':colors['light_blue']}),
    dcc.Graph(id='content',figure={}),
])

#Filtering with tabs-------------------------------------------------------------------------
@app.callback(
    Output('tracker','children'),
    Output('local','data'),
    Output('content','figure'),
    Output('flow_hider','hidden'),
    Output('check_hider','hidden'),
    Input('parish_slct','value'),
    Input('tabs','value'),
    Input('flows','value'),
    Input('src','value'),
    Input('quanti','value')
)

def change_data(values1,tab,flow_switch,src,quanti):
    w = df.copy()
    if tab == 'map':
        f_hide = False
        c_hide = True
    else:
        f_hide = True
        c_hide = False
    if src != 'All':
        w = w.loc[w['Source']==src]
    if 'all' in values1:
        filtered = w.copy().to_dict(orient='tight')
        #print(filtered)
        fig = render_content(tab,filtered,flow_switch,quanti)
        return 'Data shown for all parishes',filtered,fig,f_hide,c_hide
    else:
        if src == 'All':
            w = w.loc[w["Parish"].isin(values1)]
            filtered = w.to_dict(orient='tight')
            #print(filtered)
            fig = render_content(tab,filtered,flow_switch,quanti)
            return 'Data shown for the following parishes: {}'.format(values1),filtered,fig,f_hide,c_hide
        else:
            w = w.loc[w["Parish"].isin(values1)]
            filtered = w.to_dict(orient='tight')
            #print(filtered)
            fig = render_content(tab,filtered,flow_switch,quanti)
            return 'Data shown for the following parishes: {}'.format(values1),filtered,fig,f_hide,c_hide

def render_content(tab,data,flow_switch,quanti):
    ret_graph = None
    w = pd.DataFrame.from_dict(data,orient='tight')
    if tab == 'hist':
        w = pd.DataFrame(w.groupby(['Parish','Flow','Disbursement_Type'],as_index = False)['Total_Annual'].sum(),columns=['Parish','Flow','Disbursement_Type','Total_Annual'])
        ret_graph = px.histogram(w,x='Parish',y="Total_Annual",color='Flow',barmode='group',
                    color_discrete_map={
                    "more": colors['light_blue'],
                    "less": colors['orange'],
                    "receipts": colors['yellow']},
                    height=800,width=1300)
        ret_graph.update_layout(
                    plot_bgcolor=colors['dark_blue'],
                    paper_bgcolor = colors['dark_blue'],
                    font_color = colors['light_blue']
                )

    elif tab == 'ice':
        ret_graph = px.treemap(w,path=['Parish','Flow','Disbursement_Type','Organizations'],values='Total_Annual',height=800,width=1400)

        ret_graph.update_layout(
            plot_bgcolor=colors['dark_blue'],
            paper_bgcolor = colors['dark_blue'],
            font_color = colors['light_blue'],
            uniformtext=dict(minsize=10, mode='hide')
        )

    elif tab == 'map':
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)
        w = w.copy()
        if quanti == 'Total':
            if flow_switch in ['more','less','receipts']:
                w = pd.DataFrame(w.groupby(['Parish','Flow'],as_index = False)['Total_Annual'].sum(),columns=['Parish','Flow','Total_Annual'])
                w = w.loc[w['Flow']==flow_switch]
                fips = []
                for parish in w['Parish']:
                    fips.append(fips_mapping[parish])
                w['fips'] = fips
                ret_graph = px.choropleth(w,geojson=counties,locations='fips',color_continuous_scale='Viridis',color='Total_Annual',scope='usa',height=1000,width=1400,range_color=(w['Total_Annual'].min(),w['Total_Annual'].max()))

            elif flow_switch in ['Disbursements to governments & nonprofits','Disbursements to individuals/3rd party collection or processing agencies','Amounts retained by collection agency']:
                w = pd.DataFrame(w.groupby(['Parish','Disbursement_Type'],as_index = False)['Total_Annual'].sum(),columns=['Parish','Disbursement_Type','Total_Annual'])
                w = w.loc[w['Disbursement_Type']==flow_switch]
                fips = []
                for parish in w['Parish']:
                    fips.append(str(fips_mapping[parish]))
                w['fips'] = fips
                ret_graph = px.choropleth(w,geojson=counties,locations='fips',color='Total_Annual',color_continuous_scale='Viridis',scope='usa',height=1000,width=1400,range_color=(w['Total_Annual'].min(),w['Total_Annual'].max()))
        elif quanti == 'Percent':
            if flow_switch in ['more','less','receipts']:
                w = pd.DataFrame(w.groupby(['Parish','Flow'],as_index = False)['Total_Annual'].sum(),columns=['Parish','Flow','Total_Annual'])
                w = w.loc[w['Flow']==flow_switch]
                fips = []
                for parish in w['Parish']:
                    fips.append(fips_mapping[parish])
                w['fips'] = fips
                percents = []
                i = 0
                for val in w['Total_Annual']:
                    par = list(w['Parish'])[i]
                    tot = totals[par]
                    percents.append(val/tot)
                    print(par,tot,val)
                    i+=1
                print(percents)
                w['pcnt'] = percents
                ret_graph = px.choropleth(w,geojson=counties,locations='fips',color_continuous_scale='Viridis',color='pcnt',scope='usa',height=1000,width=1400,range_color=(w['pcnt'].min(),w['pcnt'].max()))
            
            elif flow_switch in ['Disbursements to governments & nonprofits','Disbursements to individuals/3rd party collection or processing agencies','Amounts retained by collection agency']:
                w = pd.DataFrame(w.groupby(['Parish','Disbursement_Type'],as_index = False)['Total_Annual'].sum(),columns=['Parish','Disbursement_Type','Total_Annual'])
                w = w.loc[w['Disbursement_Type']==flow_switch]
                fips = []
                for parish in w['Parish']:
                    fips.append(str(fips_mapping[parish]))
                w['fips'] = fips
                percents = []
                i = 0
                for val in w['Total_Annual']:
                    par = list(w['Parish'])[i]
                    tot = totals[par]
                    percents.append(val/tot)
                    print(par,tot,val)
                    i+=1
                w['pcnt'] = percents
                print(percents)
                ret_graph = px.choropleth(w,geojson=counties,locations='fips',color='pcnt',color_continuous_scale='Viridis',scope='usa',height=1000,width=1400,range_color=(w['pcnt'].min(),w['pcnt'].max()))
    return ret_graph


'''To Crash when the the server won't stop'''
#os.kill(os.getpid(),signal.SIGTERM)
if __name__ =='__main__':
    app.run_server(debug=True)
