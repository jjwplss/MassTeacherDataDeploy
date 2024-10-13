import pandas as pd
import os as os
from dash import Dash, dash_table, html, dcc, callback, Output, Input
import plotly.express as px

# somehow the head is 2nd row
df1 = pd.read_excel('data/2022_2023/TeacherData.xlsx', header=1)
replace_value_df1 = {' to 1': ''}  # in the Excell it is "19.1 to 1"
df1 =df1.replace({'Student / Teacher Ratio': replace_value_df1}, regex=True)

df2 = pd.read_excel('data/2022_2023/ClassSizebyGenPopulation.xlsx', header=1)
df2 = df2.drop('District Name', axis=1)

salary_20_21 = pd.read_excel('data/2020_2021/TeacherSalaries.xlsx', header=1)
salary_20_21 = salary_20_21.drop('District Name',axis=1)
salary_20_21 = salary_20_21.rename(columns={'Average Salary': 'Average Salary 2020-21', 'FTE Count':'FTE Count 2020-21','Salary Totals':'Salary Totals 2020-21'})
replace_values = {',': '', '\$':''} # need to escape
salary_20_21 = salary_20_21.replace({"Salary Totals 2020-21": replace_values}, regex=True)
salary_20_21 = salary_20_21.replace({"Average Salary 2020-21": replace_values}, regex=True)

df_m = pd.merge(df1, df2, on='District Code', how='left', indicator=True)
df_m['_merge'].value_counts()
df_m = df_m.drop('_merge',axis=1)

df_merged = pd.merge(df_m, salary_20_21, on='District Code', how='left', indicator=True)
# df_merged['_merge'].value_counts()
# df_merged[df_merged['_merge']!='both']
df_merged = df_merged.rename(columns={'District Name': 'District', '_merge':'Merge Status'})
df_merged = df_merged.drop('Merge Status',axis=1)
#df_merged = df_merged.rename(columns={})

# remove the row of State Total, sort by a column and get the first 10 rows
# filtered = df_merged[df_merged['District Code'] != 0].sort_values(by='Number of Students', ascending=False).head(10)

# selected = df_merged[df_merged['District'].isin(['Boston','Worcester','Springfield'])]
#df_merged.shape

# 1. replace "123,4.9" with "1234.9"; 2. Then, convert "1234.9" to numeric
column_bound = len(df_merged.columns) - 1
for col in df_merged.columns[2:column_bound]:
    # astype(float) cannot convert 11.9 to 11
    # https://stackoverflow.com/questions/75711289/how-to-convert-pandas-column-to-numeric-if-there-are-strings
    df_merged[col]=pd.to_numeric(df_merged[col].replace(",","",regex=True), errors='coerce')


app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(children='A tool for Massachusetts public school teachers to compare salaries and other outcomes by district',
             style={'textAlign':'center',
                    'font-size': '24px'}),
    html.Div(children='Version 0.1; data is based on 2023 Teacher Salaries Report from Massachusetts Department of Education',
             style={'textAlign':'center',
                    'font-size': '14px'}),

    html.Label('Select school districts', style={'fontSize': '20px'}),
    # district dropdown
    dcc.Dropdown(df_merged['District'].unique(), 
                 value = ['Arlington','Lexington','Watertown'], 
                 id='district-selection',
                 multi=True),
    # select a measure
    #dcc.Dropdown(options=df_merged.columns.tolist(), value='Student / Teacher Ratio', id='my-ddk-radio-items-final'),
    html.Label('Select an outcome:', style={'fontSize': '20px'}),
    dcc.Dropdown(
        id='measure-dropdown',
        # For each column, it creates a dictionary with two keys: 'label' and 'value'. 
        # {'label': col, 'value': col}:
        # The label is set to the column name (col), and the value is also set to the column name (col). 
        # This ensures that the column name is both displayed to the user and used as the value 
        # when an option is selected.
        options=[{'label': col, 'value': col} for col in df_merged.columns[2:]], 
        value=df_merged.columns[2],  # Default value
        clearable=False
    ),
    dcc.Graph(id='graph-content'),
    #html.Div(children='Raw data from the Department of Education',style={'textAlign':'left'}),
    #dash_table.DataTable(data=df_merged.to_dict('records'), page_size=20),

    html.A([html.H3('Any feedback?')], title ='email_me', href='mailto:cfaw.tickets@gmail.com')
])

@callback(
    Output('graph-content', 'figure'),
    [Input('district-selection', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_graph(selected_city, selected_column):
    #https://stackoverflow.com/questions/75721229/only-list-like-objects-are-allowed-to-be-passed-to-isn
    # district-selection would give string, not a list; isin() expects a list, resulting in error
    # dff = df_merged[df_merged['District'].isin(selected_city)]
    # In the query() method, the @ symbol is used as a special syntax to reference variables from 
    # the local or global namespace within the query string
    dff = df_merged.query('District==@selected_city')
    fig = px.bar(dff, x=selected_column, y='District', orientation='h')
    return fig.update_yaxes(categoryorder="total ascending")

if __name__ == '__main__':
    app.run(debug=True)
