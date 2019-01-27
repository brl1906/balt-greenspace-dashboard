"""This module houses functions for parsing file objects from Plotly Dash
upload components, hanldes the files with data cleaning and preparation before
returning figure objects for charts in the app.  This module does the work
behind the file selection and uploading of a site userself.

author: Babila Lima
date: December 22, 2018
"""


import base64
import dash_html_components as html

import datetime as dt
import io
import numpy as np
import pandas as pd
import plotly.graph_objs as go


## functions for handling callbacks for dashboard row 1 charts
def parse_fundriaser_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def fundraise_piechart(dframe, target=15000):
        """
        Returns a plotly fig item for donut chart showing the percentages
        and dollar amounds raised by each member through their fundraising
        activities.
            """
        # find date of report run (usually appened to end of report in first column)
        for value in dframe['Contact Role']:
            try:
                if 'Generated' in value:
                    for segment in value.split():
                        if '/' in segment:
                            report_date = segment
            except:
                pass


        dframe = dframe[dframe['Amount'].notnull()]
        dframe['Donation Name'] = [name[0]+' '+name[1].replace('-','') for name in dframe['Donation Name'].str.split()]
        dframe['anonymized'] = ['id:'+str(np.round(np.random.rand(1),2)).\
        strip('[]').strip() for name in dframe['Last Name']]

        trace = []
        trace.append(go.Pie(
            values = dframe.groupby('Last Name')['Amount'].sum(),
            labels = dframe.groupby('Last Name')['Amount'].sum().index,
            domain = {'x': [0, .48]},
            name = 'pct raised',
            hoverinfo = 'percent+value',
            hole = .4,
            opacity = .8))

        layout = {
        "title": "Fundraising Outcomes {}<br><b>{}</b> members fundraised <b>{:,.1f}</b>% of target ".format(report_date,\
                                                      dframe.groupby('Last Name')['Amount'].sum().\
                                                       index.nunique(),(dframe['Amount'].sum() /\
                                                                        target) * 100),
        "titlefont": {'color':'#CCCCCC'},
        "showlegend":False,
        'paper_bgcolor':'#303939',
        'plot_bgcolor':'#303939',
        "annotations": [
            {
                "font": {"size": 20,
                        'color': '#CCCCCC'},
                "showarrow": False,
                "text": "BGS",
                "x": 0.20,
                "y": 0.5},
            {
                "font": {"size": 13,
                        'color':'#CCCCCC'},
                "showarrow": False,
                "text": "Target: $15k",
                "x": .75,
                "y": .88,
                'xref':'paper',
                'yref':'paper'
            },
            {
                "font": {"size": 13,
                        'color':'#CCCCCC'},
                "showarrow": False,
                "text": "Raised: ${:,.0f}".format(dframe['Amount'].sum()),
                "x": .75,
                "y": .83,
                'xref':'paper',
                'yref':'paper'},
            {
                "font": {"size": 13,
                        'color':'#CCCCCC'},
                "showarrow": False,
                "text": ('Shortfall: ${:,.0f}'.format(target - dframe['Amount'].sum())),
                "x": .75,
                "y": .78,
                'xref':'paper',
                'yref':'paper'}
        ]}

        fig = {'data':trace,'layout':layout}
        return fig


# try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = fundraise_piechart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig

# pldedges horizontal barchart
def parse_pledges_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def pledges_barchart(dframe, colors = ['#8dc16a','#d6746f']):
        """
        Returns a plotly fig item for donut chart showing the percentages
        and dollar amounds raised by each member through their fundraising
        activities.
        """
        # anonymize members & convert dollar values to float type
        anonymized = []
        for name in dframe['Last Name']:
            if str(name) == 'nan':
                anonymized.append('--')
            else:
                anonymized.append('M: {}'.format(np.random.randint(1,100)))

        dframe['anonymized'] = anonymized
        for col in ['Amount','Payment Amount Received','Remaining Balance']:
            dframe[col] = dframe[col].astype(float)

        # series of percentage donated against pledged
        pct_fulfiilled = pd.Series(dframe.groupby('Last Name')['Payment Amount Received'].sum() /
        dframe.groupby('Last Name')['Amount'].mean() * 100)

        # series of percentage donated against pledged
        # handle for negative values remaining for 'over achieving donors'
        normalized_balance_values = [0 if val < 0 else val for val in dframe.groupby('Last Name')['Remaining Balance'].sum() ]
        pct_outstanding =  (normalized_balance_values /
                            dframe.groupby('Last Name')['Amount'].mean() * 100)

        trace1 = go.Bar(
            x = pct_fulfiilled.values,
            y = pct_fulfiilled.index,
            name = 'received %',
            marker = {'color':'#8dc16a'},
            hoverinfo = 'x',
            opacity = .8,
            orientation = 'h'
                        )
        trace2 = go.Bar(
            x = pct_outstanding.values,
            y = pct_outstanding.index,
            name = 'outstanding %',
            hoverinfo = 'x',
            marker = {'color':'#d6746f'},
            opacity = .8,
            orientation = 'h'
                        )

        layout = go.Layout(
            legend = {'orientation': 'h'},
            xaxis = {'title': 'pct  %',
                        'titlefont': {'color':'#CCCCCC'},
                        'tickfont': {'color': '#CCCCCC'}},
            # hide y axis names by matching text color to background
            yaxis =  {'title': '',
                         'tickfont': {'color':'#303939'}},
            barmode =  'stack',
            hovermode = 'closest',
            title =  'Percent of Pledge Donated',
            titlefont =  {'color':'white'},
            paper_bgcolor =  '#303939',
            plot_bgcolor =  '#303939')

        traces = [trace1,trace2]
        fig = {'data':traces,'layout':layout}

        return fig

    # try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = pledges_barchart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig

# budget stacked barchart
def parse_budget_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def budget_barchart(dframe, colors=['#d6746f','green']):
        """
        Returns a plotly fig item for stacked barchart for budget vs actuals.
        """

        dframe = df.copy()
        dframe.columns = ['budget_item','actual','budgeted',
                        'over_budget','pct_overbudget']
        dframe.drop(dframe.index[0:5],inplace=True)
        for col in dframe.columns[1:]:
            dframe[col] = dframe[col].astype(float)
        dframe['budget_item'] = dframe['budget_item'].str.strip()

        # store report run date from last row in sheet to use in chart title
        report_run_date_list = dframe.iloc[-1][0].split()[1:4]
        run_date = report_run_date_list[0]+' '+report_run_date_list[1]+' '+report_run_date_list[2]

        # drop stamp from quickbooks in sheet
        for i in range(4):
            dframe.drop(dframe.index[-1],inplace=True)

        # create budget line item identifier to create filter -- isoloate key total lines
        budget_line_code = []
        for i,tag in enumerate(dframe.budget_item):
            if len(tag.split()) <= 1:
                budget_line_code.append('0000')
            elif tag.split()[0].isdigit():
                budget_line_code.append('00-' + str(tag.split()[0]))
            elif tag.split()[1].isdigit():
                budget_line_code.append(tag.split()[1])
            else:
                budget_line_code.append('0001')
        dframe['budget_code'] = budget_line_code


        # create plot trace & figure
        budgeted_xaxis,budgeted_yaxis,raised_xaxis,raised_yaxis = [],[],[],[]
        for item,tag in zip(['Grants','Support','Government'],
                            ['43300','43400','44500']):
            budgeted_xaxis.append(item)
            raised_xaxis.append(item)
            budgeted_yaxis.append(dframe[dframe.budget_code == tag].budgeted.sum()  - \
                 dframe[dframe.budget_code == tag].actual.sum())
            raised_yaxis.append(dframe[dframe.budget_code == tag].actual.sum())

        traces = []
        for stack,color,xaxis,yaxis in zip(['budget','actual'],colors,
                                     [budgeted_xaxis,raised_xaxis],
                                     [budgeted_yaxis,raised_yaxis]):
            traces.append(go.Bar(
                x = xaxis,
                y = yaxis,
                name = stack,
                marker = {'color': color},
                opacity = .7))

        data = traces
        layout = {
            'barmode':'stack',
            'hovermode':'closest',
            'title': 'Budget Target vs Actuals<br>{}'.format(run_date),
            'titlefont':{'color':'#CCCCCC'},
            'tickfont': {'color':'#CCCCCC'},
            'legend':{'font': {'color':'#CCCCCC'}},
            'yaxis':{'tickfont':{'color':'#CCCCCC'}},
            'xaxis':{'tickfont':{'color':'#CCCCCC'}},
            'paper_bgcolor': '#303939',
            'plot_bgcolor':'#303939',
             'annotations' : [
                 {'font':{'size':11,
                        'color': '#CCCCCC'},
                  'showarrow':False,
                  'x':.9,
                  'y': 1,
                  'xref':'paper',
                  'yref':'paper',
                  'text':'Target: ${:,.0f}'.\
                  format(dframe[dframe.budget_item=='Total Income'].budgeted.sum())
                 },
                 {'font':{'size':11,
                        'color':'#CCCCCC'},
                  'showarrow':False,
                  'x':.9,
                  'y': .93,
                  'xref':'paper',
                  'yref':'paper',
                  'text':'<b>Shortfall</b>: ${:,.0f}'.\
                  format(dframe[dframe.budget_item=='Total Income'].\
                         budgeted.sum() - dframe[dframe.budget_item=='Total Income'].\
                         actual.sum())}
             ]}
        fig = {'data':data, 'layout':layout}
        return fig

    # try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = budget_barchart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig

# grant outcomes barchart
def parse_grants_file_outcomes(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def grant_outcomes_barchart(dframe):
        """
        Returns a plotly fig item for stacked barchart displaying simplified
        status of grant funding application activity by quarter.
        """
        # prepare dataframe
        dframe = df.copy()
        dframe.columns = [col.lower().replace(' ','_') for col in dframe.columns]
        dframe = dframe[dframe['organization_name'].notnull()]
        dframe.drop(['thank_you_sent','report_due','report_sent'],axis=1,
                    inplace=True)
        dframe.set_index(dframe['date_application_sent'],inplace=True)

        grant_stage = []
        [grant_stage.append(status.lower().strip()) for status in dframe.stage]
        dframe['stage'] = grant_stage
        grant_status = [] # merge status to 3 primary categories, make 'awarded' tag
        for status in dframe.stage:
            if status not in ['obligations complete','pledged','posted']:
                grant_status.append(status)
            else:
                grant_status.append('awarded')
        dframe['grant_status'] = grant_status

        # create chart
        color_dict = {'awarded':'#adebad','not approved':'#d6746f',
                    'submitted':'#ffffb3'}
        grant_count_trace = []
        for status in dframe.grant_status.unique():
            grant_count_trace.append(go.Bar(
            x = dframe[dframe.grant_status==status].resample('Q')['stage'].count().index,
            y = dframe[dframe.grant_status==status].resample('Q')['stage'].count(),
            name = status,
            marker = {'color':color_dict[status]},
            opacity = .8))

        layout = {'barmode':'stack',
                 'hovermode':'closest',
                 'paper_bgcolor':'#303939',
                 'plot_bgcolor':'#303939',
                 'legend':{'font':{'color':'#CCCCCC'}},
                 'yaxis':{'title':'no. applications',
                        'tickfont':{'color':'#CCCCCC'},
                        'titlefont':{'color':'#CCCCCC'},
                         'showgrid':False},
                 'xaxis':{'title':'quarter submitted',
                        'titlefont':{'color':'#CCCCCC'},
                        'tickfont': {'color':'#CCCCCC'}},
                 'title':'Grant Application<br>Status Overview',
                 'titlefont':{'color':'#CCCCCC'}}

        fig  = {'data':grant_count_trace, 'layout':layout}
        return fig

# try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = grant_outcomes_barchart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig

# grant dollars barchart
def parse_grants_file_dollars(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def grant_dollars_barchart(dframe):
        """
        Returns a plotly fig item for stacked barchart displaying dollar amounts
        for grant application activity by quarter.
        """
        # prepare dataframe
        dframe = df.copy()
        dframe.columns = [col.lower().replace(' ','_') for col in dframe.columns]
        dframe = dframe[dframe['organization_name'].notnull()]
        dframe.drop(['thank_you_sent','report_due','report_sent'],axis=1,
                    inplace=True)
        dframe.set_index(dframe['date_application_sent'],inplace=True)

        # create chart
        color_dict = {'awarded':'#adebad','not approved':'#d6746f',
                    'submitted':'#ffffb3'}
        grant_stage = []
        [grant_stage.append(status.lower().strip()) for status in dframe.stage]
        dframe['stage'] = grant_stage
        grant_status = [] # merge status to 3 primary categories, make 'awarded' tag
        for status in dframe.stage:
            if status not in ['obligations complete','pledged','posted']:
                grant_status.append(status)
            else:
                grant_status.append('awarded')
        dframe['grant_status'] = grant_status

        # create chart
        grant_outcomes_trace = []
        for status in dframe.grant_status.unique():
            # sum 'amount' column totals for awarded grants
            if status == 'awarded':
                grant_outcomes_trace.append((go.Bar(
                x = dframe[dframe.grant_status==status].resample('Q')['amount'].count().index,
                y = dframe[dframe.grant_status==status].resample('Q')['amount'].sum(),
                name = status,
                marker = {'color': color_dict[status]},
                opacity = .8)))

            else:
            # sum 'requested amount' column totals for submitted and not approved
                grant_outcomes_trace.append((go.Bar(
                x = dframe[dframe.grant_status==status].resample('Q')['requested_amount'].count().index,
                y = dframe[dframe.grant_status==status].resample('Q')['requested_amount'].sum(),
                name = status,
                marker = {'color': color_dict[status]},
                opacity = .8)))

        layout = {'barmode':'stack',
                 'hovermode':'closest',
                 'legend': {'font': {'color': '#CCCCCC'}},
                 'paper_bgcolor': '#303939',
                 'plot_bgcolor': '#303939',
                  'yaxis':
                    {'title':'US$',
                    'tickfont':{'color':'#CCCCCC'},
                    'titlefont': {'color':'#CCCCCC'},
                    'showgrid':False},
                  'xaxis':{'title':'quarter submitted',
                        'titlefont': {'color':'#CCCCCC'},
                        'tickfont': {'color':'#CCCCCC'}},
                 'title':'Grant Application<br>Outcomes Overview',
                 'titlefont': {'color':'#CCCCCC'}}

        fig = {'data':grant_outcomes_trace,'layout':layout}
        return fig

# try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = grant_dollars_barchart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig

# strategic plan
def parse_strategic_plan_file(contents, filename):
    """Read in excel sheet, generate pandas dataframe and return bar chart.

    Function expects the sheet named 'All Items 7.17.17' to be the first
    sheet in the workbook as the cleaning process is set to the format and
    dimensions of that file.
    """
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    else:
        pass

    def strategic_plan_barchart(dframe, colors=['#f4aa42','#becca5','#9fa399',
                                '#d88668','#43a559','#edf760']):
        """
        Returns a plotly figure object for stacked bar chart showing progress
        on strategic plan items by quarter.
        """
        # prepare dataframe
        # check if user has changed number of columns in sheet
        if len(dframe.columns) != 11:
            issue = 'User has altered spreadsheet by {} {} columns.'
            if len(dframe.columns) < 11:
                action = 'removing'
                number = 11 - len(dframe.columns)
                print(issue.format(action,number))
            else:
                action = 'adding'
                number = len(dframe.columns) - 11
                print(issue.format(action,number))

        dframe.drop(dframe.index[0:6],inplace=True)
        new_cols = ['start_qt','start_yr','goal_id','topic_area','task_name',
                  'task_stage','blank1','start','finish','owner','internal_status']
        dframe.columns = new_cols
        dframe.drop('blank1',axis=1,inplace=True)
        dframe = dframe[dframe.task_stage.notnull()] # filter dataframe for items with a stage
        dframe['status'] = [x.lower().strip() for x in dframe.task_stage]
        dframe['start'] = [pd.to_datetime(date.split()[1]) for date in dframe.start]
        dframe['finish'].fillna(method='ffill',inplace=True)

        finish = []
        for date in dframe['finish']:
            if (type(date)) is str:
                finish.append(pd.to_datetime(date.split()[1]))
            else: finish.append(pd.to_datetime(date))
        dframe['finish'] = finish
        dframe['finish_qt'] = ['Q'+str(date.quarter) for date in dframe['finish']]
        YrQt_complete = ['{} Q{}'.format(date.year,date.quarter)  for date in dframe['finish']]
        dframe['YrQt_complete'] =  YrQt_complete

        # create chart
        if len(colors) != dframe['status'].nunique():
            colors = None

        trace = []
        clrs = dict(zip(sorted(dframe['status'].unique().tolist()),colors))
        for sts, clr in zip(sorted(dframe['status'].unique()),clrs.values()):
            trace.append(go.Bar(
            x = dframe[(dframe['task_stage']==sts)].groupby('YrQt_complete')['YrQt_complete'].count().index,
            y = dframe[(dframe['task_stage']==sts)].groupby('YrQt_complete')['YrQt_complete'].count(),
            name = sts,
            marker = {'color': clr},
            opacity = .8))

        layout = {
            'barmode':'stack',
            'legend': {'font':{'color':'#CCCCCC'}},
            'titlefont': {'color': '#CCCCCC'},
            'hovermode':'closest',
            'paper_bgcolor': '#303939',
            'plot_bgcolor': '#303939',
            'xaxis':{'title':'Target Completion Quarter',
                    'tickfont': {'color': '#CCCCCC'},
                    'titlefont': {'color': '#CCCCCC'}},
            'yaxis':{'title':'No. of Activities',
                    'tickfont': {'color': '#CCCCCC'},
                    'titlefont': {'color': '#CCCCCC'}},
            'title':'Strategic Plan Overview'}

        fig = {'data':trace,'layout':layout}
        return fig

# try except for filetype handling from upload
    try:
        if 'xls' in filename:
            # Expects excel file  uploaded
            df = pd.read_excel(io.BytesIO(decoded))
            fig = strategic_plan_barchart(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this Excel file.'
        ])

    return fig
