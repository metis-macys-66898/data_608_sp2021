#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 00:31:11 2021

@author: dpong
"""


#import libraries
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np

import requests

import json
from pandas import json_normalize 
import datetime as dt
from datetime import date
# import pytz
from dateutil.parser import parse
# !pip install maya
import maya

# from contextlib import suppress
from scipy import stats

from annotated_text import annotated_text, annotation


#Introduction (main section)
st.write("""
# The Effect of Pandemic on the selling price and rent for 1-bedroom condo or apartment.
## Introduction
Background info: As we're entering a era of remote working, and with the interest rates near historic lows, there are many buyers for single family homes everywhere from 
East Bay of SF Bay Area to Sacramento, CA to some small towns in Colorado and Arizona. I've got a 1-bedroom/1-bathroom condo that I really wanted to sell but unfortunately 
the demand has been dropping due to the pandemic and prices have been driven down. We tried to look at Sold Price and Sq-footage price Pre-pandemic to try to make some 
comparisons with what we see since Mar 18 2020, the official stay-at-home date for CA. In additions, we tried to also look for 1-bed/1-bath rental market for both condos
and apartments in the area and see we can also see the same declining trend in terms of demand and price.
""")

#Instructions (sidebar)
st.sidebar.write("""
### Instructions
In this sidebar(panel), you can enter your desired selling price and determine what's the percentile it is for 1-bed/1-ba condos at the zip code level or at the county level.
""")

#Image (sidebar)
# st.sidebar.image('https://github.com/metis-macys-66898/data_608_sp2021/blob/main/zip_code_map_sidebar_top_graphic.png')

#Image (for Reference of the Zip Code Map)
# st.image('https://github.com/metis-macys-66898/data_608_sp2021/blob/main/zip_code_map.png')

chart1 = st.empty()
chart2 = st.empty()
chart3 = st.empty()
chart4 = st.empty()

with chart1.beta_container():
#Price change
    st.write("Price change of 1bd/1ba condos across SF Bay Area by zip code")
    components.iframe("https://rawcdn.githack.com/metis-macys-66898/data_608_sp2021/a0f7f9a72271150c563b0f86465c4ae80a4b6337/price_change_map.html", height = 301, scrolling = True)

with chart2.beta_container():
#Sq Footage Price Change
    st.write("Square footage price change of 1bd/1ba condos across SF Bay Area by zip code")
    components.iframe("https://rawcdn.githack.com/metis-macys-66898/data_608_sp2021/a0f7f9a72271150c563b0f86465c4ae80a4b6337/sq_footage_price_change_map.html", height = 301, scrolling = True)

with chart3.beta_container():
#Price Change in Rent
    st.write("Price change in rent of 1bd/1ba condos across SF Bay Area by zip code")
    components.iframe("https://rawcdn.githack.com/metis-macys-66898/data_608_sp2021/a0f7f9a72271150c563b0f86465c4ae80a4b6337/price_change_in_rent_map.html", height = 301, scrolling = True)


with chart4.beta_container():
#Price Change in Rent per sq footage 

    st.write("Price change in rent per sq ft of 1bd/1ba condos across SF Bay Area by zip code")
    components.iframe("https://rawcdn.githack.com/metis-macys-66898/data_608_sp2021/a0f7f9a72271150c563b0f86465c4ae80a4b6337/price_change_in_rent_per_sqft_map.html", height = 301, scrolling = True)
    

# Using Requests to get each of the pandemic datasets Using realty-mole-api

#95054 
url = "https://realty-mole-property-api.p.rapidapi.com/salePrice"

querystring = {"compCount":"10","squareFootage":"870","bathrooms":"1","address":"1883 Agnew Rd Unit 318, Santa Clara, CA","bedrooms":"1","propertyType":"Condo"}

headers = {
    'x-rapidapi-key': "ca0f4a0c63msheb56ce445093e55p1d9232jsn4658d02eedac",
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
print(response.json())
sale_estimate_pdf = json_normalize(response.json())
# sale_estimate_pdf.head

#95110

querystring = {"compCount":"10","bathrooms":"1","address":"175 W St James St, San Jose, CA","bedrooms":"1","propertyType":"Condo"}

response1 = requests.request("GET", url, headers=headers, params=querystring)

print(response1.text)
sale_estimate_pdf_1 = json_normalize(response1.json())
# sale_estimate_pdf_1.head()

#94085

querystring = {"compCount":"10","bathrooms":"1","address":"612 Arcadia Ter #102 SUNNYVALE, CA","bedrooms":"1","propertyType":"Condo"}

response2 = requests.request("GET", url, headers=headers, params=querystring)

print(response2.text)
sale_estimate_pdf_2 = json_normalize(response2.json())
# sale_estimate_pdf_2.head()


#  95051

querystring = {"compCount":"10","bathrooms":"1","address":"150 Saratoga Ave #318 SANTA CLARA, CA","bedrooms":"1","propertyType":"Condo"}

response3 = requests.request("GET", url, headers=headers, params=querystring)

print(response3.text)
sale_estimate_pdf_3 = json_normalize(response3.json())
# sale_estimate_pdf_3.head()

#  94086

querystring = {"compCount":"10","bathrooms":"1","address":"420 E Evelyn Ave Unit Z102 SUNNYVALE, CA","bedrooms":"1","propertyType":"Condo"}

response4 = requests.request("GET", url, headers=headers, params=querystring)

print(response4.text)

sale_estimate_pdf_4 = json_normalize(response4.json())
# sale_estimate_pdf_4.head()

#  94087

querystring = {"compCount":"10","bathrooms":"1","address":"880 E Fremont Ave #304, SUNNYVALE, CA","bedrooms":"1","propertyType":"Condo"}

response5 = requests.request("GET", url, headers=headers, params=querystring)

print(response5.text)
sale_estimate_pdf_5 = json_normalize(response5.json())
# sale_estimate_pdf_5.head()

# Combining the 6 dataframes into one
sale_estimate_pdfs = pd.concat([sale_estimate_pdf, sale_estimate_pdf_1, sale_estimate_pdf_2, sale_estimate_pdf_3, sale_estimate_pdf_4, sale_estimate_pdf_5], ignore_index=True)
# sale_estimate_pdfs


class DatetimeRange:
    def __init__(self, dt1, dt2):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        return self._dt1 <= dt <= self._dt2

# Define CA Pandemic Period

pandemic_dt1 = dt.date(2020, 3, 18)
pandemic_dt2 = date.today()

print(pandemic_dt1)
print(pandemic_dt2)


# construct a data zip that can be summarized at zip code level. Restrict to all transactions since Mar 18, 2020

columns = ['publishedDate', 'price', 'squareFootage', 'sq_Footage_price', 'zipcode']
main_df = pd.DataFrame(columns=columns)
counter = 0
for k in range(len(sale_estimate_pdfs.listings)):
    for i in range(len(sale_estimate_pdfs.listings[k])):
        publishedDate = maya.parse(sale_estimate_pdfs.listings[k][i]['publishedDate']).datetime(to_timezone='America/Los_Angeles', naive=False)
    #     print(publishedDate.date())
        if publishedDate.date() in DatetimeRange(pandemic_dt1, pandemic_dt2):
            print(counter)
            main_df.loc[counter, 'publishedDate'] = publishedDate.date()
            print(publishedDate.date())
            main_df.loc[counter, 'price'] = sale_estimate_pdfs.listings[k][i]['price']
            print( sale_estimate_pdfs.listings[k][i]['price'])
            main_df.loc[counter, 'squareFootage'] =  sale_estimate_pdfs.listings[k][i]['squareFootage']
            print(sale_estimate_pdfs.listings[k][i]['squareFootage'])
            main_df.loc[counter, 'sq_Footage_price'] =  round(sale_estimate_pdfs.listings[k][i]['price'] / sale_estimate_pdfs.listings[k][i]['squareFootage'],0)
            print(round(sale_estimate_pdfs.listings[k][i]['price'] / sale_estimate_pdfs.listings[k][i]['squareFootage'],0))
            main_df.loc[counter, 'zipcode'] =  sale_estimate_pdfs.listings[k][i]['zipcode']
            print(sale_estimate_pdfs.listings[k][i]['zipcode'])
            counter+=1
            
# main_df            
main_df.price = main_df.fillna(0).price.astype(int)
main_df.squareFootage =  main_df.fillna(0).squareFootage.astype(int)
main_df.sq_Footage_price = main_df.fillna(0).sq_Footage_price.astype(float)


# Pre-pandemic dataset (Source: Self_Created_DB.csv)
filename = "https://raw.githubusercontent.com/metis-macys-66898/data_608_sp2021/main/Self_Created_DB.csv"
cols = list(pd.read_csv(filename, nrows =1))

self_created_db = pd.read_csv(filename, usecols =[i for i in cols if i != 'Index'])

# self_created_db

# main_df2
main_df2 = self_created_db.loc[self_created_db['Is it 1-bed/1-bath']=='Y' , ['Address','Price / sq ft', 'Sold Price',  'Sold Price Pre-Pandemic']]

main_df2['zipcode'] = main_df2['Address'].str[-5:]
# dropping Address
main_df2.drop('Address', inplace=True, axis=1)

# price / sq ft needs to be changed to float
main_df2[main_df2.columns[0,]] = main_df2[main_df2.columns[0,]].replace('[\$,]', '', regex=True).astype(float)


main_df2['Sold Price Pre-Pandemic'] = main_df2['Sold Price Pre-Pandemic'].fillna(0)
main_df2['Sold Price'] = main_df2['Sold Price'].fillna(0)

main_df2['Sold Price'] = main_df2.apply(lambda x: x[1] if x[2] == 0 else x[2], axis = 1)

main_df2[main_df2.columns[1:3,]] = main_df2[main_df2.columns[1:3,]].replace('[\$,]', '', regex=True).astype(float)

main_df2.drop('Sold Price Pre-Pandemic', inplace=True, axis=1)

# Creating a final dataset for calculting sq footage price percentile (final calculator) by zip code

final_2 = main_df2[['zipcode','Price / sq ft']]
final_2.columns = ['zipcode', 'sq_Footage_price']
final_df = pd.concat([main_df[['zipcode','sq_Footage_price']], final_2], ignore_index=True)
# final_df


            
#-------------------------------------------------Final Calculator     -----------------------------------------------#

def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

def percentile(n):
    def percentile_(x):
        return proper_round(np.percentile(x, n),2)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

h_rule = "<HR WIDTH="71%" SIZE="8" NOSHADE>"
st.markdown(h_rule) 


# Enter your desired percentile n
# For example, n = 89 means 89th percentile

st.sidebar.write('Enter your desired percentile(n)')
n = st.sidebar.number_input(label="If you want to get the desired selling price of your 1-bed/1-bath condo, you can enter the desired percentile:", min_value=0, max_value=100)
if 0 <= n <= 100:
    st.sidebar.write('You entered:', n, '-th percentile')
    # At zip code level, what's the sq footage price for each
    final_results = final_df.groupby('zipcode').agg({'sq_Footage_price': percentile(n)})
    # final_df
    st.write("At zip code level, here are the square footage prices at ", n, "-th percentile", final_results)
    
    # At santa clara county level, what's the sq footage price for each
    santa_clara_county_level = final_df.reset_index().drop('zipcode', axis = 1).agg(percentile(n)).to_frame()[1:]
    santa_clara_county_level.columns = ['Santa_Clara_County']
    # santa_clara_county_level
    st.write("At the county level, here are the square footage prices at ", n, "-th percentile", santa_clara_county_level)
    
else:
    st.sidebar.write('Improper entry, please try again with a number between 0 and 100.')


h_rule = "<HR WIDTH="71%" SIZE="8" NOSHADE>"
st.markdown(h_rule) 


# Enter your desired selling sq footage price. We'll calculate the percentile for you, i.e. how it measures against cumulative historical sold prices and listed prices of current listings
st.sidebar.write('Enter your desired selling sq footage price(p)')
p = st.sidebar.number_input("We'll calculate the percentile for you, i.e. how it measures against cumulative historical sold prices and listed prices of current listings:", min_value = 0)

if 0 <= p:
    st.sidebar.write('You entered $', p, ' as your desired selling sq. footage price')
    # county level 
    percentile = int(proper_round(stats.percentileofscore(final_df['sq_Footage_price'], p)))
    st.write(annotated_text('Based on your desired selling square footage price ', p, ' , we found that it measured at ', percentile, '-th percentile against cumulative historical sold \
                            prices and  \n listed prices of current listings at the county level')
            )
    
else:
    st.sidebar.write('Improper entry, please try again with a number greater than or equal to 0.')





#-------------------------------------------------Citations-----------------------------------------------#

#Cite myself as author
st.sidebar.markdown(' ')
st.sidebar.markdown('......................................................')
st.sidebar.markdown("*This app was built by Dennis Pong using Python and Streamlit.*")

#Cite data and academic motivational sources
st.markdown(' ')
st.markdown('.............................................................................................')
st.write("""
## References
https://towardsdatascience.com/visualizing-data-at-the-zip-code-level-with-folium-d07ac983db20
https://docs.streamlit.io/en/stable/develop_streamlit_components.html#render-an-html-string
https://docs.streamlit.io/en/stable/deploy_streamlit_app.html#python-dependencies
https://github.com/Jcharis/streamlit-trend-app
"""
)


