# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from utilities import shower
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

print(df.head(4))
df2 = df[(df['homelessness'] == 'Overall Homeless') & (df['state'] == 'Total')]
barchart =  px.bar(df2, x = 'year' , y = 'number' , title = 'Year wise count of Overall Homeless people in USA' , color='year')
#print(df.head(4))
df2 = df[(df['homelessness'] == 'Overall Homeless') & (df['state'] == 'Total')]
barchart =  px.bar(df2, x = 'year' , y = 'number' , title = 'Year wise count of Overall Homeless people in USA' , color='year')
df3 = df[(df['state'] != 'Total')]
df3 = df3.groupby(['state','year'])['number'].sum().reset_index()
#df4 = df3.groupby('state')['number'].sum().reset_index()
line_chart_1 = px.line(df3, x = 'year', y = 'number',color='state', title= 'Year on Year Homeless Trend statewise') 
#text_auto = 'True'
corr_plot = px.imshow(df.corr(), zmin=-1, zmax=1, color_continuous_scale='rdbu')
df_1 = df[(df['homelessness'] == 'Chronically Homeless Individuals' ) & (df['state'] != 'Total')]
df_1 = df_1.groupby(['year','state','region'])['number'].sum().reset_index()

pie_1= px.pie(
	data_frame=df_1,
	names='region',
	values='number',
	color='region',
	title='Region wise Chronically Homeless Individuals',
	template=None,
	width=None,
	height=None,
	opacity=None,
	hole=0.8
) 

pie_2= px.pie(
	data_frame=df_1,
	names='state',
	values='number',
	color='region',
	title='State wise Chronically Homeless Individuals',
	color_discrete_sequence=px.colors.sequential.RdBu,
	template=None,
	width=1000,
	height=1000,
	opacity=None,
	hole=0.3
) 
df_2 = df[(df['homelessness'] == 'Chronically Homeless People in Families')|(df['homelessness'] =='Unsheltered Chronically Homeless' )|(df['homelessness'] =='Sheltered Total Chronically Homeless') | (df['homelessness'] == 'Chronically Homeless Individuals') & (df['region'] != 'Total')]
scat_1 = px.scatter(df_2, x="homelessness", y="number", title="Scatterplot of Chronically homeless population",color="year",
                 size='number' )
scat_2 = px.scatter(df, x="year", y="number", title="Scatterplot of homeless population through years",color="homelessness",
                 size='number' )
scat_3 = px.scatter(df_1, x="year", y="number", color="region", facet_row=None, facet_col="region")

overall=df[(df.homelessness=='Sheltered ES Homeless') & ((df.state!='Total') & (df.state != 'CA') & (df.state != 'NY') & (df.state != 'MA') & (df.state != 'PA'))]
overall=overall.sort_values(by = 'year', ascending = True) 
choro = px.choropleth(overall, locations='state',
                    locationmode="USA-states", color='number', animation_frame="year", scope="usa", color_continuous_scale="oranges", title= 'Animated Choropleth Map')

###
#J#
###
shel = 'Sheltered Total Homeless'
totl = 'Overall Homeless'

def minidf(df, count_type):
	temp_df = df.loc[df.homelessness == count_type] 
	return temp_df.drop(labels='homelessness', axis=1).rename({'number': count_type}, axis=1)

ratio_df = pd.merge(
	minidf(df, shel),
	minidf(df, totl),
	on=['year', 'state', 'state_new', 'region']
)

# Ratio DF building complete
ratio_df.insert(len(ratio_df.columns), 'pct_sheltered', ratio_df.apply(lambda x: x[shel] / x[totl], axis=1))

# Turn to np for better vis of timelines use in px.imshow
statecodes = df.loc[df.state_new == 'State'].state.unique()
matrix = np.array([ratio_df.loc[ratio_df.state == ST].sort_values(by='year').pct_sheltered.to_numpy() for ST in statecodes])
imf = px.imshow(
	np.transpose(matrix),
	y=np.linspace(2007,2018,12),
	x=statecodes,
	range_color=[0,1],
	origin='lower',
	labels={
		'x': 'State',
		'y': 'Year'
	}
)

imf.update_layout(title={'text': 'Sheltered Ratio'}, title_x = 0.5)
imf.update_xaxes(dtick=1)
imf.update_yaxes(dtick=1)
#imf.update_layout(title_text='Sheltered Ratio', ###title_x=0.5, title_font_color="green",)

# Make corr
ratio_grp = ratio_df.groupby('state')
region_order = np.asarray([ratio_grp.get_group(ST).region.iloc[0] for ST in statecodes])
swapper = np.argsort(region_order)
newmat = matrix[swapper,:]
newstt = statecodes[swapper]

corf = px.imshow(
	np.corrcoef(newmat),
	x=newstt,
	y=newstt,
	range_color=[-1,1],
	color_continuous_scale=px.colors.diverging.BrBG
)
corf.update_layout(
	title={'text': 'Sheltered Ratio Relationships between States'},
	width=900,
	height=900
)
corf.update_xaxes(dtick=1)
corf.update_yaxes(dtick=1)
###
#J#
###

sid_box = px.box(df_1, x="region", y="number", title = "Boxplot analyis in each region with the count")
sid_box.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="green"
)

#stacked - bar
chronically_homeless = ['Chronically Homeless','Chronically Homeless Individuals','Chronically Homeless People in Families']
Overall_homeless = ['Overall Homeless']
Homeless_individuals = ['Homeless Children of Parenting Youth',
'Homeless Family Households',
'Homeless Individuals',
'Homeless Parenting Youth (Under 25)',
'Homeless Parenting Youth Age 18-24',
'Homeless Parenting Youth Under 18',
'Homeless People in Families',
'Homeless Unaccompanied Youth (Under 25)',
'Homeless Unaccompanied Youth Age 18-24',
'Homeless Unaccompanied Youth Under 18',
'Homeless Veterans']

Sheltered_Chronically_homeless = ['Sheltered ES Chronically Homeless',
'Sheltered ES Chronically Homeless Individuals',
'Sheltered ES Chronically Homeless People in Families']

Sheltered_homeless = ['Sheltered ES Homeless',
'Sheltered ES Homeless Children of Parenting Youth',
'Sheltered ES Homeless Family Households',
'Sheltered ES Homeless Individuals',
'Sheltered ES Homeless Parenting Youth (Under 25)',
'Sheltered ES Homeless Parenting Youth Age 18-24',
'Sheltered ES Homeless Parenting Youth Under 18',
'Sheltered ES Homeless People in Families',
'Sheltered ES Homeless Unaccompanied Youth (Under 25)',
'Sheltered ES Homeless Unaccompanied Youth Age 18-24',
'Sheltered ES Homeless Unaccompanied Youth Under 18',
'Sheltered ES Homeless Veterans',
'Sheltered SH Chronically Homeless',
'Sheltered SH Chronically Homeless Individuals',
'Sheltered SH Homeless',
'Sheltered SH Homeless Individuals',
'Sheltered SH Homeless Unaccompanied Youth (Under 25)',
'Sheltered SH Homeless Unaccompanied Youth Age 18-24',
'Sheltered SH Homeless Unaccompanied Youth Under 18',
'Sheltered SH Homeless Veterans',
'Sheltered TH Homeless',
'Sheltered TH Homeless Children of Parenting Youth',
'Sheltered TH Homeless Family Households',
'Sheltered TH Homeless Individuals',
'Sheltered TH Homeless Parenting Youth (Under 25)',
'Sheltered TH Homeless Parenting Youth Age 18-24',
'Sheltered TH Homeless Parenting Youth Under 18',
'Sheltered TH Homeless People in Families',
'Sheltered TH Homeless Unaccompanied Youth (Under 25)',
'Sheltered TH Homeless Unaccompanied Youth Age 18-24',
'Sheltered TH Homeless Unaccompanied Youth Under 18',
'Sheltered TH Homeless Veterans',
'Sheltered Total Chronically Homeless',
'Sheltered Total Chronically Homeless Individuals',
'Sheltered Total Chronically Homeless People in Families',
'Sheltered Total Homeless',
'Sheltered Total Homeless Children of Parenting Youth',
'Sheltered Total Homeless Family Households',
'Sheltered Total Homeless Individuals',
'Sheltered Total Homeless Parenting Youth (Under 25)',
'Sheltered Total Homeless Parenting Youth Age 18-24',
'Sheltered Total Homeless Parenting Youth Under 18',
'Sheltered Total Homeless People in Families',
'Sheltered Total Homeless Unaccompanied Youth (Under 25)',
'Sheltered Total Homeless Unaccompanied Youth Age 18-24',
'Sheltered Total Homeless Unaccompanied Youth Under 18',
'Sheltered Total Homeless Veterans']

Unsheltered_homeless = ['Unsheltered Homeless',
'Unsheltered Homeless Children of Parenting Youth',
'Unsheltered Homeless Family Households',
'Unsheltered Homeless Individuals',
'Unsheltered Homeless Parenting Youth (Under 25)',
'Unsheltered Homeless Parenting Youth Age 18-24',
'Unsheltered Homeless Parenting Youth Under 18',
'Unsheltered Homeless People in Families',
'Unsheltered Homeless Unaccompanied Youth (Under 25)',
'Unsheltered Homeless Unaccompanied Youth Age 18-24',
'Unsheltered Homeless Unaccompanied Youth Under 18',
'Unsheltered Homeless Veterans'
]

unsheltered_chronically_homeless = ['Unsheltered Chronically Homeless',
'Unsheltered Chronically Homeless Individuals',
'Unsheltered Chronically Homeless People in Families']

df.loc[df['homelessness'].isin(chronically_homeless) , 'homeless_type'] = 'chronically_homeless'
df.loc[df['homelessness'].isin(Homeless_individuals) , 'homeless_type'] = 'Homeless_individuals'
df.loc[df['homelessness'].isin(Unsheltered_homeless) , 'homeless_type'] = 'Unsheltered_homeless'
df.loc[df['homelessness'].isin(unsheltered_chronically_homeless) , 'homeless_type'] = 'Unsheltered_chronically_homeless'
df.loc[df['homelessness'].isin(Sheltered_Chronically_homeless) , 'homeless_type'] = 'Sheltered_Chronically_homeless'
df.loc[df['homelessness'].isin(Sheltered_homeless) , 'homeless_type'] = 'Sheltered_homeless'
df.loc[df['homelessness'].isin(Overall_homeless) , 'homeless_type'] = 'Overall_homeless'

# df.head(2)
df8 = df.groupby(['year','homeless_type'])['number'].sum().reset_index()
# df8.head(10)

# stacked = df8[(df8['state'] == 'Total')]
stacked =  px.bar(
	df8,
	x = 'year' ,
	y = 'number' ,
	title = 'Year on Year Proportions of Homeless Type' ,
	color='homeless_type',
	pattern_shape_sequence=[".", "x", "+"],
	pattern_shape='homeless_type'
)
stacked.update_layout(title_text='year on Year Proportions of Homeless Type', title_x=0.5, title_font_color="magenta")


df_3 = df[(df['region'] == 'west')  & ((df['homelessness'] == 'Chronically Homeless People in Families')|(df['homelessness'] =='Unsheltered Chronically Homeless' ) |
(df['homelessness'] =='Sheltered Total Chronically Homeless') | (df['homelessness'] == 'Chronically Homeless Individuals'))  ]
df_3 = df_3.groupby(['year','state'])['number'].sum().reset_index()
line2 = px.line(df_3, x="year", y="number",color='state',title='Chronical Homelessness trend spawning over years in west region of USA')
df_4 = df[(df['region'] == 'southwest')  & ((df['homelessness'] == 'Chronically Homeless People in Families')|(df['homelessness'] =='Unsheltered Chronically Homeless' ) |

          (df['homelessness'] =='Sheltered Total Chronically Homeless') | (df['homelessness'] == 'Chronically Homeless Individuals'))  ]

df_4 = df_4.groupby(['year','state'])['number'].sum().reset_index()

area_1=px.area(df_4, x="year", y="number", color="state", line_group="state")

title='Chronical Homelessness trend spawning over years in southwest region of USA'
area_1.update_layout(title_text='Chronical Homelessness trend spawning over years in southwest region of USA', title_x=0.5, title_font_color="blue",)
#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
vio=px.violin(df_4, x="state", y="number",title='Statistical attributes of Southwest region states ', color='state')
df7 = df[df['state']!= 'Total']
sun = px.sunburst(df7, path=['region', 'state'], values='number', height=600, title='State wise homeless population distribution')

df_2 = df[
	(
		(df['homelessness'] == 'Chronically Homeless People in Families') |
		(df['homelessness'] =='Unsheltered Chronically Homeless' ) |
		(df['homelessness'] =='Sheltered Total Chronically Homeless') | 
		(df['homelessness'] == 'Chronically Homeless Individuals')
	) &
	(
		df['region'] != 'Total'
	)
]

sun_1 = px.sunburst(
	df_2,
	values='number',
	path=['region','homelessness'],
	ids=None,
	color=None,
	color_continuous_scale=None,
	range_color=None,
	color_continuous_midpoint=None,
	color_discrete_sequence=None,
	color_discrete_map=None,
	hover_name=None,
	hover_data=None,
	custom_data=None,
	labels=None,
	title='Chronical data distribution data in various regions',
	template=None,
	width=None,
	height=750,
	branchvalues=None,
	maxdepth=None
)

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Dashboard for Homeless people in United States of America (USA)", style = {'text-align': 'center'}),


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

    dcc.Graph(
        id='bar-graph',
        figure=barchart
    ),

    dcc.Graph(
        id='pie-graph',
        figure=line_chart_1
    ),

    dcc.Graph(
        id='corr-graph',
        figure=corr_plot
    ),

    dcc.Graph(
        id='pie_1',
        figure=pie_1
    ),

        dcc.Graph(
        id='pie_2',
        figure=pie_2
    ),

    dcc.Graph(
        id='scatter_1',
        figure=scat_1
    ),

        dcc.Graph(
        id='scatter_2',
        figure=scat_2
    ), 
        dcc.Graph(
        id='scatter_3',
        figure=scat_3
    ),
        dcc.Graph(
        id='chorofil',
        figure=choro
    ),
 
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
	html.Br(),
	html.Div(
		dcc.Graph(figure=corf),
		style={
			'width': '1000px',
			'height': '1000px'
		}
	),
	html.Br(),
	html.Br(),
	html.Div(
		''' '''
	),
	html.Div(style={'height': '200px'}),
#######
#end J#
#######

	html.Div(children='''
        Dash: Another example Bar chart
    '''),
        dcc.Graph(
        id='box_plot',
        figure=sid_box
    ),
	html.Div(children='''
        boxplot
    '''),
	dcc.Graph(
			id='stacked_plot',
			figure=stacked  
	),
	dcc.Graph(
			id='line2_plot',
			figure=line2  
	),

	dcc.Graph(
			id='area1_plot',
			figure=area_1  
	),

	dcc.Graph(
			id='sun_plot',
			figure=sun  
	),
	dcc.Graph(
			id='vio_plot',
			figure=vio  
	),
	dcc.Graph(
			id='sun_plot1',
			figure=sun_1 
	),

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
        title_x= 0.5,
		margin={'autoexpand': False, 'r': 250}
	)
	return ps_fig
#######
#end J#
#######


if __name__ == '__main__':
  app.run_server(debug = True, port = 8080)
