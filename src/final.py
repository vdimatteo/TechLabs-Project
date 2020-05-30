import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import matplotlib.dates as mdates

df = pd.read_csv("../data/time_series_covid19_confirmed_global.csv")
df2 = pd.read_csv("../data/time_series_covid19_deaths_global.csv")
df3 = pd.read_csv("../data/time_series_covid19_recovered_global.csv")
population_df = pd.read_csv("../data/Population.csv")

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
# pop_df.info()

# Lat, Long in allen Droppen
df.drop(['Lat', 'Long'], axis=1, inplace=True)
df2.drop(['Lat', 'Long'], axis=1, inplace=True)
df3.drop(['Lat', 'Long'], axis=1, inplace=True)

# Provinzen raus
countries = df.groupby("Country/Region").sum()
countries2 = df2.groupby("Country/Region").sum()
countries3 = df3.groupby("Country/Region").sum()

# Transform Row/Columns
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

# skalierung
for country in recovered_scaled.columns:
    recovered_scaled[country] = recovered_scaled[country] / pop_df.loc[country].values * 100000

for country in recovered_scaled.columns:
    death_scaled[country] = death_scaled[country] / pop_df.loc[country].values * 100000

for country in recovered_scaled.columns:
    confirmed_scaled[country] = confirmed_scaled[country] / pop_df.loc[country].values * 100000

# Versuch Wachstumsrate
conf = confirmed.copy()
confs = conf.shift(1)
Change = conf - confs

week = Change.copy()
# Resample auf Woche
weekly = week.resample('W').sum()

# Versuch Todesrate --> Todesrate = Tote/Infizierte*100
deathrate = (death / confirmed) * 100

# aktuell Infizierte
infected = confirmed - recovered - death
active = confirmed - recovered - death


# hier kommt Stefans Teil
def plot_by_population():
    countries=["Germany","China","US","Italy","Sweden"]
    dateFmt=mdates.DateFormatter("%d.%m.20")
    fix,(ax1,ax2)=plt.subplots(2,1,sharex=True)



    #confirmed cases
    ax1.plot(confirmed_scaled[countries])
    ax1.set_title("Confirmed cases per 100.000 inhabitants")
    ax1.legend(countries)




    #confirmed deaths
    ax2.plot(death_scaled[countries])
    ax2.set_title("Deaths per 100.000 inhabitants")
    ax2.legend(countries)
    ax2.xaxis.set_major_formatter(dateFmt)
    _ =plt.xticks(rotation=60)


    plt.show()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


##PLOT doubled time

def plot_double_selected(Selected_countries):
    lw_inc = weekly.loc['2020-05-17']
    lw_conf = confirmed.loc['2020-05-17']
    lw_double = lw_conf / lw_inc

    lw_double_filtered = lw_double[lw_double.index.isin(Selected_countries)]
    lw_double_filtered.plot.bar(x=lw_double_filtered.index, y=lw_double_filtered.array, legend=False, figsize=(15, 7.5),
                                fontsize="x-large", capsize=4)

    plt.axhline(y=1, linestyle='--')
    plt.axhline(y=3, linestyle='--')
    plt.axhline(y=5, linestyle='--')
    plt.xlabel('Countries', fontsize="x-large")
    plt.ylabel('Doubling Time (Weeks)', fontsize="x-large")
    plt.title('Doubling Time in Weeks as of 2020-05-17. Selected countries', fontsize="x-large")
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_overall_dev():
    print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
    country = input("Please enter country : ")
    confirmed[country].plot()
    recovered[country].plot()
    death[country].plot()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_weekly():
    print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
    country = input("Please enter country : ")
    weekly[country].plot()
    Change[country].plot()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_death_rate(countries):
    deathrate.plot(y=countries)
    plt.show()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_stacked():
    print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
    country = input("Please enter country : ")


    confirmed1 = confirmed[country].values.tolist()
    recovered1 = recovered[country].values.tolist()
    deaths1 = death[country].values.tolist()
    active1 = active[country].values.tolist()
    dates1 = confirmed.index.tolist()
    rng = pd.date_range(start="01/22/2020", periods=122, freq="D")

    plt.figure(figsize=(15, 7.5))
    labels = ["active", "recovered", "deaths"]
    plt.stackplot(rng, active1, recovered1, deaths1, baseline='zero', labels=labels)

    plt.title(country)
    plt.xlabel("Date")
    plt.ylabel("Total number of")
    plt.legend(loc="upper left")
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_conf_dev():
    print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
    country = input("Please enter country : ")
    confirmed[country].plot()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_conf_dev_all():
    confirmed.plot(legend=None)
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()

def plot_act_dev():
    print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
    country = input("Please enter country : ")
    active[country].plot()
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


def plot_act_dev_all():
    active.plot(legend=None)
    print("Press any key to close plot...")
    plt.waitforbuttonpress(0)
    plt.close()


ans = True
while ans:
    print("""
    Main Menu
    1. Overall Development
    2. Development of confirmed cases
    3. Development of active cases
    4. Daily/weekly growth rates
    5. Death Rates 
    6. Doubling time of infected cases
    7. Confirmed & death cases scaled By population from preselected countries
    8. Exit
    """)
    ans = input("Please select an option: ")
    if ans == "1":
        print("""
            1. Line Diagram
            2. Stacked Diagram
            """)
        ans1 = input("Choose an option: ")
        if ans1 == "1":
            plot_overall_dev()
        else:
            plot_stacked()
    elif ans == "2":
        print("""
        1. Confirmed cases in all countries
        2. Confirmed cases in a selected country 
        """)
        ans2 = input("Choose an option: ")
        if ans2 == "1":
            plot_conf_dev_all()
        else:
            plot_conf_dev()
    elif ans == "3":
        print("""
        1. Active cases in all countries
        2. Active cases in a selected country 
        """)
        ans3 = input("Choose an option: ")
        if ans3 == "1":
            plot_act_dev_all()
        else:
            plot_act_dev()
    elif ans == "4":
        plot_weekly()
    elif ans == "5":
        print("\n Death rates between 5 contries (Case sensitive) : \n")
        print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
        con1 = input("Enter country #1: ")
        con2 = input("Enter country #2: ")
        con3 = input("Enter country #3: ")
        con4 = input("Enter country #4: ")
        con5 = input("Enter country #5: ")
        countries = [con1, con2, con3, con4, con5]
        plot_death_rate(countries)
    elif ans == "6":
        print("\n Doubling time of infected cases between 5 contries: \n")
        print("\n Enter Countries with the first as a capital letter , e.g Germany : \n")
        con1 = input("Enter country #1: ")
        con2 = input("Enter country #2: ")
        con3 = input("Enter country #3: ")
        con4 = input("Enter country #4: ")
        con5 = input("Enter country #5: ")
        countries = [con1, con2, con3, con4, con5]
        plot_double_selected(countries)
    elif ans == "7":
        plot_by_population()
    elif ans == "8":
        break
    else:
        print("\n Not Valid Choice Try again")

    input("Press Enter to return to main menu...")
    print("\n" * 100)
