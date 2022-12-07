def clean(df):
	import numpy as np

	#df.head(10)

	#df.info()

	"""There are no null values in the data set except for the column 'count' where there are '436' null values. We shall deep dive into this and decide the course of action as we proceed further."""

	#df.describe()

	df.rename(columns={"count_type":"homelessness", "count":"number"}, inplace = True)

	df['dup']=df.duplicated()
	#print(df.dup.unique())

	df=df.drop(columns='dup')

	df[df['number'].isna()]

	"""We have 436 rows of null values and its corresponding rows provide no useful data, therefore we can drop these rows.

	---


	"""

	df.dropna(subset=['number'], inplace=True)

	#df.info()

	"""We have cleaned the data and handled all the null values."""

	#print(df.state.unique())

	#print(df.state.nunique())

	"""Our state data is accurate with state and union territory codes of USA plus Total."""

	state_region= {'AK':'west','CA':'west','NV':'west','UT':'west','CO':'west','WY':'west','ID':'west','OR':'west','MT':'west','WA':'west','HI':'west', 'GU':'west','MP':'west',
				   'AZ':'southwest','NM':'southwest','TX':'southwest','OK':'southwest',
				   'ND':'midwest','SD':'midwest','NE':'midwest','KS':'midwest','MO':'midwest','IA':'midwest','MN':'midwest','IL':'midwest','WI':'midwest','IN':'midwest','MI':'midwest','OH':'midwest',
				   'AR':'southeast','LA':'southeast','MS':'southeast','AL':'southeast','GA':'southeast','TN':'southeast','DE':'southeast','KY':'southeast','WV':'southeast','DC':'southeast','VA':'southeast','NC':'southeast','SC':'southeast','FL':'southeast','MD':'southeast',
				   'PA':'northeast','NY':'northeast','NJ':'northeast','CT':'northeast','RI':'northeast','MA':'northeast','NH':'northeast','ME':'northeast','VT':'northeast','PR':'northeast','VI':'northeast',
				   'Total': 'Total'}

	df['region'] = df.state.map(state_region)	

	#Territory = ['AS','GU','MP','PR','VI']  # These state codes  

	#df['state_new'] = np.where(df['state'].isin(Territory),'Territory','State')
	
	def is_terr(row):
		if row.state == 'Total':
			return None
		if row.state in ['AS','GU','MP','PR','VI']:
			return 'Territory'
		return 'State'

	df['state_new'] = df.apply(is_terr, axis=1)
	#df.info()
	#df.sample(10)

	return df
