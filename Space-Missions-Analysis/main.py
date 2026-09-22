import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
from datetime import datetime, timedelta

pd.options.display.float_format = '{:,.2f}'.format  # Might just be for colab
plt.close('all')

# Load the data
df_data = pd.read_csv('mission_launches.csv')

## Preliminary Data Exploration
# What is the shape of df_data?
print(df_data.shape)
# How many rows and columns does it have?
print(df_data.info)
# What are the column names?
print(df_data.columns)
print(df_data.head())
# Are there any NaN values or duplicates?
print(f'Any NaN values among the data? {df_data.isna().values.any()}')
print(df_data.isna().sum())

## Data Cleaning - Check for Missing Values and Duplicates
print(f'Any duplicates? {df_data.duplicated().values.any()}')

## Descriptive Statistics

# Number of Launches per Company
# Create a chart that shows the number of space mission launches by organisation.
launches_by_org = df_data["Organisation"].value_counts()  # Count launches by organisation
launches_by_org.plot(kind="bar", figsize=(12, 6))  # Create the bar chart

plt.xlabel("Organisation")
plt.ylabel("Number of launches")
plt.title("Number of Space Mission Launches by Organisation")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Number of Active versus Retired Rockets - How many rockets are active compared to those that are decomissioned?
rocket_status = df_data["StatusActive"].value_counts()
print(rocket_status)

# Distribution of Mission Status - How many missions were successful? How many missions failed?
rocket_status = df_data["Success"].value_counts()
print(rocket_status)

# How Expensive are the Launches? - Create a histogram and visualise the distribution. The price column is given in USD millions (careful of missing values).
price_of_launches = df_data["Price"].dropna()
hist = px.histogram(price_of_launches)

hist.update_layout(xaxis_title='Price of Rocket Launches (USD millions)', yaxis_title='Number of Launches', )

hist.show()

# Use a Choropleth Map to Show the Number of Launches by Country

# - Create a choropleth map using [the plotly
#   documentation](https://plotly.com/python/choropleth-maps/)
# - Experiment with [plotly\'s available
#   colours](https://plotly.com/python/builtin-colorscales/). I quite like
#   the sequential colour `matter` on this map.
# - You\'ll need to extract a `country` feature as well as change the
#   country names that no longer exist.
#
# Wrangle the Country Names

# You\'ll need to use a 3 letter country code for each country. You might
# have to change some country names.

# - Russia is the Russian Federation
# - New Mexico should be USA
# - Yellow Sea refers to China
# - Shahrud Missile Test Site should be Iran
# - Pacific Missile Range Facility should be USA
# - Barents Sea should be Russian Federation
# - Gran Canaria should be USA

def get_country_code(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None
# Extract country
df_data["Country"] = df_data["Location"].str.split(",").str[-1].str.strip()

country_replacements = {
    "Russia": "Russian Federation",
    "New Mexico": "USA",
    "Yellow Sea": "China",
    "Shahrud Missile Test Site": "Iran",
    "Pacific Missile Range Facility": "USA",
    "Barents Sea": "Russian Federation",
    "Gran Canaria": "USA"
}
# Fix special cases
df_data["Country"] = df_data["Country"].replace(country_replacements)
# Creating three letter ISO code
df_data["ISO3"] = df_data["Country"].apply(get_country_code)

launches_by_country = df_data["ISO3"].value_counts().reset_index()
launches_by_country.columns = ["Country", "Launches"]

# You can use the iso3166 package to convert the country names to Alpha3 format.

fig = px.choropleth(
    launches_by_country,
    locations="Country",
    color="Launches",
    color_continuous_scale="matter",
    locationmode="ISO-3",
    title="Number of Space Launches by Country"
)

fig.show()

# Use a Choropleth Map to Show the Number of Failures by Country

failures = df_data[df_data["Success"] == False]
failures["Country"] = failures["Location"].str.split(",").str[-1].str.strip()

failures_by_country = failures["Country"].value_counts().reset_index()
failures_by_country.columns = ["Country", "Failures"]

fig = px.choropleth(
    rocket_status,
    locations="Country",
    color="Failures",
    color_continuous_scale="matter",
    locationmode="ISO-3",
    title="Number of Failures by Country"
)

fig.show()

# Create a Plotly Sunburst Chart of the countries, organisations, and mission status.

country_org_mission = df_data.groupby(
    ['Country', 'Organisation', 'Mission_Status'],
    as_index=False
).agg({'Mission_Status': pd.Series.count})

burst = px.sunburst(
    country_org_mission,
    path=['Country', 'Organisation', 'Mission_Status'],
    values='Mission_Status',
    title='Where are rockets being launched?'
)

burst.update_layout(
    coloraxis_showscale=False
)

burst.show()

# Analyse the Total Amount of Money Spent by Organisation on Space Missions
money_by_organisation  = df_data.groupby("Organisation")["Price"].sum()
print(money_by_organisation)

# Analyse the Amount of Money Spent by Organisation per Launch
money_per_launch = df_data.groupby("Organisation").agg(
    Total_Spent=("Price", "sum"),
    Number_of_Launches=("Organisation", "count")
)

money_per_launch["Spent_Per_Launch"] = (
    money_per_launch["Total_Spent"] /
    money_per_launch["Number_of_Launches"]
)

print(money_per_launch)


# Chart the Number of Launches per Year

df_data["Date"] = pd.to_datetime(df_data["Date"])

launches_per_year = df_data["Date"].dt.year.value_counts().sort_index()

print(launches_per_year)

launches_per_year.plot(kind="line")

plt.xlabel("Year")
plt.ylabel("Number of Launches")
plt.title("Number of Space Launches per Year")

plt.show()

# Chart the Number of Launches Month-on-Month until the Present

launches_per_month = df_data["Date"].dt.to_period("M").value_counts().sort_index()

print(launches_per_month)

launches_per_month.plot(kind="line")

plt.xlabel("Month")
plt.ylabel("Number of Launches")
plt.title("Number of Space Launches Month-on-Month")

plt.show()

# Which month has seen the highest number of launches in all time?
# Superimpose a rolling average on the month on month time series chart.
print(launches_per_month.idxmax())
print(launches_per_month.max())

rolling_average = launches_per_month.rolling(12).mean()

launches_per_month.plot(kind="line", label="Monthly Launches")
rolling_average.plot(kind="line", label="12-Month Rolling Average")

plt.xlabel("Month")
plt.ylabel("Number of Launches")
plt.title("Space Launches per Month")
plt.legend()

plt.show()

# Launches per Month: Which months are most popular and least popular for launches?
launches_per_month = df_data["Date"].dt.month_name().value_counts()
month_counts = df_data["Date"].dt.month.value_counts().sort_index()

month_counts.plot(kind="bar")

plt.xlabel("Month")
plt.ylabel("Number of Launches")
plt.title("Number of Space Launches by Month")

plt.show()

print("Most popular month:", month_counts.idxmax())
print("Most launches:", month_counts.max())

print("Least popular month:", month_counts.idxmin())
print("Fewest launches:", month_counts.min())

# Some months have better weather than others. Which time of year seems to be best for space missions?
print(month_counts)
month_counts.plot(kind="bar")

plt.xlabel("Month")
plt.ylabel("Number of Launches")
plt.title("Number of Space Launches by Month")

plt.show()

# How has the Launch Price varied Over Time?
df_data["Date"] = pd.to_datetime(df_data["Date"])

fig = px.scatter(
    df_data.dropna(subset=["Price"]),
    x="Date",
    y="Price",
    title="Launch Price Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Launch Price (USD millions)"
)

fig.show()

# Create a line chart that shows the average price of rocket launches over time.

df_data["Date"] = pd.to_datetime(df_data["Date"])

average_price_by_year = (
    df_data.dropna(subset=["Price"])
    .groupby(df_data["Date"].dt.year)["Price"]
    .mean()
)

fig = px.line(
    average_price_by_year,
    x=average_price_by_year.index,
    y=average_price_by_year.values,
    title="Average Price of Rocket Launches Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Launch Price (USD millions)"
)

fig.show()

# Chart the Number of Launches over Time by the Top 10 Organisations.
# Find the top 10 organisations
top10_orgs = df_data["Organisation"].value_counts().head(10).index

# Keep only the top 10 organisations
top10_data = df_data[df_data["Organisation"].isin(top10_orgs)]

# Convert Date to datetime
top10_data["Date"] = pd.to_datetime(top10_data["Date"])

# Count launches per year for each organisation
launches_by_year = top10_data.groupby(
    [top10_data["Date"].dt.year, "Organisation"]
).size().reset_index(name="Launches")

# Create the chart
fig = px.line(
    launches_by_year,
    x="Date",
    y="Launches",
    color="Organisation",
    title="Number of Launches over Time by Top 10 Organisations"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Launches"
)

fig.show()


# How has the dominance of launches changed over time between the different players?
df_data["Date"] = pd.to_datetime(df_data["Date"])

launches_by_org_year = (
    df_data.groupby([df_data["Date"].dt.year, "Organisation"])
    .size()
    .reset_index(name="Launches")
)

fig = px.line(
    launches_by_org_year,
    x="Date",
    y="Launches",
    color="Organisation",
    title="Launch Dominance by Organisation Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Launches"
)

fig.show()

# Cold War Space Race: USA vs USSR - The cold war lasted from the start of the dataset up until 1991.
df_data["Date"] = pd.to_datetime(df_data["Date"])

cold_war = df_data[df_data["Date"].dt.year <= 1991]

usa_ussr = cold_war[
    cold_war["Organisation"].isin(["NASA", "RVSN USSR"])
]

launches = usa_ussr["Organisation"].value_counts()

print(launches)

fig = px.bar(
    launches,
    x=launches.index,
    y=launches.values,
    title="Cold War Space Race: USA vs USSR"
)

fig.update_layout(
    xaxis_title="Organisation",
    yaxis_title="Number of Launches"
)

fig.show()

# Create a Plotly Pie Chart comparing the total number of launches of the USSR and the USA
# Hint: Remember to include former Soviet Republics like Kazakhstan when analysing the total number of launches.
df_data["Country"] = df_data["Location"].str.split(",").str[-1].str.strip()

usa = df_data[df_data["Country"] == "USA"].shape[0]

ussr = df_data[df_data["Country"].isin(["Russia", "Kazakhstan"])].shape[0]

launches = pd.Series({
    "USA": usa,
    "USSR": ussr
})

print(launches)

fig = px.pie(
    values=launches.values,
    names=launches.index,
    title="Total Space Launches: USSR vs USA"
)

fig.show()

# Create a Chart that Shows the Total Number of Launches Year-On-Year by the Two Superpowers
df_data["Superpower"] = df_data["Country"].replace({
    "Russia": "USSR",
    "Kazakhstan": "USSR",
    "USA": "USA"
})

superpowers = df_data[
    df_data["Superpower"].isin(["USA", "USSR"])
]

launches_by_year = (
    superpowers.groupby(
        [superpowers["Date"].dt.year, "Superpower"]
    )
    .size()
    .reset_index(name="Launches")
)

fig = px.line(
    launches_by_year,
    x="Date",
    y="Launches",
    color="Superpower",
    title="USA vs USSR Launches Year-on-Year"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Launches"
)

fig.show()

# Chart the Total Number of Mission Failures Year on Year.
failures = df_data[df_data["Success"] == False]

failures_by_year = (
    failures.groupby(failures["Date"].dt.year)
    .size()
)

fig = px.line(
    failures_by_year,
    x=failures_by_year.index,
    y=failures_by_year.values,
    title="Total Number of Mission Failures per Year"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Failures"
)

fig.show()

# Chart the Percentage of Failures over Time
# Did failures go up or down over time? Did the countries get better at minimising risk and improving their chances of success over time?
yearly_failures = (
    df_data.groupby(df_data["Date"].dt.year)["Success"]
    .apply(lambda x: (x == False).mean() * 100)
)

fig = px.line(
    yearly_failures,
    x=yearly_failures.index,
    y=yearly_failures.values,
    title="Percentage of Mission Failures Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Failure Rate (%)"
)

fig.show()

# For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including including 2020)
# Do the results change if we only look at the number of successful launches?
superpowers = df_data[
    (df_data["Superpower"].isin(["USA", "USSR"])) &
    (df_data["Date"].dt.year <= 2020)
]

year_country = (
    superpowers.groupby(
        [superpowers["Date"].dt.year, "Superpower"]
    )
    .size()
    .reset_index(name="Launches")
)

fig = px.line(
    year_country,
    x="Date",
    y="Launches",
    color="Superpower",
    title="USA vs USSR Launches by Year"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Launches"
)

fig.show()

# Only successful launches
successful = superpowers[superpowers["Success"] == True]

successful_by_year = (
    successful.groupby(
        [successful["Date"].dt.year, "Superpower"]
    )
    .size()
    .reset_index(name="Successful Launches")
)

fig = px.line(
    successful_by_year,
    x="Date",
    y="Successful Launches",
    color="Superpower",
    title="USA vs USSR Successful Launches by Year"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Successful Launches"
)

fig.show()

# Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches

launches_by_org_year = (
    df_data.groupby(
        [df_data["Date"].dt.year, "Organisation"]
    )
    .size()
    .reset_index(name="Launches")
)

top_org_each_year = (
    launches_by_org_year.loc[
        launches_by_org_year.groupby("Date")["Launches"].idxmax()
    ]
)

print(top_org_each_year)

fig = px.bar(
    top_org_each_year,
    x="Date",
    y="Launches",
    color="Organisation",
    title="Organisation with the Most Launches Each Year"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Launches"
)

fig.show()

# Which organisation was dominant in the 1970s and 1980s?
seventies_eighties = launches_by_org_year[
    launches_by_org_year["Date"].between(1970, 1989)
]

dominant_orgs = (
    seventies_eighties.groupby("Organisation")["Launches"]
    .sum()
    .sort_values(ascending=False)
)

print(dominant_orgs)

# Which organisation was dominant in 2018, 2019 and 2020?

recent_orgs = launches_by_org_year[
    launches_by_org_year["Date"].isin([2018, 2019, 2020])
]

top_recent = (
    recent_orgs.loc[
        recent_orgs.groupby("Date")["Launches"].idxmax()
    ]
)

print(top_recent)