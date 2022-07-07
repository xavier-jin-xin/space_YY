# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print("min payload: ", min_payload)
#print("max payload: ", max_payload)

# Create a dash application
app = dash.Dash(__name__)
#print('Site :\n', spacex_df['Launch Site']) 
#print('label 2 :', spacex_df['Launch Site'][2]) 
ls = np.unique(spacex_df['Launch Site'])
#print('ls : \n', ls)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.P("Select a Launch Site :"),
                                dcc.Dropdown(id='site_dropdown',  options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': ls[0], 'value': ls[0]},
                                            {'label': ls[1], 'value': ls[1]},
                                            {'label': ls[2], 'value': ls[2]},
                                            {'label': ls[3], 'value': ls[3]}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.P("Success Pie Chart:"),
                                html.Div(dcc.Graph(id='success-pie-chart')),  # style={'display': 'flex'}),
                                html.Br(),



                                html.P("Payload Range (Kg) :"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0:'0', 2500:'2500',5000:'5000',
                                                      7500:'7500', 10000:'10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.P("Correlation between Payload and Launch success :"),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))

                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
### Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            [Input(component_id='site_dropdown', component_property='value'),
             Input(component_id='payload_slider', component_property='value')])
def get_pie_chart(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        # return the Total success launches in a pie chart for all sites
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
                                 &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        #str_range = [payload_slider[0], payload_slider[1]]
        #piechart = px.pie(data_frame = filtered_data, names='Payload Mass (kg) Site', values='class', title='Total Launches for All Sites')
        piechart = px.pie(data_frame = filtered_data, names='class', title='Globally success rate (listening to payload)')
        #print('site: ', site_dropdown)
        return piechart
    else:  #elif site_dropdown == ls[0]:
        # return the outcome piechart for a selected site
        filtered_df = spacex_df.loc[spacex_df['Launch Site']==site_dropdown]
        piechart = px.pie(data_frame = filtered_df, names='class',
                          title='For the launch site - ' + site_dropdown)
        ## piechart_values will be calculated automatically !
        #print('site: ', site_dropdown)
        return piechart


# Note: Don't Need this -- A callback function for `payload-slider` as inputs, `selected payload mass` as output ?
#@app.callback( Output('mass', 'children'),
#                Input('payload_slider', 'value'))
#def update_output(payload_slider):
#    return 'You have selected "{}"'.format(value)


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site_dropdown', component_property='value'),
               Input(component_id='payload_slider', component_property='value') ])
def get_scatter_chart(site_dropdown, payload_slider):
    ### Generally, return scatter plots with the x axis to be the payload and the y to be the launch outcome (i.e., class column)
    if site_dropdown == 'ALL':
        ## We render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
        ## In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
        
        #filtered_df = spacex_df    #.groupby('Launch Site').mean()
        #fig = px.scatter(y='class', x='Payload Mass (kg)')
        #print('scatter - site: ', site_dropdown)

        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
                                 &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class",
                                color="Booster Version Category")
        return scatterplot
    else:
        # We need to filter the spacex_df first, and render a scatter chart to show values Payload Mass (kg) and
        # class for the selected site, 
        # and color-label the point using Boosster Version Category likewise.
        
        #filtered_df = spacex_df.loc[spacex_df['Launch Site']==site_dropdown]
        #fig = px.scatter(y='class', x='Payload Mass (kg)')
        #print('scatter - site: ', site_dropdown)

        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])
                                   &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class",
                                color="Booster Version Category")
        return scatterplot


# Run the app
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False)


#### Finding Insights Visually -----
# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer questions:
# Which site has the largest successful launches?
# Which site has the highest launch success rate?
# Which payload range(s) has the highest launch success rate?
# Which payload range(s) has the lowest launch success rate?
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
