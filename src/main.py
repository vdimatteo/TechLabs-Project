import pandas as pd
import matplotlib.pyplot as plt

# csv into dataframe
data_confirmed = pd.read_csv("C:/Users/Andres/TechLabs-Project/data/time_series_covid19_confirmed_global.csv")
data_deaths = pd.read_csv("C:/Users/Andres/TechLabs-Project/data/time_series_covid19_deaths_global.csv")
data_recovered = pd.read_csv("C:/Users/Andres/TechLabs-Project/data/time_series_covid19_recovered_global.csv")

# "duplicates" wie Australia mit Provinces werden addiert
data_confirmed = data_confirmed.groupby("Country/Region").sum()

# Lat und Long deleted
del data_confirmed['Lat']
del data_confirmed['Long']

# Beispielsland zum Plotten
country = 'Colombia'
df_country = data_confirmed.loc[country]

df_country.plot(x='time', y='confirmed', kind='line')

plt.show()
