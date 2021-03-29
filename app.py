#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 20:46:21 2021

@author: dpong
"""

import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input


# Crucial function to convert (pivoted) dataframe into something Heatmap can consume
def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()
           }


codepen_playground = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=codepen_playground)
    

borough = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
           '$select=distinct boroname').replace(' ', '%20')
borough_name = pd.read_json(borough)

species = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
           '$select=distinct spc_common').replace(' ', '%20')
species_name = pd.read_json(species)
species_name = species_name.dropna(subset=['spc_common'])
species_name = species_name.reset_index(drop=True)


# tree2_url = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json?' \
#             '$select=health,spc_common,boroname,steward,count(tree_id)' \
#             '&$group=steward,health,boroname,spc_common'

app.layout = html.Div(children=[
    html.H1(children='NYC Tree Health Analytics', className="header-title"),
    html.P(
        children="Studying the health of various tree species across each borough of NY",
        className="header-description",
    ),

    dcc.Dropdown(
         id="borough",
         options=[{'label': i, 'value': i} for i in np.sort(borough_name.boroname.unique())],
         placeholder = 'Select A Borough', 
         value="Brooklyn",
         clearable=False,
         ),

    dcc.Dropdown(
         id="tree_type",
         options=[{'label': i, 'value': i} for i in np.sort(species_name.spc_common.unique())],
         placeholder = 'Select The type of the Tree', 
         value="Japanese maple",
         clearable=False,
         searchable=True,
         ),
    
    
    dcc.Graph(
        id = 'Trees_health'    
    ),
    
    dcc.Graph(
        id = 'Trees_Steward1'    
    ), 
    dcc.Graph(
        id = 'Trees_Steward2'    
    ),
       
    
     
   ])


# @app.callback(
#     dash.dependencies.Output('Trees_Steward', 'figure'),
#     [
#     dash.dependencies.Input('borough', 'value'), 
#     dash.dependencies.Input('tree_type', 'value')
#     ])

@app.callback(
    [Output('Trees_health', 'figure'), Output('Trees_Steward1', 'figure'), Output('Trees_Steward2', 'figure')],
    [
        Input("borough", "value"),
        Input("tree_type", "value")
    ]
    )


def update_charts(boroname, spc_common):
    
    tree1_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
                       '$select=boroname,spc_common,health,count(tree_id)' +\
                       '&$where=boroname=\'borough\'&spc_common=\'species\'' +\
                       '&$group=boroname,spc_common,health').\
                       replace('borough', boroname).replace('species', spc_common).replace(' ', '%20')

    tree1 = pd.read_json(tree1_url).dropna()
    


    tree2_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
                        '$select=boroname,spc_common,steward,health,count(health)' +\
                        '&$where=boroname=\'borough\'&spc_common=\'species\'' +\
                        '&$group=boroname,spc_common,steward,health').\
                        replace('borough', boroname).replace('species', spc_common).replace(' ', '%20') 
                
    tree2 = pd.read_json(tree2_url).dropna()

    tree2['steward_sorted'] = tree2['steward'].apply(lambda x: {'None':0, '1or2':1, '2or3':2, '3or4':3, '4orMore':4}[x])
    tree2.sort_values(by='steward_sorted', inplace = True)
    
    

    


# def update_figure(tree_type, borough):
    
    selected1 = tree1.loc[(tree1.spc_common == spc_common) & (tree1.boroname ==boroname)]
    
    # Pie Chart
    fig1 = px.pie(selected1, values='count_tree_id', names='health', title='Health Report of Trees by borough and tree species', \
                 labels = {'health':'Health Condition', 'count_tree_id':'Proportion of Trees'})
    fig1.update_traces(textposition='inside', textinfo='percent+label')

    selected = tree2.loc[(tree2.spc_common == spc_common) & (tree2.boroname ==boroname)]
    selected['prop'] = round(selected['count_health']*100/selected['count_health'].sum(), 2)
    
    # need to re-sort selected as it enters pivot
    df_selected_pivoted = selected.pivot(index = ['steward_sorted', 'steward'], columns='health', values='prop').sort_values(by='steward_sorted', ascending=True)

    df_selected_pivoted = df_selected_pivoted.reset_index().drop(('steward_sorted'), axis=1).set_index('steward')

    # heatmap 
    fig_hm = go.Figure(data = go.Heatmap(df_to_plotly(df_selected_pivoted), colorscale='rainbow', zmin=30.0, zmax=210.0))
                # labels=dict(x="steward", y="prop", color="health"),
                # x=['None', '1or2', '3or4', '4orMore']
                # y=['Morning', 'Afternoon', 'Evening']

    fig_hm.update_layout(title='Steward Impact on Species Health(Heatmap)')
    colors = {'background': '#111111','text': '#7FDBFF'}
    fig_hm.update_layout(title_x=0.5,plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])
    
    # bar chart 
    fig2_bar = px.bar(selected, x="steward", y="prop", color="health", barmode="stack",
                                  title='Steward Impact on Species Health(Bar Chart)',
                                  category_orders={"steward": ["None", "1or2","3or4","4orMore"],
                                                    "health": ["Good", "Fair", "Poor"]},
                                   labels={'prop':'%'}
                                  )
    
    colors = {'background': '#111111','text': '#7FDBFF'}
    fig2_bar.update_layout(title_x=0.5,plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])

    return fig1, fig_hm, fig2_bar


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True,threaded=True, port=3001)
