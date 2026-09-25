import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


# Notebook Presentation
pd.options.display.float_format = '{:,.2f}'.format
plt.close('all')

# Load the data
df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")

# Convert numeric columns from strings to numbers
df_pct_poverty["poverty_rate"] = pd.to_numeric(
    df_pct_poverty["poverty_rate"],
    errors="coerce"
)

df_pct_completed_hs["percent_completed_hs"] = pd.to_numeric(
    df_pct_completed_hs["percent_completed_hs"],
    errors="coerce"
)
race_columns = [
    "share_white",
    "share_black",
    "share_hispanic",
    "share_asian",
    "share_native_american"
]

for column in race_columns:
    df_share_race_city[column] = pd.to_numeric(
        df_share_race_city[column],
        errors="coerce"
    )

## Preliminary Data Exploration
# What is the shape of the DataFrames?
print(df_fatalities)
print(df_hh_income)
print(df_pct_completed_hs)
print(df_pct_poverty)
print(df_share_race_city)

# How many rows and columns do they have?
# What are the column names?
print(df_fatalities.columns)
print(df_fatalities.head())

print(df_hh_income.columns)
print(df_hh_income.head())

print(df_pct_completed_hs.columns)
print(df_pct_completed_hs.head())

print(df_pct_poverty.columns)
print(df_pct_poverty.head())

print(df_share_race_city.columns)
print(df_share_race_city.head())


# Are there any NaN values or duplicates?
print(f'Any NaN values among the data? {df_fatalities.isna().values.any()}')
print(df_fatalities.isna().sum())

print(f'Any NaN values among the data? {df_hh_income.isna().values.any()}')
print(df_hh_income.isna().sum())

print(f'Any NaN values among the data? {df_pct_completed_hs.isna().values.any()}')
print(df_pct_completed_hs.isna().sum())

print(f'Any NaN values among the data? {df_pct_poverty.isna().values.any()}')
print(df_pct_poverty.isna().sum())

print(f'Any NaN values among the data? {df_share_race_city.isna().values.any()}')
print(df_share_race_city.isna().sum())

# Data Cleaning - Check for Missing Values and Duplicates
# Consider how to deal with the NaN values. Perhaps substituting 0 is appropriate.
print(f'Any duplicates? {df_fatalities.duplicated().values.any()}')

print(f'Any duplicates? {df_hh_income.duplicated().values.any()}')

print(f'Any duplicates? {df_pct_completed_hs.duplicated().values.any()}')

print(f'Any duplicates? {df_pct_poverty.duplicated().values.any()}')

print(f'Any duplicates? {df_share_race_city.duplicated().values.any()}')

# Chart the Poverty Rate in each US State
# Create a bar chart that ranks the poverty rate from highest to lowest by US state. Which state has the highest poverty rate?
# Which state has the lowest poverty rate? Bar Plot

poverty_per_state = (
			df_pct_poverty
			.groupby("Geographic Area")["poverty_rate"]
			.mean()
			.sort_values(ascending=False)
			)
poverty_per_state.plot(kind='barh')

# Find highest and lowest
highest_state = poverty_per_state.idxmax()
lowest_state = poverty_per_state.idxmin()

print("State with highest poverty rate:", highest_state)
print("State with lowest poverty rate:", lowest_state)

plt.xlabel("States")
plt.ylabel("Poverty Rate")
plt.title("Poverty Rate Per State in the US")

plt.show()


# Chart the High School Graduation Rate by US State
# Show the High School Graduation Rate in ascending order of US States.
# Which state has the lowest high school graduation rate?
# Which state has the highest?

completed_hs_per_state = (
			df_pct_completed_hs
			.groupby("Geographic Area")["percent_completed_hs"]
			.mean()
			.sort_values(ascending=True)
			)
completed_hs_per_state.plot(kind='barh')

# Find highest and lowest
highest_completion = completed_hs_per_state.idxmax()
lowest_completion = completed_hs_per_state.idxmin()

print("State with highest highschool completion rate:", highest_completion)
print("State with lowest highschool completion rate:", lowest_completion)

plt.xlabel("States")
plt.ylabel("Completion Rate")
plt.title("Highschool Completion Rate Per State in the US")

plt.show()

# Visualise the Relationship between Poverty Rates and High School Graduation Rates
# Create a line chart with two y-axes to show if the rations of poverty and high school graduation move together.
# Combine the two Series
comparison = pd.concat(
    [poverty_per_state, completed_hs_per_state],
    axis=1
).dropna()

# Create the plot
fig, ax1 = plt.subplots()

ax1.plot(
    comparison.index,
    comparison["poverty_rate"],
    label="Poverty Rate"
)

ax1.set_xlabel("States")
ax1.set_ylabel("Poverty Rate")

# Create second y-axis
ax2 = ax1.twinx()

ax2.plot(
    comparison.index,
    comparison["percent_completed_hs"],
    label="High School Completion Rate"
)

ax2.set_ylabel("High School Completion Rate")

plt.title("Poverty Rate vs High School Completion Rate by State")

plt.show()

# Now use a Seaborn .jointplot() with a Kernel Density Estimate (KDE) and/or scatter plot to visualise the same relationship
sns.jointplot(
    data=comparison,
    x="poverty_rate",
    y="percent_completed_hs",
    kind="scatter"
)

plt.show()

# Seaborn's .lmplot() or .regplot() to show a linear regression between the poverty ratio and the high school graduation ratio.
sns.regplot(
    data=comparison,
    x="poverty_rate",
    y="percent_completed_hs"
)

plt.xlabel("Poverty Rate")
plt.ylabel("High School Completion Rate")
plt.title("Poverty Rate vs High School Completion Rate")

plt.show()

# Create a Bar Chart with Subsections Showing the Racial Makeup of Each US State
# Visualise the share of the white, black, hispanic, asian and native american population in each US State using a bar chart with sub sections.
race_per_state = (
	df_share_race_city
    .groupby("Geographic area")[
        [
            "share_white",
            "share_black",
            "share_hispanic",
            "share_asian",
            "share_native_american"
        ]
    ]
    .mean()
)

race_per_state.plot(
    kind="bar",
    stacked=True,
    figsize=(15, 8)
)

plt.xlabel("States")
plt.ylabel("Population Share")
plt.title("Racial Makeup of Each US State")

plt.show()

# Create Donut Chart by of People Killed by Race
# Hint: Use .value_counts()
race_counts = df_fatalities["race"].value_counts()

plt.pie(
    race_counts,
    labels=race_counts.index,
    autopct="%1.1f%%",
    wedgeprops={"width": 0.4}
)

plt.title("People Killed by Race")
plt.show()

# Create a Chart Comparing the Total Number of Deaths of Men and Women
# Use df_fatalities to illustrate how many more men are killed compared to women.
deaths_per_gender = (df_fatalities["gender"].value_counts())
deaths_per_gender.plot(kind='bar')


plt.xlabel("Gender")
plt.ylabel("Total Number of Deaths")
plt.title("Total Number of Deaths by Gender in the US")

plt.show()

# Create a Box Plot Showing the Age and Manner of Death
# Break out the data by gender using df_fatalities. Is there a difference between men and women in the manner of death?
sns.boxplot(
    data=df_fatalities,
    x="manner_of_death",
    y="age",
    hue="gender"
)

plt.xlabel("Manner of Death")
plt.ylabel("Age")
plt.title("Age and Manner of Death by Gender")

plt.show()
# Is there a difference between men and women in the manner of death?

sns.countplot(
    data=df_fatalities,
    x="manner_of_death",
    hue="gender"
)

plt.xlabel("Manner of Death")
plt.ylabel("Number of Deaths")
plt.title("Manner of Death by Gender")

plt.show()

## Were People Armed?
# In what percentage of police killings were people armed?
# Create chart that show what kind of weapon (if any) the deceased was carrying.
# How many of the people killed by police were armed with guns versus unarmed?
print(df_fatalities["armed"].value_counts())
armed_count = (df_fatalities.loc[df_fatalities["armed"].notna(), "armed"] != "unarmed").sum()

total_count = df_fatalities["armed"].notna().sum()

armed_percentage = armed_count / total_count * 100

print(f"Percentage of people who were armed: {armed_percentage:.2f}%")

## How Old Were the People Killed?
# Work out what percentage of people killed were under 25 years old.
below_25 = (df_fatalities["age"] < 25).sum()
total_people = df_fatalities["age"].notna().sum()
percent_below_25 = (below_25 / total_people) * 100

print(f"The percentage of people killed under 25 years old is {percent_below_25:.2f}%")

# Create a histogram and KDE plot that shows the distribution of ages of the people killed by police.
sns.histplot(
    data=df_fatalities,
    x="age",
    kde=True
)

plt.xlabel("Age")
plt.ylabel("Number of People")
plt.title("Age Distribution of People Killed by Police")

plt.show()

# Create a seperate KDE plot for each race. Is there a difference between the distributions?
sns.kdeplot(
    data=df_fatalities,
    x="age",
    hue="race",
    common_norm=False
)

plt.xlabel("Race")
plt.ylabel("Density")
plt.title("Age Distribution of People Killed by Police by Race")

plt.show()

## Race of People Killed
# Create a chart that shows the total number of people killed by race.
death_per_race = (
			df_fatalities["race"].value_counts()
			)
death_per_race.plot(kind='bar')

plt.xlabel("Race")
plt.ylabel("Total Deaths")
plt.title("Total Deaths by race in the US")

plt.show()

## Mental Illness and Police Killings
# What percentage of people killed by police have been diagnosed with a mental illness?
mental_illness = df_fatalities["signs_of_mental_illness"].sum()
total_people = df_fatalities["signs_of_mental_illness"].notna().sum()
percent_mental_illness = (mental_illness / total_people) * 100

print(f"The percentage of people killed with mental illnesses was {percent_mental_illness:.2f}%")

## In Which Cities Do the Most Police Killings Take Place?
# Create a chart ranking the top 10 cities with the most police killings. Which cities are the most dangerous?
top10_cities = df_fatalities["city"].value_counts().head(10)

top10_cities.plot(kind="bar")

plt.xlabel("City")
plt.ylabel("Number of Police Killings")
plt.title("Top 10 Cities by Number of Police Killings")

plt.show()

## Rate of Death by Race
# Find the share of each race in the top 10 cities.
# Contrast this with the top 10 cities of police killings to work out the rate at which people are killed by race for each city.
top10_cities = df_fatalities["city"].value_counts().head(10).index
top10_data = df_fatalities[df_fatalities["city"].isin(top10_cities)]
race_counts = (
    top10_data
    .groupby("city")["race"]
    .value_counts()
    .unstack(fill_value=0)
)

race_rate = (
    race_counts
    .div(race_counts.sum(axis=1), axis=0)
    * 100
)

print(race_rate)
race_rate.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 8)
)

plt.xlabel("City")
plt.ylabel("Percentage of Police Killings")
plt.title("Rate of Police Killings by Race in the Top 10 Cities")
plt.legend(title="Race")

plt.show()

## Create a Choropleth Map of Police Killings by US State
# Which states are the most dangerous? Compare your map with your previous chart.
# Are these the same states with high degrees of poverty?

killings_by_state = (
    df_fatalities["state"]
    .value_counts()
    .reset_index()
)

killings_by_state.columns = ["State", "Killings"]

# Create choropleth map
fig = px.choropleth(
    killings_by_state,
    locations="State",
    color="Killings",
    locationmode="USA-states",
    scope="usa",
    color_continuous_scale="matter",
    title="Number of Police Killings by US State"
)

fig.show()

## Number of Police Killings Over Time
# Analyse the Number of Police Killings over Time. Is there a trend in the data?
# Convert date column to datetime
df_fatalities["date"] = pd.to_datetime(df_fatalities["date"])

# Count police killings by date
killings_over_time = (
    df_fatalities
    .groupby("date")
    .size()
)

# Plot the number of killings over time
killings_over_time.plot(
    kind="line",
    figsize=(12, 6)
)

plt.xlabel("Date")
plt.ylabel("Number of Police Killings")
plt.title("Number of Police Killings Over Time")

plt.show()