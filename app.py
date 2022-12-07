
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
# Bar Plot
import plotly.graph_objs as go

#barchart
url = 'https://storage.googleapis.com/fall2022_assignments/Point_in_Time_Estimates_of_Homelessness_in_the_US_by_State.csv'
#df = pd.read_csv('https://storage.googleapis.com/fall2022_assignments/Point_in_Time_Estimates_of_Homelessness_in_the_US_by_State.csv')
df = pd.read_csv(url)
print(df.head(4))
df2 = df[(df['count_type'] == 'Overall Homeless') & (df['state'] == 'Total')]
barchart =  px.bar(df2, x = 'year' , y = 'count' , title = 'Year wise count of Overall Homeless people in USA' , color='year')

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Web Application Dashboard with Dash", style = {'text-align': 'center'}),

    dcc.Dropdown(id = "state_ranking",
                 options=[
                     {"label": "Top 10 States", "value": "Top 10 States"},
                     {"label": "Least 10 States", "value": "Least 10 States"},
                     {"label": "Intermediate States", "value": "Intermediate States"}],
                     multi = False,
                     value = "Top 10 States",
                     style ={'width':"40%"}
                ),
    html.Div(id = 'output_container', children = []),
    html.Br(),

    dcc.Graph(
        id='example-graph',
        figure=barchart
    ),

])

if __name__ == '__main__':
  app.run_server(debug = True, port = 6080)
