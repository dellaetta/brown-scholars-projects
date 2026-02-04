""" 
Unit Final Project: COVID-19
Analyzing COVID-19 in the United States and its Impact
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Finding the COVID-19 numbers per state
# List of states sorted in alphabetical order
statesList = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

# Corresponding abbreviations for each state.
stateAbbreviationList = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND",
"OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

# Corresponding latitudes for each state.
latitudes = [32.361538, 58.301935, 33.448457, 34.736009, 38.555605, 39.7391667, 41.767, 39.161921, 30.4518, 33.76,
            21.30895, 43.613739, 39.783250, 39.790942, 41.590939, 39.04, 38.197274, 30.45809, 44.323535, 38.972945,
            42.2352, 42.7335, 44.95,32.320, 38.572954,46.595805,40.809868,39.160949,43.220093, 40.221741,35.667231,
            42.659829,35.771, 48.813343,39.962245, 35.482309,44.931109, 40.269789, 41.82355, 34.000,  44.367966,36.165,
            30.266667,40.7547,44.26639, 37.54, 47.042418,38.349497,43.074722, 41.145548]

# Corresponding longitudes for each state.
longitudes = [-86.279118,-134.419740,-112.073844, -92.331122,-121.468926 ,-104.984167 ,-72.677 , -75.526755 ,
              -84.27277,-84.39,-157.826182 ,-116.237651 ,-89.650373 ,-86.147685 ,-93.620866 ,-95.69 , -84.86311
              ,-91.140229 ,-69.765261 ,-76.501157 ,-71.0275 ,-84.5467 , -93.094 ,-90.207 , -92.189283
              , -112.027031 ,-96.675345 ,-119.753877 ,-71.549127 , -74.756138, -105.964575 , -73.781339 ,-78.638 
              ,-100.779004 ,-83.000647 , -97.534994,-123.029159 ,-76.875613 , -71.422132, -81.035, -100.336378
              ,-86.784 ,-97.75 ,-111.892622 ,-72.57194 ,-77.46 ,-122.893077 ,-81.633294 ,-89.384444 ,-104.802042]

# Data from New York Times
# Function returns # of cases over time given name of state
def barCases(name):
  df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
  df_state = df.loc[df["state"] == name].copy().reset_index()
  df_cases = df_state["cases"]
  df_date = df_state["date"]
  plt.bar(df_date,df_cases)
  plt.title("Total amount of cases in " + str(name))
  plt.xlabel("Date")
  plt.ylabel("Death")
  plt.show()
  
  return 

# Function returns # of deaths over time given name of state
def barDeaths(name):
  df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
  df_state = df.loc[df["state"] == name].copy().reset_index()
  df_cases = df_state["deaths"]
  df_date = df_state["date"]
  plt.bar(df_date,df_cases)
  plt.title("Total amount of deaths in " + str(name))
  plt.xlabel("Date")
  plt.ylabel("Cases")
  plt.show()
  
  return 

barCases("New York")
barDeaths("New York")

# Create choropleth map of United States
df_map = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")

# Dataframe Formatter
def dfFormatter(df, selectColumn):
    # Pivot the data: states as rows, dates as columns
    df_formatted = (
        df
        .pivot(index="state", columns="date", values=selectColumn)
        .fillna(0)
        .reset_index()
    )

    # Add latitude and longitude back
    lat_long_df = pd.DataFrame({
        "state": statesList,
        "lat": latitudes,
        "long": longitudes
    })

    df_formatted = df_formatted.merge(lat_long_df, on="state", how="left")

    # Reorder columns: state, lat, long, dates...
    cols = ["state", "lat", "long"] + [
        c for c in df_formatted.columns if c not in ["state", "lat", "long"]
    ]
    df_formatted = df_formatted[cols]

    # Drop extra rows (non-states)
    df_formatted = df_formatted.iloc[:50]

    return df_formatted

cases_formatter = dfFormatter(df_map, "cases")
deaths_formatter = dfFormatter(df_map, "deaths")

colors = ["#FCFCAE", "#FCD97D", "#FCCE7D", "#FFC07D",  "#FEB562", "#F9A648", "#F98E48",
          "#FD8739 ", "#FE7519", "#FE5E19", "#FA520A",  "#FA2B0A", "#9B1803", "#861604",
          "#651104", "#570303"]

total_list = cases_formatter.groupby('state')['2021-06-13'].sum().tolist() 
state_list = cases_formatter["state"].tolist()
state_set = set(state_list)
state_list = list(state_set)
state_list.sort()

new_df = pd.DataFrame(list(zip(state_list, total_list)), 
  columns =['state', 'cases'])

state_abbrev = []
for i in new_df["state"]:
  for c,x in enumerate(statesList):
    if i == x:
      state_abbrev.append(stateAbbreviationList[c])

state_abbrev_dict = dict(zip(state_list, state_abbrev))
new_df["abbreviations"] = new_df["state"].map(state_abbrev_dict)
new_df.pop("state")

fig = go.Figure(data = go.Choropleth(
    locationmode = "USA-states",
    locations = new_df["abbreviations"],
    z = new_df["cases"],
    autocolorscale = False,
    colorscale = colors,
    reversescale = False,
    colorbar_title = "# of cases"
))

fig.update_layout(
    title_text = "United States COVID-19 Cases",
    title_x = 0.5,
    geo_scope = "usa",
)

fig.show()

total_list = deaths_formatter.groupby('state')['2021-06-13'].sum().tolist() 
state_list = deaths_formatter["state"].tolist()
state_set = set(state_list)
state_list = list(state_set)
state_list.sort()

new_df = pd.DataFrame(list(zip(state_list, total_list)), 
  columns =['state', 'deaths'])
state_abbrev = []
for i in new_df["state"]:
  for c,x in enumerate(statesList):
    if i == x:
      state_abbrev.append(stateAbbreviationList[c])

state_abbrev_dict = dict(zip(state_list, state_abbrev))
new_df["abbreviations"] = new_df["state"].map(state_abbrev_dict)
new_df.pop("state")

fig = go.Figure(data = go.Choropleth(
    locationmode = "USA-states",
    locations = new_df["abbreviations"],
    z = new_df["deaths"],
    autocolorscale = False,
    colorscale = colors,
    reversescale = False,
    colorbar_title = "# of deaths"
))

fig.update_layout(
    title_text = "United States COVID-19 Deaths",
    title_x = 0.5,
    geo_scope = "usa",
)
fig.show()

""" 
Analyze the impagct on the United States 
Analyze testing in New York State, create one bar plot of # of tests conducted per day and another bar plot of # of new positives found per day.
"""
df_tests = pd.read_csv("data/New_York_State_Statewide_COVID-19_Testing.csv")
df_tests.head()
test_date = df_tests["Test Date"]
test_dates_string = []
for i in test_date:
  test_dates_string.append(str(i))

del test_dates_string[470:29140]

tests_performed = []
new_positives = []
for i in test_dates_string:
  df_per_day = df_tests.loc[df_tests["Test Date"] == i]
  test_totals = sum(df_per_day["Total Number of Tests Performed"])
  tests_performed.append(test_totals)
  positive = sum(df_per_day["New Positives"])
  new_positives.append(positive)

plt.bar(test_dates_string, tests_performed)
plt.xlabel("Dates")
plt.ylabel("Amount of Tests Performed")
plt.title("Amount of Tests Performed per day in New York")
plt.show()

plt.bar(test_dates_string, new_positives)
plt.xlabel("New Positi ves")
plt.ylabel("Amount of New Positives")
plt.title("Amount of New Positives per day in New York")
plt.show()