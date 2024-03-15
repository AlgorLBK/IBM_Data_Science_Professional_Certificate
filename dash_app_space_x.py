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
site = spacex_df['Launch Site'].unique()

# Callback for updating the pie chart based on dropdown selection
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_pie_chart(selected_site, payload_range):
    if selected_site == 'All Sites':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        title = f'Success vs Failed launches for all sites (Payload Range: {payload_range[0]} - {payload_range[1]} kg)'
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        title = f'Success vs Failed launches for {selected_site} (Payload Range: {payload_range[0]} - {payload_range[1]} kg)'
    
    fig = px.pie(filtered_df, names='class', title=title)
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All Sites':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        title = f'Payload Mass vs Class for all sites (Payload Range: {payload_range[0]} - {payload_range[1]} kg)'
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        title = f'Payload Mass vs Class for {selected_site} (Payload Range: {payload_range[0]} - {payload_range[1]} kg)'
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    return fig
# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown list for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': site_name, 'value': site_name} for site_name in ['All Sites'] + list(site)],
        value='All Sites',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),
    
    # Pie chart for successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # Slider for payload range selection
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        #marks={i: str(i) for i in range(0, max_payload + 1, 1000)},
        value=[min_payload, max_payload]
    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#1. Which site has the largest successful launches?
#CCAFS LC-40
#2. Which site has the highest launch success rate?
#CCAFS LC-40
#3. 

# Run the app
if __name__ == '__main__':
    app.run_server()
