import csv#csv reader
import pandas as pd#csv parser
import collections#not needed
import requests#retrieves URL fom gov data


def getFile():
    #repo for covid data
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    #load data
    response = requests.get(url)
    print('Writing file...')
    open('us_confirmed.csv','wb').write(response.content)
    
#takes raw data from link. creates CSV for each unique state and removes unneeded headings
#add or remove headings as you wish, adding lat and long may break it, since i am using a combined key to allow for the date range. Adding a new column may break it
#new feature for near future
def createCSV():
    print("us_confirmed.csv (base file) created!")
    getFile()
    #init data
    data=pd.read_csv('us_confirmed.csv', delimiter = ',')
    #drop extra columns
    data.drop(['UID'],axis=1,inplace=True)
    data.drop(['iso2'],axis=1,inplace=True)
    data.drop(['iso3'],axis=1,inplace=True)
    data.drop(['code3'],axis=1,inplace=True)
    data.drop(['FIPS'],axis=1,inplace=True)
    data.drop(['Country_Region'],axis=1,inplace=True)
    data.drop(['Lat'],axis=1,inplace=True)
    data.drop(['Long_'],axis=1,inplace=True)
    data.drop(['Combined_Key'],axis=1,inplace=True)
    #remove debug data later
    data.to_csv('DEBUGDATA.csv')
      
    #print all coluns being written to ensure correct function -- WILL INCLUDe ALL DATES
    for col in data.columns:
        print(col)
        
    print('Above dates are a live view of available dates from data dump')
    
    #group by Province_State (state) and Admin2 (county) as a MultiIndex (combined key)
    data = data.set_index((['Province_State','Admin2']))
    
    #parse all but first two columns as date time to be renamed, so pandas can recognize for date ranges
    data = data.iloc[:,3:].rename(columns=pd.to_datetime, errors='ignore')
    
    #create and name files within selected date range
    for name, g in data.groupby(level='Province_State'):
        g[pd.date_range('03/23/2020', '03/30/20')] \
            .to_csv('{0}_confirmed_cases.csv'.format(name))
    print('confirmed_cases has been created in this directory')

def Main():
    print('Started program...')
    createCSV()

if __name__ == "__main__":
    Main()

    
