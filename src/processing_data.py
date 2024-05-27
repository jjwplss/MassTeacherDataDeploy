import pandas as pd
import os as os
from dash import Dash, dash_table, html, dcc, callback, Output, Input
import plotly.express as px

# somehow the head is 2nd row
df1 = pd.read_excel('C:\\Users\\kansa\\Documents\\MassTeacherData\\data\\2022_2023\\TeacherData.xlsx', header=1)
#df1.head(5)
replace_value_df1 = {' to 1': ''}
df1 =df1.replace({'Student / Teacher Ratio': replace_value_df1}, regex=True)
df1.iloc[:,0:5].head(3) # check data and see if there are any non-numeric symbols
df1.iloc[:,5:10].head(3)

df2 = pd.read_excel('C:\\Users\\kansa\\Documents\\MassTeacherData\\data\\2022_2023\\ClassSizebyGenPopulation.xlsx', header=1)
df2 = df2.drop('District Name',axis=1)
df1.columns.difference(df2.columns) # confirm that 'District Code' is dropped
df2.iloc[:,1:5].head(3)
df2.iloc[:,5:10].head(3)

salary_20_21 = pd.read_excel('C:\\Users\\kansa\\Documents\\MassTeacherData\\data\\2020_2021\\TeacherSalaries.xlsx', header=1)
salary_20_21.shape # only 396, compared with 399 rows in df1 and df2
salary_20_21.columns.difference(df1.columns)
salary_20_21 = salary_20_21.drop('District Name',axis=1)
salary_20_21 = salary_20_21.rename(columns={'Average Salary': 'Average Salary 2020-21', 'FTE Count':'FTE Count 2020-21','Salary Totals':'Salary Totals 2020-21'})
replace_values = {',': '', '\$':''} # need to escape using \$
salary_20_21 = salary_20_21.replace({"Salary Totals 2020-21": replace_values},regex=True)
salary_20_21 = salary_20_21.replace({"Average Salary 2020-21": replace_values},regex=True)
salary_20_21.head(4)

type(salary_20_21['Salary Totals 2020-21'][1])

df_m = pd.merge(df1, df2, on='District Code', how='left', indicator=True)
df_m['_merge'].value_counts()
df_m = df_m.drop('_merge',axis=1)

df_merged = pd.merge(df_m, salary_20_21, on='District Code', how='left', indicator=True)
df_merged['_merge'].value_counts()
df_merged[df_merged['_merge']!='both'].head(5)
df_merged = df_merged.rename(columns={'_merge':'Merge Status'})


df_merged.iloc[:,1:5].head(3)
df_merged.iloc[:,5:8].head(3)
df_merged.iloc[:,8:11].head(3)

'''
# somehow the first column will be renamed with _x
if 'District Name_x' in df_merged.columns:
    df_merged = df_merged.rename(columns={'District Name_x': 'District Name'})

columns_to_remove = [col for col in df_merged.columns if '_' in col]

# Drop the columns
df_merged = df_merged.drop(columns=columns_to_remove)
'''

df_merged = df_merged.rename(columns={'District Name': 'District'})

df_merged.columns.tolist()

df_merged.columns
df_merged.columns[2]

print(df_merged.dtypes)
c1 = df_merged.iloc[115:117] # 116 are NaN
type(c1)
# df_merged.iloc[115:117]['Percent Teaching In-Field'] # the charter school has missing in Percent, NaN
for col in c1.columns[2:]:
    c1[col]=pd.to_numeric(c1[col].replace(",","",regex=True), errors='coerce')
c1.dtypes
c1['Percent Teaching In-Field']
c

fig = px.bar(c1, x='Percent Teaching In-Field', y='District', orientation='h')
fig.show()

# convert the 1,234 to 1234
print(df_merged.dtypes)

# https://saturncloud.io/blog/pandas-tips-change-column-type/
df_merged['Total # of Teachers (FTE)'] = pd.to_numeric(df_merged['Total # of Teachers (FTE)'])

# https://stackoverflow.com/questions/36684013/extract-column-value-based-on-another-column-in-pandas
df_merged.query('District==@Boston')['Total # of Teachers (FTE)']


df_merged[df_merged['District']=='Boston']['Total # of Teachers (FTE)'].item()
# without item() it is a pandas series, with item() it is scalar
# "4,311.6"

# https://stackoverflow.com/questions/42331992/replace-part-of-the-string-in-pandas-data-frame
# need regex=TRUE; otherwise will need perfect match of ","
df_merged['Total # of Teachers (FTE)']=df_merged['Total # of Teachers (FTE)'].replace(",","",regex=True)
df_merged[df_merged['District']=='Boston']['Total # of Teachers (FTE)'].item()
type(df_merged['Total # of Teachers (FTE)'][0])  # still string
type(df_merged['Total # of Teachers (FTE)'].astype(float)[0]) 

df_merged['Total # of Teachers (FTE)'].replace(",","",regex=True).astype(float)

df_merged.columns[1:]
# Iterate through columns starting from the second column
df_merged.dtypes
type(df_merged['District'])=
print(df_merged['District'].dtype)=='object'

pd.to_numeric("1231.9", errors='coerce')

column_bound = len(df_merged.columns)-1
for col in df_merged.columns[2:column_bound]:
    # astype(float) cannot convert 11.9 to 11
    # https://stackoverflow.com/questions/75711289/how-to-convert-pandas-column-to-numeric-if-there-are-strings
    df_merged[col]=pd.to_numeric(df_merged[col].replace(",","",regex=True), errors='coerce')

df_merged.dtypes
df_merged.isnull().any()
df_merged.iloc[:,1:5].head(3)
df_merged.iloc[:,5:8].head(3)
df_merged.iloc[:,8:11].head(3)
df_merged.iloc[:,11:14].head(3)
df_merged.iloc[:,14:18].head(3)
df_merged.iloc[:,18:21].head(3)

df_merged['Percent Teaching In-Field'][0:3]
check = df_merged[['Percent Teaching In-Field']] # double brackets, so still a dataframe

# teacher-student ratios are all NaN. why
df_nan = check.loc[check.isnull().any(axis=1)]
'''
     Percent Teaching In-Field
116                        NaN
129                        NaN
181                        NaN
271                        NaN
'''

'''
    if print(df_merged[col].dtype)!="float64":
        print(df_merged[col].dtype)
'''    

    #df_merged[col] = df_merged[col].replace(",","",regex=True).astype(float)


# remove the row of State Total, sort by a column and get the first 10 rows
# filtered = df_merged[df_merged['District Code'] != 0].sort_values(by='Number of Students', ascending=False).head(10)

# selected = df_merged[df_merged['District Name'].isin(['Boston','Worcester','Springfield'])]
#df_merged.shape

'''
fig = px.bar(selected, x='District Name', y='Students with Disabilities %')
fig.show()
'''

dff = df_merged[df_merged['District'].isin(['Boston','Lexington','Arlington'])]
fig = px.bar(dff, y=dff.columns[2], x='District') #, orientation='h')
fig.show()


app = Dash(__name__)
app.layout = html.Div([
    html.Div(children='Mass Teacher Data',style={'textAlign':'center'}),
    dash_table.DataTable(data=df_merged.to_dict('records'), page_size=20),
    dcc.Dropdown(df_merged['District Name'].unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df_merged[df_merged['District Name']==value]
    return px.line(dff, x='District Name', y='Students with Disabilities %')


