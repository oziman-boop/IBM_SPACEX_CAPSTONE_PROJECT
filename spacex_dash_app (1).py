# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                            value='ALL',
                                            placeholder = 'All Sites',
                                            searchable=True
                                            ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                            

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site): 
    filtered_df = spacex_df

    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Launch Sites Pie Chart')
        return fig
    else:
        for i in filtered_df.loc[:,'Launch Site'].value_counts().index:
            if entered_site == i:
                filtered_df = filtered_df[filtered_df.loc[:, 'Launch Site'] == i]

                filtered_df_pie = filtered_df['class'].value_counts()
                filtered_df_pie = pd.DataFrame(filtered_df_pie)
                filtered_df_pie.reset_index(inplace=True)

                fig = px.pie(filtered_df_pie, values='count', names='class', title='Pie Chart For '+i+' Launch Site')
                return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_dropdown_site, entered_slider_payload):
    filtered_df = spacex_df

    if entered_dropdown_site == 'ALL':
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] > entered_slider_payload[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] < entered_slider_payload[1]]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title = 'All Launch Sites - Success Scatter Plot With Booster Version Coloring')
        return fig
    
    else:
        for i in filtered_df.loc[:,'Launch Site'].value_counts().index:
            if entered_dropdown_site == i:
                filtered_df = filtered_df[filtered_df.loc[:, 'Launch Site'] == i]
                filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] > entered_slider_payload[0]]
                filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] < entered_slider_payload[1]]
                fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                                 color='Booster Version Category',
                                 title = entered_dropdown_site + ' - Success Scatter Plot With Booster Version Coloring')
                return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
