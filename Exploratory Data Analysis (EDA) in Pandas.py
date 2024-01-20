#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis (EDA) in Pandas

# EDA is basically the first look at your data. This process looks at patterns in the data, understanding the relationship within the features, and look at outliers within the dataset.
# You are also looking for mistake and missing values that will need to be cleaned up.
# The following are some of the most popular EDA techniques.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"/Users/Documents/py_bc/world_population.csv")
df

#to change the decimal display to two placces use the following

pd.set_option('display.float_format', lambda x: '%.2f' % x)

#first EDA step, review data and its data types
df.info()

#Descriptive statistics include those that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.
df.describe()

#show all the columns and display the number of missing values
df.isnull().sum()

#displays how many unique values are in each column
df.nunique()

df.sort_values(by="World Population Percentage", ascending=False).head(10)

#correlation of column, excluding NA/null values
#it will compare all columns to every other other and showing how closely realated they are
df.corr()

#create heat map
sns.heatmap(df.corr(), annot=True)

plt.rcParams['figure.figsize'] = (20,10)

plt.show()

#group by
df.groupby('Continent').mean().sort_values(by="2022 Population", ascending=False)

#serach for and display the results
df[df['Continent'].str.contains('Oceania')]

df2 = df.groupby('Continent').mean().sort_values(by="2022 Population", ascending=False)
df2.transpose()

#used to list all the columns
df2.columns

df2 = df.groupby('Continent')[['1970 Population', '1980 Population', '1990 Population',
                               '2000 Population', '2010 Population', '2015 Population',
                               '2020 Population', '2022 Population']].mean().sort_values(by="2022 Population", ascending=False)
df2

#another way to display only the population columns
df4 = df.groupby('Continent')[df.columns[3:15]].mean().sort_values(by="2022 Population", ascending=False)
df4

df3 = df2.transpose()
df3.plot()

#box plots are great for showing outliers. 
#the dots outside the box are values that fall out of the normal numbers
df.boxplot(figsize=(20,10))

df.dtypes

#dtype allow you to serach the entire dataframe to display either numbers, floats, objects, etc
df.select_dtypes(include='object')