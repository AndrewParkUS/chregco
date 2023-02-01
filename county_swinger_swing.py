import pandas as pd
import random
import math
df = pd.read_csv("~/Desktop/Personal/Code/Politics/finalmatrix.csv")
array = df.values.tolist()


# 'Autauga', 1.0, nan, nan, .... etc.
df_fips = pd.read_csv("~/Desktop/Personal/Code/Politics/ALtoIA.csv")
fips_codes = df_fips.values.tolist()
final_fips = [item for sublist in fips_codes for item in sublist]
for i in range(len(final_fips)):
    if (final_fips[i] < 10000):
        final_fips[i] = "0" + str(final_fips[i])
    else:
        final_fips[i] = str(final_fips[i])

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
df3 = pd.read_csv("~/Desktop/Personal/Code/Politics/2020_data.csv",
                    dtype={"county_fips": str})
countydata = df3['per_point_diff'].tolist()

swing_amounts = []
def find_county():
    chosen_state = input("Choose a state: ")
    starting_fips = fips_states[chosen_state] + "001"
    starting_search = 0
    for i in range(len(final_fips)):
        if (final_fips[i] == starting_fips):
            starting_search = i

    chosen_county = input("Choose a base county: ")
    # need to find row/column of that county (which is same)
    county_rowcolumn = 0

    for i in range(len(array)):
        if (array[starting_search+i][0] == chosen_county):
            county_rowcolumn = starting_search+i
            break
    swing_amounts.append(float(input("Swing Percent: ")))

    return county_rowcolumn

# loop until they dont want to change any more counties
swing_counties = [] # list of county rowcolumns
while True:
    check = input("Continue? ")
    if (check == "y"):
        swing_counties.append(find_county())
    else:
        break
# 2d list that holds each county's slopes
county_slopes = []
for i in swing_counties:
    appending = array[i].copy()
    del appending[0]
    county_slopes.append(appending)

# 2d list that holds each county's correlations
correlationdf = pd.read_csv("~/Desktop/Personal/Code/Politics/FINALCORRELATION.csv")
array2 = correlationdf.values.tolist()
county_correlations = []
for i in range(len(array2)):
    del array2[i][0]
for i in swing_counties:
    correlation_list = []
    for j in range(len(array2)):
        if (j <= i):
            correlation_list.append(array2[i][j])
        else:
            correlation_list.append(array2[j][i])
    county_correlations.append(correlation_list)

# swing_amounts holds each county's amount to swing by 
for i in range(len(county_slopes[0])): # for EACH of ALL county
    # sum = 0
    # term = 0
    # for j in range(len(county_slopes)):
    #     sum += swing_amounts[j] * county_slopes[j][i]
    #     term += 1
    # countydata[i] += (sum/term)/100
    sum = 0
    correlation = 0
    for j in range(len(county_slopes)): # for each county we're changing
        sum += (swing_amounts[j] * county_slopes[j][i]) * abs(county_correlations[j][i])
        correlation += abs(county_correlations[j][i])
    countydata[i] = (sum / correlation) / 100

# for each_county in range(len(county_slopes[0])): # for each of the 3000 counties
#     sum, correlation = 0
#     for changed_county in range(len(county_slopes)): # for each county we're changing
#         sum += 


# convert fips + correlation_list back to csv file (BRUH)
dict = {"fips" : final_fips, "County Correlation" : countydata}
df_2 = pd.DataFrame(dict)

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import plotly.express as px
import plotly.graph_objects as go

fig = px.choropleth(df_2, geojson=counties, locations='fips', color=countydata,
    # color_continuous_scale=px.colors.diverging.RdBu_r,
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
    # scope="usa",
    width=1440,
    height=720,   
    projection="albers usa",            
    labels={'per_point_diff':'Margin'},
    title = "County Swing Map"
    )
fig.update_traces(marker_line_width=1, marker_opacity=0.8)
fig.update_geos(
showsubunits=True, subunitcolor="black"
)
fig.show()