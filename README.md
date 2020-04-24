
# README

### COVID-19 Data Retriever

## About
 - This program is built for the purpose of retrieving the date specified for the United States confirmed cases and deaths for COVID-19
 - It takes the most recent data dump from [confirmed](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv) and [deaths](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv) and creates CSV's for each state's data, with the headers of state, county, and dates you've selected

## Instructions
#### Required Dependencies

 - csv
 - pandas
 - collections
 - requests
 - glob

**Example**

    pip install pandas
	pip install requests

**To Run Program**

 - Double click the either *retrieve_confirmed_cases.py* or *retrieve_confirmed_deaths.py* 
 - This will retrieve from 03/23/2020 - 04/02/2020 from the range.

**Changing the Date Range**

 - Edit the corresponding file you are trying to run with a text editor
 - replace `g[pd.date_range('03/23/2020', '03/30/20')]` in `createCSV()` to the date range you prefer, following the respective format

## References
https://stackoverflow.com/questions/60961580/pandas-not-displaying-all-columns-when-writing-to?noredirect=1#comment107853739_60961580
