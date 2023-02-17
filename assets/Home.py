import re
import plotly.express as px
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output, callback
import os, sys
import signal
import itertools
import matplotlib as plt

df = pd.read_csv('/Users/mmontgomery/fines_and_fees/final3.csv')
dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2("Dissecting the User Pay Criminal Justice System"),

    html.H3("The Problem"),
    
    html.P(children=['''Louisiana is the state with the highest incarceration rate, in the country with the highest incarceration rate.
    Relying on fines and fees to fund the justice system creates conflicts of interest that disproportionately affect black and brown communities.
    Law enforcement and courts are incentivized to create new fines and fees, because they receive funding from these criminal activities.
    The greatest burden of these fines and fees falls on the people who can least afford them--often low-income Louisianans, and communities of color.
    These system trap people with debt and criminalization when they cannot afford to pay. Because penalized individuals cannot always afford to pay,
    fines and fees are also a volatile source of funding for law enforcement agencies that need steady income to protect and serve their communities.''']),

    html.H3("Legal Action: 2019"),
    html.P(children=['''In 2019, Act 87 required all public and private organizations that received and disbursed fines and fees collected through the criminal justice system 
    report these fines and fees in Schedule 87 of their annual financial report. These reports were made publicly available through the Louisiana Legislative Auditor. These reports 
    provide snapshot images of the working of Louisiana's user-pay criminal justice system.''']),
    html.P(children=['''The data of 63 parishes are represented out of Louisiana 64 parishes. This is due to the Caliste v Cantrell case of 2019, in which the standard practice of allowing the New Orleans
    magistrate judge to both generate and administer court fees, to be a conflict of interest. In reality, this practice extends across Louisiana criminal justice system. Sheriffs offices arrest individuals, 
    who the Courts can prosecute for fines and fees moneys to continue funding the criminal justice system.''']),

    
    html.H3("Our Contribution"),
    html.P(children=['''This data on this website comes from the most recent financial reports of 63 sheriff parishes in Louisiana as of January 2023. 
    Sheriff parish reports were chosen because all transactions for each parish go through the parish sheriff. 
    By placing the information in these reports in one location at your fingertips, we have tried to build the bigger picture of Louisiana's criminal justice system funding from the parish-level snapshots.
    Louisiana Progress hopes to allow citizens to explore the sources and destinations of this money.''']),

    html.H3('How to Use this Tool'),
    html.P(children=['''Use the links at the top of the page to navigate across the Explorer, Map, and Histogram tools. The Explorer shows the Source Type composition of the funds collected and disbursed by the sheriffs office, 
    as well as the composition of the organizations to which funds were disbursed. The Map plots types of disbursements across the state of Louisiana either by the sum for each parish or as a percentage of a selection of the funds reported in Schedule 87 for that parish.
    Finally, the Histogram tool plots these sum total of the values across Louisiana or individually, with the option to compare them. (For some fields plotted, the range of values to show is too great, making it hard to represent multiple parishes on the same axis.) ''']),

    html.H3('Methodology'),
    html.P(children=['''The parish sheriff Schedule 87 Collecting/Receiving Entity, Disbursing Entity, and Receipts were compiled into a single csv (available for download below). 
    The following fields are taken directly from Scehdule 87 reports: 'Parish,' 'Transaction,' 'P1,' 'P2,' 'Flow,', and 'Disbursement Type.' Transaction refers to the flow of money into or out of the parish sheriff office copied verbatim from its listing in the report. 
    P1 and P2 refer to six-moth fiscal periods. (For this web app, I have summed P1 and P2 fields into a single 'Total_Annual' field that is used across the web app; however, these fields exist as legacy in the csv.)
    The 'Flow' field refers to whether the transaction is the flow of fines and fees into or out of the sheriff accounts; 'more' indicates incoming funds, 'less' indicates disbursements,
    while 'receipts' indicates funds coming from jurisdiction external to the parish sheriff (district, municipal, state, or federal). Disbursement_Type only applies to transactions for which the Flow field is 'less' --  that is, the parish sheriff is disbursing money to governmental or private organizations.
    The 'fips' field is inferred from the 'Parish' field and is used for mapping purposes. The 'Source Type,' 'Organization,' and 'Receiving Type' fields are inferred from the 'Transaction' field.
    The 'Source Type' refers to the type of funds involved in transaction--for example, funds from bond fees, civil fees, or criminal fines. The 'Organization' refers to the exact department, organization, or agency that receives these funds.
    The 'Receiving Type' field is the broad category in which the 'Organization' falls. Note that funds may be received or disbursed to municipalities within the parish as well.
    ''']),
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv")

])

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "all_fines_and_fees.csv") 
