from dash import dcc, html, Input, Output, Dash
import pandas as pd
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

countydata = pd.read_csv("~/Desktop/Personal/Code/Politics/2020_data.csv")['per_point_diff'].tolist()
array = pd.read_csv("~/Desktop/Personal/Code/Politics/finalmatrix.csv").values.tolist()
fips_codes = pd.read_csv("~/Desktop/Personal/Code/Politics/ALtoIA.csv").values.tolist()
final_fips = [str(fip).zfill(5) for sublist in fips_codes for fip in sublist]

fips_states = {"Alabama": "01","Alaska":"02",
"Arizona": "04",
"Arkansas": "05",
"California": "06",
"Colorado": "08",
"Connecticut": "09",
"Delaware": "10",
"DC": "11",
"Florida": "12",
"Georgia": "13",
"Hawaii": "15",
"Idaho": "16",
"Illinois": "17",
"Indiana": "18",
"Iowa": "19",
"Kansas": "20",
"Kentucky": "21",
"Louisiana": "22",
"Maine": "23",
"Maryland": "24",
"Massachusetts": "25",
"Michigan": "26",
"Minnesota": "27",
"Mississippi": "28",
"Missouri": "29",
"Montana": "30",
"Nebraska": "31",
"Nevada": "32",
"New Hampshire": "33",
"New Jersey": "34",
"New Mexico": "35",
"New York": "36",
"North Carolina": "37",
"North Dakota": "38",
"Ohio": "39",
"Oklahoma": "40",
"Oregon": "41",
"Pennsylvania": "42",
"Rhode Island": "44",
"South Carolina": "45",
"South Dakota": "46",
"Tennessee": "47",
"Texas": "48",
"Utah": "49",
"Vermont": "50",
"Virginia": "51",
"Washington": "53",
"West Virginia": "54",
"Wisconsin": "55",
"Wyoming": "56",}
array2 = pd.read_csv("~/Desktop/Personal/Code/Politics/FINALCORRELATION.csv").values.tolist()
for i in range(len(array2)):
    del array2[i][0]
swing_counties=[0]

county_slopes = [array[i].copy()[1:] for i in swing_counties]
county_correlations = []
for i in swing_counties:
    correlation_list = []
    for j in range(len(array2)):
        if (j <= i):
            correlation_list.append(array2[i][j])
        else:
            correlation_list.append(array2[j][i])
    county_correlations.append(correlation_list)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(
        placeholder='Enter a state...',
        type='text',
        value='',
        id='state',
    ),
    dcc.Input(
        placeholder='Enter a county...',
        type='text',
        value='',
        id='county',
    ),   
    dcc.Slider(-100, 100, marks=None,
               value=0,
               step=1,
               id='candidate',
               tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Graph(id="graph")
])

@app.callback(
    Output('graph', 'figure'),
    Input('candidate','value'),
    Input('state','value'),
    Input('county','value')
    )

def display_choropleth(candidate,state,county):
    starting_fips = fips_states[state] + "001"
    starting_search = 0
    for i in range(len(final_fips)):
        if (final_fips[i] == starting_fips):
            starting_search = i

    county_rowcolumn = 0
    for i in range(len(array)):
        if (array[starting_search+i][0] == county):
            county_rowcolumn = starting_search+i
            break
    swing_counties=[county_rowcolumn]
    swing_amounts = [candidate]

    county_slopes = [array[i].copy()[1:] for i in swing_counties]
    county_correlations = []
    for i in swing_counties:
        correlation_list = []
        for j in range(len(array2)):
            if (j <= i):
                correlation_list.append(array2[i][j])
            else:
                correlation_list.append(array2[j][i])
        county_correlations.append(correlation_list)

    finaldata = [countydata[i] + (swing_amounts[swing_counties.index(i)] if i in swing_counties else sum((swing_amounts[j] * county_slopes[j][i] * abs(county_correlations[j][i])) for j in range(len(county_slopes))) / sum(abs(county_correlations[j][i]) for j in range(len(county_slopes)))) / 100 for i in range(len(countydata))]

    df_2 = pd.DataFrame({"fips" : final_fips, "County Correlation" : finaldata})

    fig = px.choropleth(df_2, geojson=counties, locations='fips', color=finaldata,
        color_continuous_scale=[(0.0,"#0D0596"),(0.1,"#0D0596"),
        (0.1,"#584CDE"), (0.2,"#584CDE"),
        (0.2,"#7996E2"), (0.3,"#7996E2"),
        (0.3,"#A5B0FF"), (0.4,"#A5B0FF"),
        (0.4,"#BDD3FF"), (0.5,"#BDD3FF"),
        (0.5,"#FFC8CD"), (0.6,"#FFC8CD"),
        (0.6,"#FFB2B2"), (0.7,"#FFB2B2"),
        (0.7,"#E27F7F"), (0.8,"#E27F7F"),
        (0.8,"#D72F30"), (0.9,"#D72F30"),
        (0.9,"#A80000"),(1.0,"#A80000")],    
        range_color=[-1, 1],     
        width=1440,
        height=720,   
        projection="albers usa",            
        labels={'County Correlation':'finaldata'},
        title = "Chregco Maps"
        )
    fig.update_traces(marker_line_width=1, marker_opacity=0.8)
    fig.update_geos(showsubunits=True, subunitcolor="black")
    return fig

app.run_server(debug=False)