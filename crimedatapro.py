#!/usr/bin/env python
# coding: utf-8
import streamlit as st
st.title('Data of crimes in Vancouver (Canada) from 2003 to 2017') 

st.header('Description of the dataset and size') 

# 
st.markdown('''TYPE - Type of crime'
YEAR - Year when the alleged criminal activity occurred
MONTH - Month when the reported criminal activity occurred
DAY - Date the alleged criminal activity occurred
HOUR - Hour when the reported criminal activity occurred
MINUTE - The minute the alleged crime occurred
HUNDRED_BLOCK - Generalized place for reporting criminal activity
NEIGHBOURHOOD - Area where the alleged criminal activity occurred
X - Coordinate values projected into UTM Zone 10
Y - Coordinate values projected into UTM Zone 10
Latitude - Latitude coordinate values
Longitude - Longitude coordinate values''')

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import seaborn as sns
get_ipython().system('pip install plotly')
import plotly.express as px


# In[2]:


data = pd.read_csv('littlecrime.csv')
st.write(data.head())


# In[3]:


data.dtypes


# In[4]:


st.write(('(Rows, Columns)', data.shape))


st.header('Import the necessary libraries')

st.subheader('Clearing the Dataset and adding columns')

st.header('Display the number of empty values') 

# In[5]:


data.isnull().sum()


st.header('Replace gaps with notes "unknown"') 

# In[6]:


data['HOUR'].fillna("unknown", inplace=True)
data['MINUTE'].fillna("unknown", inplace=True)
data['NEIGHBOURHOOD'].fillna("unknown", inplace=True)


st.header("Create a bool column that tells us whether we know the exact time of the crime and a column with units to make it easier to build graphs and find the amount")

# In[7]:


data['the_exact_time_is_known'] = data['HOUR']!="unknown" 
data['quantity'] = 1
data.head(20)


# In[8]:


data.sort_values(by=["YEAR", "MONTH"], ascending=False).head(20)


# In[9]:


data['DATE'] = pd.to_datetime({'year':data['YEAR'], 'month':data['MONTH'], 'day':data['DAY']})
data['DAY_OF_WEEK'] = data['DATE'].dt.dayofweek
import calendar

def convert_month(text):
    return calendar.month_name[int(text)]

data['Month_Word'] = data['MONTH'].apply(convert_month)
data[:5]


st.subheader('Working with data and numeric fields') 

# In[10]:


print('Median day of month of crimes', (data['DAY']).median())
print('Mean day of week of crimes', (data['DAY_OF_WEEK']).mean())
print('Median seed (day of week of crimes): ',(data['DAY_OF_WEEK']).std())
print('The latest crime: ', max((data['YEAR'])))
print('Mean crime year: ', round(data['YEAR'].mean()))
print('The latest crime: ', min((data['YEAR'])))
print('Mean time of crimes', (data['HOUR']!='unknown').mean())
print('Median time of crimes', (data['HOUR']!='unknown').median())
print('Median seed (hour of crimes): ',(data['HOUR']!='unknown').std())


# In[11]:


fig = px.pie(values=data['the_exact_time_is_known'].value_counts(), 
             names=data['the_exact_time_is_known'].value_counts().index,
            title='Time of the crimes is known',
            )
st.plotly_chart(fig)


# In[12]:


data['the_exact_time_is_known']


st.header("The graph shows that in most of the crimes it was possible to determine the exact time") 

# 

st.subheader("Hypothesis: Most people steal from parked cars")

# In[13]:


fig = px.histogram(data, x='TYPE', title='Сorrelation between number of crimes and their types')
fig.update_layout(xaxis_categoryorder = 'total descending')
st.plotly_chart(fig)


st.subheader("As we can see, the vast majority of crimes are thefts from parked cars, so the hypothesis is correct.") 

st.subheader("Hypothesis: most crimes occur in crowded places")

# In[14]:


fig = px.histogram(data, x='NEIGHBOURHOOD',color_discrete_sequence=["green"], title='Сorrelation between number of crimes and neighbourhoods')
fig.update_layout(xaxis_categoryorder = 'total ascending')
st.plotly_chart(fig)


st.header("The graph shows that the bulk of the crimes were committed in the Central Business District, which is largely due to mass gatherings of people who want to visit cafes, restaurants and the largest shopping center in the city, the hypothesis is confirmed") 

st.subheader("Hypothesis: The crime rate rises towards the summer as many people go on vacation and leave their homes and cars unattended, plus tourists come to the city")

# In[15]:


from datetime import datetime
months = {}
for col in set(data['Month_Word']):
    months[col] = len(data[data['Month_Word']==col])

months = dict(sorted(months.items(), key=lambda m: datetime.strptime(m[0], "%B")))
fig = px.line(x=months.keys(), y=months.values(), title='Сorrelation between number of crimes and months', labels={'x': 'Months', 'y': 'Number of crimes'})
st.plotly_chart(fig)


st.header("According to the plot, you can see that the high level of crime was in August, there were also surges in April - May")
st.header("Using information from additional sources, the high level of crime in August can be explained by an accident in the power system of the United States and Canada. About 10 million Canadians (about a third of the population) were left without electricity. Splashes in April-May could be caused by the success of the local hockey team and mass celebrations. Also in February, Vancouver was nominated to host the Olympic Games, where it won in July.")

# In[16]:


sl2 = {}
types = set(data['TYPE'])
for year in set(data['YEAR']):
    a = []
    for i in set(data['TYPE']):
        df = data[data['YEAR'] == year]
        a.append(len(df[df['TYPE'] == i]))
    sl2[year] = a
sl2    


# In[17]:


import plotly.graph_objects as go
import plotly.express as px
k = 0
fig = go.Figure()
years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
for i in types:
    fig.add_trace(go.Scatter(x = years, y = sl2[years[k]], name = i))
    k+=1
st.plotly_chart(fig)


st.subheader('The number of crimes increases by 2012, theft of vehicles remainds dominant') 

# In[18]:


fig = px.scatter_mapbox(data[data['Longitude'] < 0], lon='Longitude', lat='Latitude', size='Latitude')
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)


# 

st.header('General conclusions:')
st.markdown('''The highest level of crime is noted:
January, April, May, August, September 
Central Business District, especially Howe street 
The most common types of crimes are car thefts and hooliganism''') 

# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=60cc00cb-d22c-4ff0-90d9-70a6bcdaa940' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
