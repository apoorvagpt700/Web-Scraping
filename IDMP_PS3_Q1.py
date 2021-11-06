#!/usr/bin/env python
# coding: utf-8

# # Web Scraping

# 1. Importing required libraries

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# 2. Getting web link and printing the details

# In[2]:


idmp_link="https://www.imdb.com/chart/top"
r=requests.get(idmp_link)
page=r.text

soup=BeautifulSoup(page,"lxml")
print(soup.prettify())


# 3. Extracting required columns

# In[3]:


movie_details=soup.select("td.titleColumn")
movie_stars = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
imdb_rating = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

#empty list
imdb = []


# In[4]:


for index in range(0, len(movie_details)):
    # Seperate movie into: 'place', 'title', 'year'
    data = movie_details[index].get_text()
    imdb_movie = (' '.join(data.split()).replace('.', ''))
    title = imdb_movie[len(str(index))+1:-7]
    release_year = re.search('\((.*?)\)', data).group(1)
    data_final = {"title": title,
            "release_year": release_year,
            "movie_stars": movie_stars[index],
            "imdb_rating": imdb_rating[index]}
    imdb.append(data_final)


# 4. To check the column names

# In[5]:


df=pd.DataFrame(imdb)
print(df.columns)


# 5. To divide movie_star column into 2 columns-  director names and actor names

# In[10]:


df['director']=df.movie_stars.str.split(",").str[0]
df['director']=df.director.replace({"\(dir.\)":''},regex=True)

df['actors']=df.movie_stars.str.split(",").str[1:3]

#round ratings upto 1 decimal
df['imdb_rating'] = df['imdb_rating'].apply(lambda x: round(float(x), 1))

#rearrange columns in required fromat
df=df.reindex(columns=['title','director','actors','release_year','imdb_rating'])


# 6. To show top 10 movies

# In[11]:


df.head(10)

