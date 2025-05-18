#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
Project Introduction: 
(@) I'm working as a Data Analyst for a foreign company and my mission is to analyze data on Google Play and Apple Store to determine what types of genres on two apps are likely to attract more users.
(@) The company only builds apps that are free to download and install, and  designs them for English-Speaking audience.
# # Opening datasets

# Let's open two datasets and explore the data inside each dataset

# In[1]:


def open_data(file_csv):
    from csv import reader
    open_file = open(file_csv)
    read_file = reader(open_file)
    dataset = list(read_file)
    return dataset


# In[2]:


#Opening AppleStore dataset
file_name = open_data('AppleStore.csv')
header_app_store = file_name[0]
app_store = file_name[1:]


# In[3]:


#Opening GooglePlay dataset
file_name = open_data('googleplaystore.csv')
header_google_play = file_name[0]
google_play = file_name[1:]


# # Exploring data
To make the table easier to read, I create the explore() function to show rows starting by header and ending with a row you want, as well as showing the total number of apps.
# In[4]:


def explore_data(dataset,start,end,rows_and_columns=False):
    data_slice = dataset[start:end]
    for space in data_slice:
        print(space)
        print('\n')
    if rows_and_columns ==True:
        print("Number of columns:",len(dataset[0]))
        print("Number of rows:",len(dataset))


# In[5]:


print(header_app_store)
print('\n')
explore_data(app_store,0,1,True)


# In[6]:


print(header_google_play)
print('\n')
explore_data(google_play,0,1,True)


# # Quality Data Report:
Before i get to to work on doing data cleaning, i need to know the quality of data which i am working with. Therefore, i am going make a quality report to check null values, duplicate values and unique values.
# In[7]:


import pandas as pd
APS = pd.read_csv('AppleStore.csv')
GPS = pd.read_csv('googleplaystore.csv')


# In[8]:


def check_data_quality(df,column):
    quality_report = {
        'null_values': df.isnull().sum().to_dict(),
        'duplicate_values': df[column].duplicated().sum(),
        'unique_values': len(df[column].unique()),
        'total_rows': len(df)
        }
    return quality_report

Appstore report based on Id column, as an ID represents a customer.
# In[9]:


quality_report = check_data_quality(df=APS,column='id')
display(quality_report)


# There is no error data in Appstore report, so it doesn't need to clean 
GooglePlay report based on App column 
# In[10]:


quality_report = check_data_quality(df=GPS, column='App')
display(quality_report)

It needs to remove duplicate_values and check null_values if any error inside it
# # Data Cleaning
Let us go to work on cleaning. First, I'll review each row's data to identify any issues. Analyze to decide whether to remove it or not.
# #      Detect inaccurate data in each row and remove

# In[11]:


for row in app_store:
    header_length = len(header_app_store)
    row_length = len(row)
    if row_length != header_length:
        print(row)
        print(app_store.index(row))


# **As we can see, row(10472) has problemtic datas in "category" and "rating" column which are 1.9 and 19. So i am going to delete it.

# In[12]:


for row in google_play:
    header_length = len(header_google_play)
    row_length = len(row)
    if row_length != header_length:
        print(header_google_play)
        print(row)
        print(google_play.index(row))
del google_play[10472] #run del statement once


# In[13]:


for row in app_store:
    header_length = len(header_app_store)
    row_length = len(row)
    if row_length != header_length:
        print(header_app_store)
        print(row)
        print(app_store.index(row))

AppStore has no error rows.
# #    Detect duplicate values
I create a function to check duplicate and unique values in two datasets.
If the app appears the first time, it will assign to unique_app. The second time  will move to duplicate_app
# In[14]:


def check_duplicate(dataset,index):
    duplicate_app = []
    unique_app = []
    for app in dataset:
        name = app[index]
        if name  in unique_app:
            duplicate_app.append(name)
        elif name not in duplicate_app:
            unique_app.append(name)
    return duplicate_app, unique_app


# In[15]:


duplicate_app, unique_app = check_duplicate(app_store,0)
print("Number of duplicate app:",len(duplicate_app))
print("Number of unique app:",len(unique_app))
print("Actual length of app store:",len(app_store))


# In[16]:


duplicate_app, unique_app = check_duplicate(google_play,0)
print("Number of duplicate app:",len(duplicate_app))
print("Number of unique app:",len(unique_app))
print("Actual length of google play:",len(google_play))


# **Criterion to remove: keep the highest number of reviews in each app and remove the others
We are going to create a dictionary that contains each key is an unique app name with its highest number of reviews.
There are four steps inside the dictionary:
    (1) To check the name in the dictionary or not
    (2) If: it has the name => compare the current review to new review
    + If a new review > current review in dictionary => update new review
    + If new review < current review in dictionary => Remain current review
    (3) If: it hasn't => Add the new app to the dictionary with the review.
# In[17]:


reviews_max = {}
for row in google_play:
    name = row[0]
    currnt_reviews = float(row[3])
    if (name in reviews_max) and reviews_max[name] < currnt_reviews:
        reviews_max[name] = currnt_reviews
    elif name not in reviews_max:
        reviews_max[name] = currnt_reviews
#display(reviews_max)

I do not want to take the duplicate entries, i have one way to only take unique tries.
First use reviews_max dictionary (which contains Key=App & Value = Highest Review)
After that, i say:
- If there is a row with the review as same as highest review, also advoid name appear twice. Add this row to a list called "Cl_google_play".
# In[18]:


Cl_google_play = []
added_app = []
for row in google_play:
    name = row[0]
    currnt_reviews = float(row[3])
    if (currnt_reviews == reviews_max[name]) and (name not in added_app):
        Cl_google_play.append(row)
        added_app.append(name)


# In[19]:


explore_data(Cl_google_play,0,2,True)


# #     Remove Non-ASCII apps: 
Remember the company aims to English-speaking audience, so i'd like to analyze only the apps that are designed for their target. However,i find that both datasets have apps with names that suggest they are not designed for an English-speaking audience.**To minimize the impact of data loss, i will only remove an app if its name has more than three non-ASCII characters:
# In[20]:


def check_ASCII(string):
    non_ASCII = 0
    for character in string:
        if ord(character) > 127:
            non_ASCII += 1
    if non_ASCII >3:
        return "Non English"
    return "English"
#print(check_ASCII('Instagram'))
#Print('爱奇艺PPS -《欢乐颂2》电视剧热播')


# In[21]:


EngCl_googleplay = []
EngCl_appstore= []

for app in Cl_google_play:
    name = app[0]
    if check_ASCII(name)=="English":
        EngCl_googleplay.append(app)     

for app in app_store:
    name = app[1]
    if check_ASCII(name)=="English":
        EngCl_appstore.append(app) 


# In[22]:


explore_data(EngCl_appstore,0,2,True)


# In[23]:


explore_data(EngCl_googleplay,0,2,True)


# We can see that we're left with 9614 Googleplay and 6183 AppleStore.

#  #     Isolating the Free Apps

# As i mentioned in the introduction, the company only build apps that are free. So i am going to remove non-free apps based on "Price" column.
# Rightnow, i am going to create a function to see how many apps have the price "zero" and remove others after that.

# In[24]:


def price_list(dataset,index):
    price_dict = {}
    for row in dataset:
        price = row[index]
        if price in price_dict:
            price_dict[price] +=1
        elif price not in price_dict:
            price_dict[price] = 1
    return price_dict

def sort_value(item):
    return item[1]

After checking the price_list, there are:
    (+) Free apps:
        - AppStore: 3222 apps that are free
        - GooglePlay: 8864 apps that are free
    (+) Non-Free apps:
        - AppStore: 2961 apps that are not free
        - GooglePlay: 760 apps that are not free
# In[25]:


pricelist_appstore = price_list(EngCl_appstore,4)
sorted_value = sorted(pricelist_appstore.items(),key=sort_value,reverse=True)
print(sorted_value)


# In[26]:


pricelist_googleplay = price_list(EngCl_googleplay,7)
sorted_value = sorted(pricelist_googleplay.items(),key=sort_value,reverse=True)
print(sorted_value)

Rightnow, we are going to get to work to remove the Non-Free English apps.
The idea to remove is that:
    + if the price is not '0' => remove
    + if the price is '0' => add to the list
**Note: rember the type of the "price" column
# In[27]:


NFrEngCl_applestore = []
FrEngCl_applestore = []
for row in EngCl_appstore:
    price = row[4]
    if price != str('0.0') and price != str('0'):
        NFrEngCl_applestore.append(row)
    elif price == str('0.0') or price == str('0'):
        FrEngCl_applestore.append(row)
print("Free Apps of AppStore:",len(FrEngCl_applestore))
print("Non Free Apps of AppStore:",len(NFrEngCl_applestore))


# In[28]:


NFrEngCl_googleplay = []
FrEngCl_googleplay = []
for row in EngCl_googleplay:
    price = row[7]
    if price != str('0.0') and price != str('0'):
        NFrEngCl_googleplay.append(row)
    elif price == str('0.0') or price == str('0'):
        FrEngCl_googleplay.append(row)
print("Free Apps of GooglePlay:",len(FrEngCl_googleplay))
print("Non Free Apps of GooglePlay:",len(NFrEngCl_googleplay))


# # Most Common Apps by Genre
I've spent an amount of time cleaning data, including the following:
    - Removing inaccurate data
    - Removing duplicates app entries
    - Removing non-English apps
    - Isolating the free apps
Let's move on to the final goal is to find app profiles that are successful in both markets to add the app on both GooglePlay and AppStore.
# **Build a frequency table for the prime_genre column of the App Store data set
# for the Genres and Category columns of the Google Play data set.

# In[29]:


def freq_table(dataset,index):
    genre_dict = {}
    total_number_of_apps = len(dataset)
    for row in  dataset:
        genre = row[index]
        if genre in genre_dict:
            genre_dict[genre] +=1
        elif genre not in genre_dict:
            genre_dict[genre] = 1
    
    genre_percentage = {}
    for genre in genre_dict:
        percentage = (genre_dict[genre]*100)/total_number_of_apps
        genre_percentage[genre] = percentage
    return genre_percentage


# In[30]:


def display_table(dataset,index):
    table_display = freq_table(dataset,index)
    table_sorted = sorted(table_display.items(),key=lambda x:x[1],reverse=True)
    for entry in table_sorted:
        print(entry[0],":",entry[1])


# In[31]:


display_table(FrEngCl_applestore,11)

- Among the free English apps, we can see that "Games" genre accountings for (58%). Entertaiment apps are approximately (8%) and followed by Photo & Video closed to (5%). There is only (~3.6%) which is designed for Education.
- The general impression is that most apps on the App Store lean toward entertainment (e.g., Games, Social Networking, etc.). However, a large percentage of apps belonging to a particular genre does not necessarily mean those apps have a large user base.
# In[32]:


display_table(FrEngCl_googleplay,1)


# There are a good number of apps are designed for life-support apps (Family,Tools, Business,LifeStyle,Productivity,etc).

# # Most Popular Apps by Genre on the AppStore
- To find out the most popular apps (have the most users), i have to find out the average install of each genre. 
- For GooglePlay dataset, i can find this information on "Install" column, but there is no "Install column" in AppStore dataset. Therefore, i am going to use "Rating_count_tot" column as a replacement
# In[33]:


genre_appstore = freq_table(FrEngCl_applestore,11)
genre_averages = []

for unique_genre in genre_appstore:
    total_rating = 0
    length_genre = 0
    
    for app in FrEngCl_applestore:
        genre_app = app[11]
        if genre_app == unique_genre:
            n_ratings = float(app[5])
            total_rating += n_ratings
            length_genre += 1
            
    average_rating = total_rating / length_genre
    genre_averages.append((unique_genre, average_rating))
    
    print(unique_genre,":",average_rating)

- The table displays all genres alongside their corresponding review counts, making the data difficult to interpret because of not desecending order. To simplify, I will first identify the top 5 genres with the highest average number of installs, then analyze the apps within those genres.
# In[34]:


top_5_genres = sorted(genre_averages,key=lambda x:x[1],reverse=True)[:5]
print("Top 5 Genres by Average Installs on AppleStore:")
for genre, average in top_5_genres:
    print(genre,":",average)

** "Navigation" genre inclined toward two majors app these are "Waze" and "Google Maps" which accounted for most of the ratings in Navigation
# In[35]:


for app in FrEngCl_applestore:
    if app[11] =='Navigation':
        print(app[1],":",app[5])

**The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc.
# In[36]:


for app in FrEngCl_applestore:
    if app[11] == 'Social Networking':
        print(app[1], ':', app[5]) #App - Install

**Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# In[37]:


for app in FrEngCl_applestore:
    if app[11] == 'Music':
        print(app[1], ':', app[5]) #App - Install

**"Refenrce" genre would been amazing if Bible and Dictionary did not skew up the average rating.
# In[38]:


for app in FrEngCl_applestore:
    if app[11] == 'Reference':
        print(app[1], ':', app[5]) #App - Install


# # Most Popular Apps by Genre on Google Play
On GooglePlay dataset has the "Install" column, but the data is not very clear. I do not know whether an app with 100,000+ installs has 100,000 number of installs,...
# In[39]:


display_table(FrEngCl_googleplay,5)

- I don't know a detailed data for our purpose, I just want to get an idea which apps in genres attract the most users.
- So i'm going to compute the average installs in each genre. However, I need to convert each install number from "string" to "float" (100,000+). It means i need to remove the commas and the plus characters
# In[40]:


category_googleplay = freq_table(FrEngCl_googleplay,1)
category_averages = []

for unique_category in category_googleplay:
    total_installs = 0
    length_category = 0
    for app in FrEngCl_googleplay:
        category_app = app[1]
        if category_app == unique_category:
            n_installs = float(app[5].replace(',','+').replace('+',''))
            total_installs += n_installs
            length_category +=1
    average_install = total_installs / length_category
    category_averages.append((unique_category,average_install))
    
    print(unique_category,":",average_install)


# In[41]:


top_5_category = sorted(category_averages,key=lambda x:x[1],reverse=True)[:5]
print("Top 5 categories by Average Installs:")
for category,average in top_5_category:
    print(category,":",average)


# To recommend potential app profile for GooglePlay, i'm going to filter those apps with under 100 millions installs.

# In[69]:


for app in FrEngCl_googleplay:
    n_installs = app[5].replace(',','+').replace('+','')
    if app[1] == 'SOCIAL' and float(n_installs) < 100_000_000:
        print(app[0], ':', app[5])

With various reasons to capture attent of users on the internet, so it's probably a good idea to build similar apps since there'll be some significant competition.

Social media has become an indispensable part of people's lives, there are alot of reasons to capture more attentions of users on the internet. So it's probably a good idea to invest social apps. We know that there'll be some sharks: Instagram, facebook,... but how about "social learning, self-study, chatting and dating app).
# # Conclusions
In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.

I concluded that buidling social learning, self-study and dating apps could be profitable for both Google Play and App Store Markets. Learners can track their study time on Statistic dashboard and they can meet strangers have the same motivation to study. A forum on app where people can discuss.