import base64
import datetime
import io
import warnings

import charts # custom module
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import pandas as pd
import plotly.graph_objs as go

warnings.filterwarnings('ignore')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})
server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.css.append_css({'external_url': external_stylesheets})
app.layout = html.Div([
    # page layout container
    html.Div([


    html.Div(
        [
            html.H1(
                'BGSview',
                className = 'twelve columns',
                style = {'text-align': 'left',
                        'color': '#A499AB',
                        'font-size':60}
                    ),
        ],
        className = 'row',
        style = {'margin-top':5}
            ),

        # upload & help text section
        html.Div([
            # upload component container
            html.Div([
                # row 1 upload components
                html.Div([
                    html.Div(
                        dcc.Upload(
                        id = 'fundraising-upload',
                        children = html.Div([
                            html.A('Fundraising File'),
                                            ]),
                                            className = 'four columns',
                                            style = {'border-color': 'grey',
                                                    'borderStyle': 'dashed',
                                                    'borderWidth': '1px',
                                                    'lineHeight': '60px',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin-left': '2px',
                                                    'margin-top': '4px',
                                                    'backgroundColor': '#44464A'}
                                            ),
                            ),
                    html.Div(
                        dcc.Upload(
                        id = 'pledges-upload',
                        children = html.Div([
                            html.A('Pledge File')
                                            ]),
                                            className = 'three columns',
                                            style = {'border-color': '#EFCCA3',
                                                    'borderStyle': 'dashed',
                                                    'borderWidth': '1px',
                                                    'lineHeight': '60px',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin-left': '2px',
                                                    'margin-top': '4px',
                                                    'backgroundColor': '#44464A'}
                                            ),
                            ),

                        ],
                        className = 'seven columns',
                        style = {'border-color':'blue'}
                        ),

                # row 2 component container
                html.Div([
                    html.Div(
                        dcc.Upload(
                        id = 'budget-upload',
                        children = html.Div([
                            html.A('Budget File')
                                            ]),
                                            className = 'four columns',
                                            style = {'border-color': 'grey',
                                                    'borderStyle': 'dashed',
                                                    'borderWidth': '1px',
                                                    'lineHeight': '60px',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin-left': '1px',
                                                    'margin-top': '4px',
                                                    'backgroundColor': '#44464A'}
                                            ),
                            ),
                    html.Div(
                        dcc.Upload(
                        id = 'grants-upload',
                        children = html.Div([
                            html.A('Grants File')
                                            ]),
                                            className = 'three columns',
                                            style = {'border-color': '#FF5733',
                                                    'borderStyle': 'dashed',
                                                    'borderWidth': '1px',
                                                    'lineHeight': '60px',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin-left': '1px',
                                                    'margin-top':'4px',
                                                    'backgroundColor': '#44464A'}
                                            ),
                            ),

                        ],
                        className = 'seven columns',
                        style = {'border-color':'blue'}
                        ),

                # row 3 component container
                html.Div([
                    html.Div(
                        dcc.Upload(
                        id = 'strategic-plan-upload',
                        children = html.Div([
                            html.A('Strategic Plan File')
                                            ]),
                                            className = 'six columns',
                                            style = {'border-color': '#CCCCCC',
                                                    'borderStyle': 'dashed',
                                                    'borderWidth': '1px',
                                                    'lineHeight': '60px',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin-left': '2px',
                                                    'margin-top': '4px',
                                                    'backgroundColor': '#44464A'}
                                            ),
                            ),
                        ],
                        className = 'seven columns',
                        style = {'border-color':'blue',
                                'margin-top':'3px',
                                'margin-left': '5px'}
                        ),

                    ],
                    className = 'row'
                    ),

            # help text container
            html.Div([
                html.H4("""Upload target Excel files to generate dashboard data and render
                 interactive charts for status on: fundraising, budget, pledges
                 and strategic plan. """)

                    ],
                    className = 'five columns',
                    style = {'color': 'grey'}
                    ),
                ],
                className = 'row'
                )
                    ]),

##**** charts section of website **** #####
    # Page Container Element
        html.Div([

# ***FIRST ROW OF CHARTS**
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id = 'piechart',

                        config = {
                            'displaylogo':False,
                            'showLink':False,
                            'displayModeBar': 'hover',
                            'modeBarButtons': [['zoom2d', 'lasso2d'],['toImage',
                                            'resetScale2d']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '10',
                        'border-style': 'dashed none none none',
                        'border-width': '2px',
                        'border-color': '#C0DAE9'}
                    ),

            html.Div(
                [
                    dcc.Graph(
                        id = 'pledge-bar',
                        config = {
                            'displaylogo':False,
                            'showLink':False,
                            'displayModeBar': 'hover',
                            'modeBarButtons': [['toImage']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '10',
                        'border-style': 'dashed none none none',
                        'border-width': '2px',
                        'border-color': '#B8E7A0'}
                    ),

            html.Div(
                [
                    dcc.Graph(
                        id = 'budget',

                        config = {
                            'displaylogo':False,
                            'showLink':False,
                            'displayModeBar': 'hover',
                            'modeBarButtons': [['zoom2d'],['toImage', 'resetScale2d']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '10'}
                    ),
        ],
        className = 'row',
        style = {'margin-left':'2',
                'margin-right': '2'}
            ),


# ***SECOND ROW OF CHARTS*** -- Completion Distrubution Frequency & Daily Heatmaps + Stacked Pct Chart
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id = 'grants-activity',
                        #figure = make_daily_count_close_heatmap(),
                        config = {
                            'displaylogo':False,
                            'showLink': False,
                            'modeBarButtons': [['zoom2d'],['toImage','resetScale2d']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '15',
                        'border-style': 'dashed none none none',
                        'border-width': '2px',
                        'border-color': '#FF5733'}
                    ),

            html.Div(
                [
                    dcc.Graph(
                        id = 'grants-dollars',
                        config = {
                            'displaylogo':False,
                            'showLink': False,
                            'modeBarButtons': [['zoom2d'],['toImage','resetScale2d']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '15',
                        'border-style': 'dashed none none none',
                        'border-width': '2px',
                        'border-color': '#FF5733'}
                    ),

            html.Div(
                [
                    dcc.Graph(
                        id = 'strategic-plan',
                        config = {
                            'displaylogo':False,
                            'showLink': False,
                            'modeBarButtons': [['zoom2d'],['toImage','resetScale2d']]
                                }
                            ),
                ],
                className = 'four columns',
                style = {'margin-top': '15',
                        'border-style': 'dashed none none none',
                        'border-width': '2px',
                        'border-color': '#CCCCCC'}
                    ),
        ],
        className = 'row',
            ),

                ],
            # set website background
            style = {'backgroundColor':'#303939'}
                )

        ],
        style = {'backgroundColor': '#303939'})





@app.callback(Output('piechart', 'figure'),
            [Input('fundraising-upload','contents'),
            Input('fundraising-upload', 'filename')])
def update_fundraising_output(content, name):
    return charts.parse_fundriaser_file(content, name)

@app.callback(Output('pledge-bar', 'figure'),
            [Input('pledges-upload','contents'),
            Input('pledges-upload', 'filename')])
def update_pledges_output(content, name):
    return charts.parse_pledges_file(content, name)

@app.callback(Output('budget', 'figure'),
            [Input('budget-upload','contents'),
            Input('budget-upload', 'filename')])
def update_budget_output(content, name):
    return charts.parse_budget_file(content, name)

@app.callback(Output('grants-activity', 'figure'),
            [Input('grants-upload','contents'),
            Input('grants-upload', 'filename')])
def update_grant_outcomes_output(content, name):
    return charts.parse_grants_file_outcomes(content, name)

@app.callback(Output('grants-dollars', 'figure'),
            [Input('grants-upload','contents'),
            Input('grants-upload', 'filename')])
def update_grant_dollars_output(content, name):
    return charts.parse_grants_file_dollars(content, name)

@app.callback(Output('strategic-plan', 'figure'),
            [Input('strategic-plan-upload','contents'),
            Input('strategic-plan-upload', 'filename')])
def update_grant_dollars_output(content, name):
    return charts.parse_strategic_plan_file(content, name)


if __name__ == '__main__':
    app.run_server(debug=True)
