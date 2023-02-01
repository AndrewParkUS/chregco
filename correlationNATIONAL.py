import pandas as pd
import random
import math
df = pd.read_csv("~/Desktop/Personal/Code/Politics/FINALCORRELATION.csv")
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

chosen_state = input("Choose a state: ")
starting_fips = fips_states[chosen_state] + "001"
starting_search = 0
for i in range(len(final_fips)):
    if (final_fips[i] == starting_fips):
        starting_search = i
print(starting_fips)
print(starting_search)

chosen_county = input("Choose a base county: ")
# need to find row/column of that county (which is same)
county_rowcolumn = 0

for i in range(len(array)):
    if (array[starting_search+i][0] == chosen_county):
        county_rowcolumn = starting_search+i
        break
print(county_rowcolumn) # 0th index means 1st row, fucking trippy af istg

correlation_list = []
for i in range(len(array)):
    del array[i][0]

for i in range(len(array)):
    if (i <= county_rowcolumn):
        correlation_list.append(array[county_rowcolumn][i])
    else:
        correlation_list.append(array[i][county_rowcolumn])

# # print(correlation_list)
print(len(correlation_list))
# # print(fips_codes)
print(len(final_fips))
# print(final_fips)

# convert fips + correlation_list back to csv file (BRUH)
dict = {"fips" : final_fips, "County Correlation" : correlation_list}
df_2 = pd.DataFrame(dict)

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import plotly.express as px
import plotly.graph_objects as go

fig = px.choropleth(df_2, geojson=counties, locations="fips", color=correlation_list,
    range_color=[-1, 1],          
    color_continuous_scale=px.colors.diverging.RdYlGn,
    title = chosen_county + " County, " + chosen_state + " Correlation Map",
    width=1440,
    height=720,
    projection="albers usa",
    )
# fig.update_geos(fitbounds="locations", visible=False)
fig.show()
    # color_continuous_scale=px.colors.diverging.RdYlGn,         