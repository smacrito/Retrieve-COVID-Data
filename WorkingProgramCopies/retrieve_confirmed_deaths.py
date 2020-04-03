import csv#csv reader
import pandas as pd#csv parser
import collections#not needed
import requests#retrieves URL fom gov data
import glob

def getFile():
    #repo for covid data
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
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
    data.drop(['UID','iso2','iso3','code3','FIPS','Country_Region','Lat','Long_','Combined_Key'],axis=1,inplace=True)

      
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
        g[pd.date_range('03/23/2020', '04/02/20')] \
            .to_csv('{0}_confirmed_cases.csv'.format(name))
    print('confirmed_cases has been created in this directory')

def Main():
    print('Started program...')
    createCSV()
    removeCols()

def removeCols():#glob is a native library. searches for all csvs
    #for file in csvs
    for filename in glob.glob('*.csv'):
        #set file to dataframe
        data = pd.read_csv(filename, delimiter = ',')
        #drop state,county columns. Axis=1 means top column, inplace=True replaces
        #the value directly in cell
        data.drop(['Province_State'],axis=1,inplace=True)
        data.rename(columns={'Admin2':'County'},inplace=True)
        

        #helps know program is working. Prints count of columns 
        print(data.index.max)
        print(data.columns)

        #set columnCount = total # of columns
        columnCount = len(data.columns)
        #init count for loop
        count = 0
        print(columnCount)

        #Specify row number to replace (starting after header).Row=0 is first row
        row_number = 0

        #create blank list to append datatypes to
        row_value = ['string']

        #append data type for each column
        while count < columnCount-1:
            count+=1
            row_value.append('number')
            print(row_value)

        #checks if row is in data
        if row_number > data.index.max()+1: 
            print("Invalid row_number")
        #call insert_row to split by row, append, and stitch
        else:
            
            data = insert_row(row_number, data, row_value) 
            print(data)
            data.to_csv('reformat_cases_{0}.csv'.format(filename), index=False)

def insert_row(row_number,data,row_value):
    #splits dataframe in half by row number
    #allows appending to original data frame then stitching back together
    #dont mess with this part!
    
    start_upper = 0
    
    end_upper = row_number
    
    start_lower = row_number
    
    end_lower = data.shape[0]
    
    upper_half = [*range(start_upper, end_upper, 1)]
    
    lower_half = [*range(start_lower, end_lower, 1)]
    
    lower_half = [x.__add__(1) for x in lower_half]
    
    index_ = upper_half + lower_half
    
    data.index = index_
    
    data.loc[row_number] = row_value
    
    data = data.sort_index()
    
    return data


if __name__ == "__main__":
    Main()

    
