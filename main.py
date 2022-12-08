# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from utilities import shower, vis
import dash
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
# Bar Plot
import plotly.graph_objs as go
from numpy.core.fromnumeric import shape
from urllib.request import urlopen

#Reading data
url = 'https://storage.googleapis.com/fall2022_assignments/Point_in_Time_Estimates_of_Homelessness_in_the_US_by_State.csv'
#df = pd.read_csv('https://storage.googleapis.com/fall2022_assignments/Point_in_Time_Estimates_of_Homelessness_in_the_US_by_State.csv')
df = pd.read_csv(url)
df = shower.clean(df)

barchart = vis.bar_chart(df)
line_chart_1 = vis.line_chart1(df)
corr_plot = vis.corrplot(df)
pie_1 = vis.pie1(df)
pie_2 = vis.pie2(df)
scat_1 = vis.scat1(df)
scat_2 = vis.scat2(df)
scat_3 = vis.scat3(df)
choro = vis.chlor(df)

ratio_df = vis.get_ratio(df)

imf, matrix, statecodes = vis.implot(df,ratio_df)
sid_box = vis.sidbox(df)
stacked = vis.stackbar(df)
line2 = vis.line_2(df)
area_1 = vis.area1(df)
vio = vis.vio_plot(df)
sun = vis.sun_plot(df)
sun_1 = vis.sun_plot_1(df)

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Homelessness in the United States: 2007-2018", style = {'text-align': 'center'}),


    # dcc.Dropdown(id = "state_ranking",
    #              options=[
    #                  {"label": "Top 10 States", "value": "Top 10 States"},
    #                  {"label": "Least 10 States", "value": "Least 10 States"},
    #                  {"label": "Intermediate States", "value": "Intermediate States"}],
    #                  multi = False,
    #                  value = "Top 10 States",
    #                  style ={'width':"40%"}
    #             ),
    html.Div(id = 'output_container', children = []),
    html.Br(),

	html.Div(children='''
    Is the Trend of homeless people increasing or decreasing over the years?'''),
    dcc.Graph(
        id='bar-graph',
        figure=barchart
    ),
	html.Div(children='''
    We do observe that the overall number of homeless people has been decreasing over the years from the above plot'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	We see that the Overall homeless people have been decreasing over a period. Does it mean all the states had high no. of homeless people and has decreased over a period of time'''),
    dcc.Graph(
        id='pie-graph',
        figure=line_chart_1
    ),
	html.Div(children='''
    We do observe that the trends of statewise are very fluctuating and the Top 4 states such as 'CA','NY','FL','TX' have a huge number of homeless people compared to the other states
	'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What is the effect on homeless population with increasing years'''),
    dcc.Graph(
        id='corr-graph',
        figure=corr_plot
    ),
	html.Div(children='''
    With increasing year homeless individuals count is slightly decreasing i.e., there is a slight negative correlation between the two variables.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What is the ratio of chronically homeless individual’s distribution across regions in USA?'''),
    dcc.Graph(
        id='pie_1',
        figure=pie_1
    ),
	html.Div(children='''
    The western region is dominated by chronically homeless individuals with close to half the chronically homeless individual’s population residing there. Followed not so close by southeastern region while southwestern region being the lowest with midwestern region coming very close.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What is the ratio of chronically homeless individual’s distribution across state in USA?'''),
	dcc.Graph(
        id='pie_2',
        figure=pie_2
    ),
	html.Div(children='''
    CA from the western region contributes highly to the western region domination of chronically homeless individuals with majority of the overall chronically homeless individual’s population residing in CA. With a far margin of difference with CA, FL, TX, NY and the rest follow while states like SD, ND, GU, MP being very sparsely populated'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	How is chronically homelessness distributed across years?'''),
    dcc.Graph(
        id='scatter_1',
        figure=scat_1
    ),
	html.Div(children='''
     Unsheltered and sheltered chronically homeless people are highest in 2012 and 2011 respectively while chronically homeless individuals and in families are highest in 2007 and 2013 respectively.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	How is homelessness category distributed across years?'''),
	dcc.Graph(
        id='scatter_2',
        figure=scat_2
    ), 
	html.Div(children='''
    Overall homeless by default are highest. The highest are Sheltered homeless and homeless individuals.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	How is homelessness category distributed across years per region?'''),
	dcc.Graph(
        id='scatter_3',
        figure=scat_3
    ),
	html.Div(children='''
    Western region has most outliers and has a pattern of increase across years while Midwest is similarly distributed and reducing passing through years.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What are the top states with homeless count in each respective region?'''),
	dcc.Graph(
        id='chorofil',
        figure=choro
    ),
	html.Div(children='''
	We observe that the North-East regions has 'NY','MA' , West is being dominated by 'CA', South-East by 'FL','GA' , South-West by 'TX','AZ' and all the top 4 states have almost equal amount of proportions in the midwest'''),
 
#########
#begin J#
#########
	html.Div(style={'height': '200px'}),
	html.H2('Sheltering the Homeless: How successful has each state been?', style={'text-align': 'center'}),
	html.Div(
		'''The size of a homeless population in some state does not tell the whole story.
		It is important to look at the conditions of this population, not only its quantity.'''
	),
	html.Br(),
	html.Div([
		html.Div(
			dcc.Graph(id='pct_shelt'),
			style={'width': '1550px'}
		),
		html.Div(
			dcc.Slider(
				min=2007,
				max=2018,
				step=1,
				value=2007,
				marks={y: str(y) for y in range(2007,2019)},
				vertical=True,
				id='year_slider'
			)
		)],
		style={'display': 'flex', 'flex-direction': 'row'}
	),
	html.Br(),
	html.Div(
		'''There are a few notable periods of change across most states: 2009 and 2014 had a lot of 
		states with increased rates of sheltering compared to the previous year, 2010 and 2015 had quite 
		the opposite.'''
	),
	
	html.Div(style={'height': '100px'}),
	html.H2('Sheltering rates across the years: Viewed differently', style={'text-align': 'center'}),
	html.Div(
		'''This visualization allows us to see the sheltering rate changes across the years for 
		all states simultaneously.'''
	),
	html.Br(),
	dcc.Graph(
		id='imf_plot',
		figure=imf
	),
	html.Br(),
	html.Div(
		'''Note how some states maintain a high sheltering rate, some a low sheltering rate, and others vary. 
		In the next analysis we will attempt to see which states sheltering rate covary with each other.'''
	),
	html.Div(style={'height': '100px'}),
	html.H2('Which states\' sheltering rates correlate with each other?', style={'text-align': 'center'}),
	html.Div(
		'''It is expected that many states will correlate with each other in this regard. 
		Most states likely move with the national average, but it will be interesting to 
		see which ones, if any, have a tighter relationship.'''
	),
	html.Br(),
	html.Div([
		html.Div(
			dcc.Dropdown(
				options=df.region.unique(),
				value='west',
				id='reg_dropdown'
			)
		),
		html.Div(
			dcc.Graph(id='ratio_cor'),
			style={'width': '1000', 'height': '1000px'}
		)
		]
	),
	html.Br(),
	html.Div(
		'''It appears that the southeast and southwest regions are the regions with the highest interstate sheltering ratio correlations.'''
	),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What is the statistical distribution of homelessness category across region?'''),
	dcc.Graph(
        id='box_plot',
        figure=sid_box
    ),
	html.Div(children='''
    All the region distributions are extremely skewed with outliers while Midwest distributed is moderately skewed. '''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	Are all the Homeless types equally distributed over the years?'''),
	dcc.Graph(
			id='stacked_plot',
			figure=stacked  
	),
	html.Div(children='''
    We observe from the data that the number of Sheltered Homeless has the highest proportion of homeless people while 'Overall Homeless' and 'Sheltered Homeless' have an almost equal amount of proportion followed by 'Homeless_Individuals'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	What is the chronically homeless trend in western region?'''),
	dcc.Graph(
			id='line2_plot',
			figure=line2  
	),
	html.Div(children='''
    All the states in west follow a stable and slight increase except for CA which is varying across years but reaching its peak in 2017. '''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	 What is the chronically homeless trend in southwestern region?'''),
	dcc.Graph(
			id='area1_plot',
			figure=area_1  
	),
	html.Div(children='''
     All the states in west follow a similar trend varying across years but reaching its peak in 2011.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	'''),

	dcc.Graph(
			id='sun_plot',
			figure=sun  
	),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	 Are Homeless of certain states equally distributed?'''),
	dcc.Graph(
			id='vio_plot',
			figure=vio  
	),
	html.Div(children='''
    We analyze the distribution of homeless according to different states, years, and numbers. First, the range of overall unemployment in different states in the Southwest region is significantly different. Relatively speaking, the change range of the number of unemployed people in OK is the smallest, and the range of the number of unemployed people in TX is the largest.'''),
	html.Div(style={'height': '100px'}),
	html.Div(children='''
	'''),
	dcc.Graph(
			id='sun_plot1',
			figure=sun_1 
	),
	html.Div(style={'height': '100px'}),
	html.H2('In Conclusion:'),
	html.H3('''
	The homeless population is less related to the year, but more related to the region and state.
	The distribution of the type and proportion of the homeless population is relatively stable, and no major changes have been seen.
	There are obvious differences in the characteristics of the homeless population in different regions, with the largest homeless population in the west and the largest homeless population in CA.''')
])

#########
#begin J#
#########
@app.callback(
    Output('pct_shelt', 'figure'),
    Input('year_slider', 'value'))
def update_graph(year):
	year = int(year)        
	ydf = ratio_df.loc[(ratio_df.year == year) & (ratio_df.state_new == 'State')]   #current year 

	npd = 'No prior data'
	inc = 'Increased from prev. year'
	dec = 'Decreased from prev. year'
	
	if year == 2007:
		bar_color = np.repeat(npd, len(ydf)) 
	else:
		pdf = ratio_df.loc[(ratio_df.year == year-1) & (ratio_df.state_new == 'State')] #previous year
		increased = np.asarray(ydf.pct_sheltered) > np.asarray(pdf.pct_sheltered)
		bar_color = np.where(increased, inc, dec)

	ps_fig = px.bar(
		ydf,
		'state',
		'pct_sheltered',
		title='Percent of Homeless population that is Sheltered (by State)',
		color=bar_color,
		color_discrete_map={
			npd: 'grey',
			inc: 'darkolivegreen',
			dec: 'darkviolet'
		},
		range_y=[0,1]
	)

	ps_fig.update_layout(
		xaxis={'categoryorder': 'category ascending'},
		width=1500,
		height=500,
		title_x=0.5,
		margin={'autoexpand': False, 'r': 250}
	)
	return ps_fig

@app.callback(
    Output('ratio_cor', 'figure'),
    Input('reg_dropdown', 'value'))
def update_cor(reg):
	ratio_grp = ratio_df.groupby('state')
	region_order = np.asarray([ratio_grp.get_group(ST).region.iloc[0] for ST in statecodes])
	reg_mat = matrix[region_order == reg,:]
	reg_stt = statecodes[region_order == reg]
	#swapper = np.argsort(region_order)
	#newmat = matrix[swapper,:]
	#newstt = statecodes[swapper]

	corf = px.imshow(
		np.corrcoef(reg_mat),
		x=reg_stt,
		y=reg_stt,
		range_color=[-1,1],
		color_continuous_scale=px.colors.diverging.BrBG
	)
	corf.update_layout(
		title={'text': 'Sheltered Ratio Relationships between States'},
		title_x=0.5,
		width=900,
		height=900
	)

	corf.update_xaxes(dtick=1)
	corf.update_yaxes(dtick=1)
	return corf
		
#######
#end J#
#######


if __name__ == '__main__':
  app.run_server(debug = True, port = 8080)

