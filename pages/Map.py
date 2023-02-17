import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output, callback
import os, sys
import signal
import itertools

#This is for the map - separate
from urllib.request import urlopen
import json

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

#Data Loading
#df = pd.read_csv('https://github.com/CappucciNOPE/la_fines_and_fees/blob/e85e2a10df4a6cf62a8308088e9cc3707b0e0f34/final3.csv',index_col=False, usecols=['Organizations','Organization','Source','P2','P2','Total_Annual','Flow','Disbursement_Type','Parish','Type','Source_Type','Receiving','Year'])
#df = pd.read_csv(r'https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/master/final3.csv',index_col=False, usecols=['Organizations','Organization','Source','P2','P2','Total_Annual','Flow','Disbursement_Type','Parish','Type','Source_Type','Receiving','Year'])
df = pd.read_csv('https://raw.githubusercontent.com/CappucciNOPE/la_fines_and_fees/main/final3.csv')
parishes = {'all':'All','acadia': 'Acadia Parish', 'allen': 'Allen Parish', 'ascension': 'Ascension Parish', 'assumption': 'Assumption Parish', 'avoyelles': 'Avoyelles Parish', 'beauregard': 'Beauregard Parish', 'bienville': 'Bienville Parish', 'bossier': 'Bossier Parish', 'caddo': 'Caddo Parish', 'calcasieu': 'Calcasieu Parish', 'caldwell': 'Caldwell Parish', 'cameron': 'Cameron Parish', 'catahoula': 'Catahoula Parish', 'claiborne': 'Claiborne Parish', 'concordia': 'Concordia Parish', 'desoto': 'De Soto Parish', 'eastbatonrouge': 'East Baton Rouge Parish', 'eastcarroll': 'East Carroll Parish', 'eastfeliciana': 'East Feliciana Parish', 'evangeline': 'Evangeline Parish', 'franklin': 'Franklin Parish', 'grant': 'Grant Parish', 'iberia': 'Iberia Parish', 'iberville': 'Iberville Parish', 'jackson': 'Jackson Parish', 'jefferson': 'Jefferson Parish', 'jeffersondavis': 'Jefferson Davis Parish', 'lafayette': 'Lafayette Parish', 'lafourche': 'Lafourche Parish', 'lasalle': 'LaSalle Parish[n]', 'lincoln': 'Lincoln Parish', 'livingston': 'Livingston Parish', 'madison': 'Madison Parish', 'morehouse': 'Morehouse Parish', 'natchitoches': 'Natchitoches Parish', 'ouachita': 'Ouachita Parish', 'plaquemines': 'Plaquemines Parish', 'pointecoupee': 'Pointe Coupee Parish', 'rapides': 'Rapides Parish', 'redriver': 'Red River Parish', 'richland': 'Richland Parish', 'sabine': 'Sabine Parish', 'stbernard': 'St. Bernard Parish', 'stcharles': 'St. Charles Parish', 'sthelena': 'St. Helena Parish', 'stjames': 'St. James Parish', 'stjohnthebaptist': 'St. John the Baptist Parish', 'stlandry': 'St. Landry Parish', 'stmartin': 'St. Martin Parish', 'stmary': 'St. Mary Parish', 'sttammany': 'St. Tammany Parish', 'tangipahoa': 'Tangipahoa Parish', 'tensas': 'Tensas Parish', 'terrebonne': 'Terrebonne Parish', 'union': 'Union Parish', 'vermillion': 'Vermilion Parish', 'vernon': 'Vernon Parish', 'washington': 'Washington Parish', 'webster': 'Webster Parish', 'westbatonrouge': 'West Baton Rouge Parish', 'westcarroll': 'West Carroll Parish', 'westfeliciana': 'West Feliciana Parish', 'winn': 'Winn Parish'}
colors = {"dark_blue":"#053F5C", 'light_blue':'#9FE7F5',
'mid_blue':'#429EBD','orange':'#F27F0C','yellow':'#F7AD19'}



more_dict = {22001: 1690734.0, 22003: 710383.0, 22005: 2614800.0, 22007: 1108838.0, 22009: 2146533.0, 22011: 1269209.0, 22013: 1385497.0, 22015: 10342436.0, 22017: 4553084.0, 22019: 6534652.0, 22021: 514495.0, 22023: 904299.0, 22025: 641136.0, 22027: 631975.0, 22029: 517245.0, 22031: 2380085.0, 22033: 37408369.0, 22035: 709662.0, 22037: 745352.0, 22039: 2830959.0, 22041: 816579.0, 22043: 336904.0, 22045: 2250559.0, 22047: 2673098.0, 22049: 418342.0, 22051: 7690377.08, 22053: 1269610.0, 22055: 16075931.0, 22057: 4037507.0, 22059: 570118.0, 22061: 2930615.0, 22063: 6786049.0, 22065: 1192837.0, 22067: 969387.0, 22069: 2102164.0, 22073: 7455775.0, 22075: 3276521.0, 22077: 811285.0, 22079: 1603752.0, 22081: 230790.0, 22083: 1499381.0, 22085: 715222.0, 22087: 1288864.56, 22089: 5820666.0, 22091: 81691.0, 22093: 913267.0, 22095: 4872637.0, 22097: 3346423.0, 22099: 2937756.0, 22101: 2112356.0, 22103: 18427339.0, 22105: 7835837.0, 22107: 301354.0, 22109: 3457482.0, 22111: 1069937.0, 22113: 1528214.0, 22115: 2923957.0, 22117: 2187173.0, 22119: 1471969.0, 22121: 1661718.0, 22123: 354243.0, 22125: 594398.0, 22127: 562753.0}
less_dict = {22001: 1681268.0, 22003: 701143.0, 22005: 2643885.0, 22007: 1053537.0, 22009: 2213165.0, 22011: 1961779.0, 22013: 1573909.921, 22015: 9620298.0, 22017: 4495872.415, 22019: 6584162.0, 22021: 469416.0, 22023: 764576.0, 22025: 686661.0, 22027: 745183.0, 22029: 504132.0, 22031: 2107260.167, 22033: 35751972.0, 22035: 709112.0, 22037: 843204.0, 22039: 2663748.0, 22041: 1140313.899, 22043: 945740.0, 22045: 2263894.0, 22047: 2936146.0, 22049: 407673.0, 22051: 13059450.53, 22053: 1550695.0, 22055: 15100273.0, 22057: 4038863.722, 22059: 584453.0, 22061: 2630309.0, 22063: 7322096.0, 22065: 1301931.0, 22067: 939141.0, 22069: 1976079.0, 22073: 6949082.0, 22075: 3178815.0, 22077: 784395.0, 22079: 2217170.0, 22081: 278989.0, 22083: 1659323.0, 22085: 680030.0, 22087: 993865.93, 22089: 4960228.722, 22091: 240564.0, 22093: 1059400.0, 22095: 4746983.0, 22097: 3217596.0, 22099: 2876761.0, 22101: 2003916.0, 22103: 17587770.0, 22105: 7644913.0, 22107: 291479.0, 22109: 3445455.0, 22111: 1115685.0, 22113: 1528210.0, 22115: 3111727.0, 22117: 2138728.0, 22119: 1462265.0, 22121: 1581787.0, 22123: 458681.0, 22125: 640922.0, 22127: 573671.0}
totals_dict={22001: 3372002.0, 22003: 1411526.0, 22005: 5258685.0, 22007: 2162375.0, 22009: 4370638.0, 22011: 3517548.0, 22013: 2967211.921, 22015: 20369700.0, 22017: 9078904.415, 22019: 13118814.0, 22021: 1012762.0, 22023: 1696743.0, 22025: 1327797.0, 22027: 1382534.0, 22029: 1021377.0, 22031: 4488745.167, 22033: 73698180.0, 22035: 1420982.0, 22037: 1588556.0, 22039: 5529396.0, 22041: 1956892.899, 22043: 1282644.0, 22045: 4688170.0, 22047: 5706086.0, 22049: 826701.0, 22051: 20749827.61, 22053: 2820305.0, 22055: 31260527.0, 22057: 8076370.722, 22059: 1154571.0, 22061: 5625480.0, 22063: 14834565.0, 22065: 2498134.0, 22067: 2053855.0, 22069: 4078243.0, 22073: 14404857.0, 22075: 6458141.0, 22077: 1595680.0, 22079: 3820922.0, 22081: 509779.0, 22083: 3177211.0, 22085: 1404569.0, 22087: 2282730.49, 22089: 11421855.722, 22091: 322255.0, 22093: 2007716.0, 22095: 9758605.0, 22097: 7410057.0, 22099: 5966855.0, 22101: 4116272.0, 22103: 36632781.0, 22105: 16363213.0, 22107: 592833.0, 22109: 6902937.0, 22111: 2234399.0, 22113: 3056424.0, 22115: 6326863.0, 22117: 4325901.0, 22119: 2944807.0, 22121: 3243505.0, 22123: 812924.0, 22125: 1235320.0, 22127: 1136424.0}
dtcoll_dict = {22001: 373434.0, 22003: 158483.0, 22005: 889237.0, 22007: 182052.0, 22009: 184526.0, 22011: 301494.0, 22013: 217300.921, 22015: 1205223.0, 22017: 1229421.415, 22019: 1471502.0, 22021: 0.0, 22023: 18146.0, 22025: 0, 22027: 191738.0, 22029: 26319.0, 22031: 311171.167, 22033: 6413571.0, 22035: 86313.0, 22037: 133208.0, 22039: 1009488.0, 22041: 184332.0, 22043: 241002.0, 22045: 297021.0, 22047: 378245.0, 22049: 98588.0, 22051: 6873035.9399999995, 22053: 189370.0, 22055: 2181946.0, 22057: 825014.722, 22059: 3600.0, 22061: 269759.0, 22063: 1245546.0, 22065: 191680.0, 22067: 145479.0, 22069: 200037.0, 22073: 1513275.0, 22075: 426677.0, 22077: 74332.0, 22079: 842574.0, 22081: 43503.0, 22083: 258769.0, 22085: 19724.0, 22087: 264963.64, 22089: 626597.0, 22091: 119931.0, 22093: 175360.0, 22095: 958447.0, 22097: 846078.0, 22099: 305424.0, 22101: 283624.0, 22103: 2337442.0, 22105: 415497.0, 22107: 44342.0, 22109: 34233.0, 22111: 166065.0, 22113: 961223.0, 22115: 909022.0, 22117: 273473.0, 22119: 315608.0, 22121: 285281.0, 22123: 63069.0, 22125: 65157.0, 22127: 105861.0}
dti3p_dict = {22001: 319233.0, 22003: 191783.0, 22005: 92694.0, 22007: 235976.0, 22009: 893839.0, 22011: 586483.0, 22013: 214543.0, 22015: 6059617.0, 22017: 427046.0, 22019: 2650538.0, 22021: 236103.0, 22023: 14435.0, 22025: 250874.0, 22027: 129485.0, 22029: 1016.0, 22031: 659960.0, 22033: 22714685.0, 22035: 55808.0, 22037: 374577.0, 22039: 312182.0, 22041: 477872.0, 22043: 135248.0, 22045: 746234.0, 22047: 1777700.0, 22049: 65059.0, 22051: 0.0, 22053: 690320.0, 22055: 9939420.0, 22057: 1634870.0, 22059: 49030.0, 22061: 955503.0, 22063: 5168279.0, 22065: 220269.0, 22067: 399313.0, 22069: 274650.0, 22073: 2106085.0, 22075: 2027300.0, 22077: 130507.0, 22079: 121939.0, 22081: 5702.0, 22083: 387862.0, 22085: 292081.0, 22087: 0, 22089: 1990122.0, 22091: 86043.0, 22093: 389228.0, 22095: 429932.0, 22097: 881610.0, 22099: 1005194.0, 22101: 621758.0, 22103: 12228595.0, 22105: 2772931.0, 22107: 31229.0, 22109: 438526.0, 22111: 483704.0, 22113: 0, 22115: 279625.0, 22117: 955592.0, 22119: 487120.0, 22121: 612322.0, 22123: 128508.0, 22125: 185087.0, 22127: 166652.0}
dtgnp_dict={22001: 988601.0, 22003: 350877.0, 22005: 1661954.0, 22007: 635509.0, 22009: 1134800.0, 22011: 1073802.0, 22013: 1142066.0, 22015: 2355458.0, 22017: 2839405.0, 22019: 2462122.0, 22021: 233313.0, 22023: 731995.0, 22025: 435787.0, 22027: 423960.0, 22029: 476797.0, 22031: 1136129.0, 22033: 6623716.0, 22035: 566991.0, 22037: 335419.0, 22039: 1342078.0, 22041: 478109.89900000003, 22043: 569490.0, 22045: 1220639.0, 22047: 780201.0, 22049: 244026.0, 22051: 6186414.59, 22053: 671005.0, 22055: 2978907.0, 22057: 1578979.0, 22059: 531823.0, 22061: 1405047.0, 22063: 908271.0, 22065: 889982.0, 22067: 394349.0, 22069: 1501392.0, 22073: 3329722.0, 22075: 724838.0, 22077: 579556.0, 22079: 1252657.0, 22081: 229784.0, 22083: 1012692.0, 22085: 368225.0, 22087: 728902.29, 22089: 2343509.722, 22091: 34590.0, 22093: 494812.0, 22095: 3358604.0, 22097: 1489908.0, 22099: 1566143.0, 22101: 1098534.0, 22103: 3021733.0, 22105: 4456485.0, 22107: 215908.0, 22109: 2972696.0, 22111: 465916.0, 22113: 566987.0, 22115: 1923080.0, 22117: 909663.0, 22119: 659537.0, 22121: 684184.0, 22123: 267104.0, 22125: 390678.0, 22127: 301158.0}
dash.register_page(__name__)

layout = html.Div([
    html.H2(id='title_map',style={'textAlign':'center'},children=['Mapping Louisiana\'s Fines and Fees']),
    
    html.H5(style={'textAlign':'center','color':colors['light_blue']}),

    html.Div(children=[
        '1. Select the field that you would like search for plot values within',
        dcc.Dropdown(options=['Total_Annual','Flow','Source_Type','Receiving_Type'],value='Total_Annual',id='broad cat',disabled=False,style={'color':"#053F5C"}),
        '2. Select the value that you would like to plot (Disabled for Total Annual)',
        dcc.Dropdown(multi=False,id='sel_val',disabled=False,style={'color':"#053F5C"}),
        '3. Select measurement',
        dcc.Dropdown(options=['Percent','Total'],value='Percent',id='meas',style={'color':"#053F5C"}),
        '3b. If you selected \'Percent\', select the value for which you would like the value to be expressed as a percentage of (Disabled for Total Annual).',
        dcc.Dropdown(options={'more':'Incoming Flows','less':'Disbursements','all':'All','gnp':'Disbursements to governments & nonprofits','i3p':'Disbursements to individuals/3rd party collection or processing agencies','coll':'Amounts retained by collection agency',"None":"None"},value='all',id='whole',disabled=False,style={'color':"#053F5C"}),

        
        dcc.Graph(id='content_map',figure={}),
        dcc.Graph(id='map_hist',figure={})])
    ])

#Getting the secondary dropdown options
@callback(
    Output('sel_val','options'),
    Output('sel_val','value'),
    Output('sel_val','disabled'),
    Input('broad cat','value')
)

def ctrl_sel_val(bval):
    if bval == 'Total_Annual':
        return(['Total_Annual'],'Total_Annual',True)
    else:
        options = list(pd.unique(df[bval]))
        return(options,options[0],False)

@callback(
    Output('meas','options'),
    Output('meas','value'),
    Output('meas','disabled'),
    Input('sel_val','value')
)

def ctrl_sel_value(sval):
    if sval == 'Total_Annual':
        return(['Total','Percent'],'Total',True)
    else:

        return(['Total','Percent'],'Percent',False)

@callback(
    Output('whole','value'),
    Output('whole','options'),
    Output('whole','disabled'),
    Input('meas','value')
)

def determine_whole(units):
    if units=='NA':
        return('NA',['NA'],True)
    else:
        return('all',{'more':'Incoming Flows','less':'Disbursements','all':'Total','gnp':'Disbursements to governments & nonprofits','i3p':'Disbursements to individuals/3rd party collection or processing agencies','coll':'Amounts retained by collecting agency',"None":"None"},False)

@callback(
    Output('content_map','figure'),
    Output('map_hist','figure'),
    Input('meas','value'),
    Input('whole','value'),
    Input('sel_val','value'),
    Input('broad cat','value')
)
def map_make(quanti,whole,flow_switch,big_meas):
    print(quanti,whole,flow_switch,big_meas)
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
        w = df.copy()
        if big_meas == "Total_Annual":
            w = pd.DataFrame(w.groupby(['fips','Parish'],as_index=False)['Total_Annual'].sum(),columns=['fips','Total_Annual','Parish'])
            print(w)
            ret_graph = px.choropleth(w,geojson=counties,locations='fips',color_continuous_scale='Viridis',color='Total_Annual',scope='usa',height=500,width=1340,range_color=(w['Total_Annual'].min(),w['Total_Annual'].max()))
            ret_hist = px.histogram(w,x='Parish',y="Total_Annual",barmode='group',height=500,width=1340)
            return ret_graph,ret_hist
        if quanti == 'Total':
            w = pd.DataFrame(w.groupby(['fips',big_meas,'Parish'],as_index = False)['Total_Annual'].sum(),columns=['fips',big_meas,'Parish','Total_Annual'])
            w = w.loc[w[big_meas]==flow_switch]
            (print(w))
            ret_graph = px.choropleth(w,geojson=counties,locations='fips',color_continuous_scale='Viridis',color='Total_Annual',scope='usa',height=500,width=1340,range_color=(w['Total_Annual'].min(),w['Total_Annual'].max()))
            ret_hist = px.histogram(w,x='Parish',y="Total_Annual",barmode='group',height=500,width=1340)
            return ret_graph,ret_hist
        elif quanti == 'Percent':
            w = pd.DataFrame(w.groupby(['fips',big_meas,'Parish'],as_index = False)['Total_Annual'].sum(),columns=['fips',big_meas,'Parish','Total_Annual'])
            w = w.loc[w[big_meas]==flow_switch]

            if whole == 'more':
                totals = more_dict
            if whole == 'less':
                totals = less_dict
            if whole == 'all':
                totals = totals_dict
            if whole == 'i3p':
                totals = dti3p_dict
            if whole == 'gnp':
                totals = dtgnp_dict
            if whole == 'coll':
                totals = dtcoll_dict

            i = 0
            percents = []
            for val in w['Total_Annual']:
                par = list(w['fips'])[i]
                tot = totals[par]
                percents.append(val/tot)
                print(par,tot,val)
                i+=1
                print(percents)
            w['pcnt'] = percents
            print(w)
            ret_graph = px.choropleth(w,geojson=counties,locations='fips',color_continuous_scale='Viridis',color='pcnt',scope='usa',height=500,width=1400,range_color=(w['pcnt'].min(),w['pcnt'].max()))
            ret_hist = px.histogram(w,x='Parish',y="pcnt",barmode='group',height=800,width=1340)

            return ret_graph,ret_hist

