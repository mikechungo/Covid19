
from flask import Flask, render_template, url_for
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

#Getting timeseries data for confirmed cases
from matplotlib import ticker

url_confirmed='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_recovered='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
url_deaths='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

df_Confirmed=pd.read_csv(url_confirmed,error_bad_lines=False)
df_Recovered=pd.read_csv(url_recovered,error_bad_lines=False)
df_Deaths=pd.read_csv(url_deaths,error_bad_lines=False)

#creating a column to show that this is confirmed cases only
df_Confirmed['Status']='Confirmed'
df_Recovered['Status']='Recovered'
df_Deaths['Status']='Dead'

number_of_unique_countries=len((df_Confirmed['Country/Region'].unique()))
countries_list=(df_Confirmed['Country/Region'].unique()).tolist()

app = Flask(__name__)

@app.route("/")
@app.route("/current")
def Current_World_Status():
    pass


@app.route("/home")
def about():
    numb_of_columns = (len(df_Confirmed.columns))
    latest_column = df_Confirmed.columns[numb_of_columns - 2]

    today_confirmed = ((df_Confirmed.groupby(['Country/Region'])[latest_column].agg('sum')).to_frame()).sort_values(
        by=latest_column, ascending=False)
    today_confirmed = today_confirmed.reset_index()
    top_50_confirmed = today_confirmed[:50]

    t50p = top_50_confirmed.plot(kind='bar', x='Country/Region', y=latest_column, color='green', figsize=(20, 10),
                                 legend=False,zorder=2)

    t50p.yaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
    print(type(t50p))
    t50p.set_ylabel("Cornfirmed Cases")
    t50p.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    t50p.set_xlabel("Countries")
    t50p.figure.savefig('static/images/chart.png')




#def Confirmed_trend():
    plotting_dates = list(df_Confirmed[40:len(df_Confirmed) - 1])
    dates_to_plot = plotting_dates[4:len(plotting_dates) - 1]

    masterdf = pd.concat([df_Confirmed, df_Recovered, df_Deaths])

    df_Confirmed_agg = df_Confirmed.groupby(['Country/Region']).agg('sum')
    df_Confirmed_agg = df_Confirmed_agg.reset_index()
    df_Recovered_agg = df_Recovered.groupby(['Country/Region']).agg('sum')
    df_Recovered_agg = df_Recovered_agg.reset_index()
    df_Deaths_agg = df_Deaths.groupby(['Country/Region']).agg('sum')
    df_Deaths_agg = df_Deaths_agg.reset_index()

    plotting_values = df_Confirmed[40:len(df_Confirmed) - 1]

    # Setting the indexs to filter on the columns
    df_Confirmed_agg.set_index('Country/Region', inplace=True)
    df_Recovered_agg.set_index('Country/Region', inplace=True)
    df_Deaths_agg.set_index('Country/Region', inplace=True)

    # print(df_Confirmed.loc['Austria'])

    country = 'Russia'

    confirmed_df = df_Confirmed_agg.loc[country].values.tolist()
    confirmed_df_plot = confirmed_df[2:]

    recovered_df = df_Recovered_agg.loc[country].values.tolist()
    recovered_df_plot = recovered_df[2:]

    Death_df = df_Deaths_agg.loc[country].values.tolist()
    Death_df_plot = Death_df[2:]

    # Creating one dataframe for Mortality/Dead and Confirmed

    # First to find the mortality rate
    a = np.array(confirmed_df_plot)
    b = np.array(Death_df_plot)

    mortality_rate = list(b / a)

    Top_50_df = pd.DataFrame({
        'Dates': dates_to_plot,
        'Confirmed': confirmed_df_plot,
        'Recovered': recovered_df_plot,
        'Dead': Death_df_plot,
        'Mortality Rate': mortality_rate
    })

    print(Top_50_df.head())

    top_50_plt = Top_50_df.plot(kind='line', x='Dates', y=['Confirmed', 'Recovered', 'Dead'], figsize=(10, 5),
                                title=country + ' Summary')
    top_50_plt.set_ylabel('People')
    top_50_plt.set_xlabel('Dates [mm/dd/yyyy]')

    top_50_plt = Top_50_df.plot(kind='line', x='Dates', y=['Mortality Rate'], figsize=(10, 5),
                                title=country + ' Mortality Rate')
    top_50_plt.set_ylabel('Mortality Rate')
    top_50_plt.set_xlabel('Dates [mm/dd/yyyy]')

    top_50_plt.figure.savefig('static/images/chart_top50.png')
    #return render_template('home.html', confirmed='/static/images/confirmed.png')

    return render_template('home.html', url='/static/images/chart.png',confirmed='/static/images/chart_top50.png')

if __name__ == '__main__':
    app.run()