import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("time_series_covid19_confirmed_global.csv")
df2 = pd.read_csv("time_series_covid19_deaths_global.csv")
df3 = pd.read_csv("time_series_covid19_recovered_global.csv")
population_df = pd.read_csv("Population.csv")

pop2020_df = population_df[(population_df["Time"] == 2020)
                           & (population_df["Variant"] == "Medium")
                           & (population_df["LocID"] <= 894)]

# relevante spalten und länder als index
pop_df = pop2020_df[["Location", "PopTotal"]].set_index("Location")

# poptotal *1000
pop_df["PopTotal"] = pop_df["PopTotal"] * 1000

# korrektur Ländernamen
index_list = pop_df.index.tolist()
wrong_names = ["Bolivia (Plurinational State of)", "Brunei Darussalam", "Myanmar", "Democratic Republic of the Congo",
               "Congo",
               "Côte d'Ivoire", "Iran (Islamic Republic of)", "Republic of Korea", "Lao People's Democratic Republic",
               "Republic of Moldova", "Russian Federation", "Syrian Arab Republic", "China, Taiwan Province of China",
               "United Republic of Tanzania", "United States of America", "Venezuela (Bolivarian Republic of)",
               "Viet Nam",
               "State of Palestine"]

right_names = ["Bolivia", "Brunei", "Burma", "Congo (Kinshasa)", "Congo (Brazzaville)", "Cote d'Ivoire", "Iran",
               "Korea, South",
               "Laos", "Moldova", "Russia", "Syria", "Taiwan*", "Tanzania", "US", "Venezuela", "Vietnam",
               "West Bank and Gaza"]

for wrong, right in zip(wrong_names, right_names):
    idx = index_list.index(wrong)
    index_list[idx] = right

pop_df.index = index_list
# fertiger df mit Bevölkerungszahlen aller Länder in 2020
#pop_df.info()

#Lat, Long in allen Droppen
df.drop(['Lat', 'Long'],axis=1, inplace=True)
df2.drop(['Lat', 'Long'],axis=1, inplace=True)
df3.drop(['Lat', 'Long'],axis=1, inplace=True)

#Provinzen raus
countries = df.groupby("Country/Region").sum()
countries2 = df2.groupby("Country/Region").sum()
countries3 = df3.groupby("Country/Region").sum()

#Transform Row/Columns
confirmed = countries.T
death = countries2.T
recovered = countries3.T

# DateTimeIndex setzen
confirmed.index = pd.DatetimeIndex(confirmed.index, name='Date', freq='D')
death.index = pd.DatetimeIndex(death.index, name='Date', freq='D')
recovered.index = pd.DatetimeIndex(recovered.index, name='Date', freq='D')

# kopien der unskalierten daten
recovered_scaled = recovered.copy()
death_scaled = death.copy()
confirmed_scaled = confirmed.copy()

# fehlende Daten bzw Kreuzfahrtschiffe löschen
recovered_scaled.drop(columns=["Diamond Princess", "Kosovo", "MS Zaandam"], inplace=True)
death_scaled.drop(columns=["Diamond Princess", "Kosovo", "MS Zaandam"], inplace=True)
confirmed_scaled.drop(columns=["Diamond Princess", "Kosovo", "MS Zaandam"], inplace=True)

# print(recovered_scaled["US"])
# print(pop_df.loc["US"])
# print(recovered_scaled["US"] / (pop_df.loc["US"].values))

# skalierung
for country in recovered_scaled.columns:
    recovered_scaled[country] = recovered_scaled[country] / pop_df.loc[country].values * 100000

for country in recovered_scaled.columns:
    death_scaled[country] = death_scaled[country] / pop_df.loc[country].values * 100000

for country in recovered_scaled.columns:
    confirmed_scaled[country] = confirmed_scaled[country] / pop_df.loc[country].values * 10000






#Versuch Wachstumsrate
conf = confirmed.copy()
confs = conf.shift(1)
Change = conf - confs

week = Change.copy()
#Resample auf Woche
weekly =week.resample('W').sum()

#Versuch Todesrate --> Todesrate = Tote/Infizierte*100
deathrate = (death/confirmed)*100

#aktuell Infizierte
infected = confirmed - recovered - death


#Doubling time in weeks based on recent week; data confirmed
#where is covid-19 pandemic still in increasing mode
lw_inc = weekly.loc['2020-05-17']
lw_conf = confirmed.loc['2020-05-17']
lw_double = lw_conf / lw_inc

lw_double_all = lw_double[lw_double < 5]

Selected_countries = ["Germany", "United Kingdom", 'Rusia', 'France', 'Italy', 'Spain', 'US']
lw_double_filtered = lw_double[lw_double.index.isin(Selected_countries)]

###PLOT

# lw_double_filtered.plot.bar(x=lw_double_filtered.index, y=lw_double_filtered.array, legend=False, figsize=(15, 7.5),
#                             fontsize="x-large", capsize=4)
# lw_double_all.plot.bar(x = lw_double_all.index, y = lw_double_all.array, legend=False, figsize=(15, 7.5),
#                        fontsize="x-large", capsize=4)
# plt.axhline(y=1, linestyle='--')
# plt.axhline(y=3, linestyle='--')
# plt.axhline(y=5, linestyle='--')
# plt.xlabel('Countries', fontsize="x-large")
# plt.ylabel('Doubling Time (Weeks)', fontsize="x-large")
# plt.title('Doubling Time in Weeks as of 2020-05-17. Selected countries with <5 weeks ', fontsize="x-large")
# plt.show()

#
# choose = input ("Please enter country : ")
#
# confirmed[country].plot()
# recovered[country].plot()
# death[country].plot()
#
# weekly['United Kingdom'].plot()
# Change['United Kingdom'].plot()
#
# deathrate.plot(y=['Germany', 'Italy', 'Spain', 'US', 'United Kingdom', 'Russia'])
# plt.show()


####LENA

country = input("Please enter country : ")

active = confirmed - recovered - death

confirmed1 = []
recovered1 = []
deaths1 = []
active1 = []
dates1 = []

confirmed1 = confirmed[country].values.tolist()
recovered1 = recovered[country].values.tolist()
deaths1 = death[country].values.tolist()
active1 = active[country].values.tolist()
dates1 = confirmed.index.tolist()
rng = pd.date_range(start="01/22/2020", periods=122, freq="D")

#####PLOT

plt.figure(figsize=(15, 7.5))
labels = ["active", "recovered", "deaths"]
# plt.bar(rng, active1, label = "active")
# plt.bar(rng, recovered1, label = "recovered", bottom = active1)
# plt.bar(rng, deaths1, label = "deaths", bottom = active1)

plt.stackplot(rng, confirmed1, recovered1, deaths1, baseline='zero', labels=labels)

plt.title(country)
plt.xlabel("Date")
plt.ylabel("Total number of")
plt.legend(loc="upper left")
plt.show()