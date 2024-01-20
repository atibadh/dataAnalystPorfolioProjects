#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning in Pandas

import pandas as pd

df = pd.read_excel(r"/Users/Documents/python_bootcamp/Customer Call List.xlsx")
df

#remove duplicates
df = df.drop_duplicates()
df

#how to drop a column or delete a column
df = df.drop(columns='Not_Useful_Column')
df

#removing unwanted characters - strip() removes removes any leading, and trailing whitespaces.
#you can also specify what to strip by putting it within the parenthsis in qoutes
#lstrip = left strip removes unwanted from the left side of a str
# df['Last_Name']=df['Last_Name'].str.lstrip("...")
# df['Last_Name']=df['Last_Name'].str.lstrip("/")
# df['Last_Name']=df['Last_Name'].str.rstrip("_")

#using the strip function provided with a list of characters, it will remove any charater listed 
df['Last_Name']=df['Last_Name'].str.strip("123./_")
df

#replace everything except a-z, A-Z, and 0-9 with nothing
df["Phone_Number"]=df["Phone_Number"].str.replace('[^a-zA-Z0-9]','')
df

#A lambda function is a small anonymous function. 
#A lambda function can take any number of arguments, but can only have one expression.
#a lambda function is a special type of function without the function name.
#to convert the phone number column to a desired 123-456-7890 format, you must ensure the cloumn is values are all string 

df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))

df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3]+'-'+x[3:6]+'-'+x[7:11])

#print convert dataframe
df

#removes the nan-- values
df["Phone_Number"] = df["Phone_Number"].str.replace('nan--','')

df["Phone_Number"] = df["Phone_Number"].str.replace('Na--','')

df

#using the split function you must specify the value to split on, in this case the comma
#next value is, how many values from left to right to look for, example 2 mean find the first two commas and split into distinct columns when found

#expand = True displays the split columns

#the code below appends the new columns specified to the dataframe, no replacing the address column
df[["Street_Address", "State", "ZIP_code"]] = df["Address"].str.split(',',2, expand=True)

df

df["Paying Customer"] = df["Paying Customer"].str.replace('Yes','Y')

df["Paying Customer"] = df["Paying Customer"].str.replace('No','N')

df

df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('Yes','Y')

df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('No','N')

df

#now we replace the value over the entire data frame
df = df.replace('N/a','')
df

#fill all NaN values with blank values
df = df.fillna('')

df

#removing the row that indicate that they do not want to be contacted

for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == 'Y':
        df.drop(x, inplace=True)

df

#removing the row that indicate that has no phone numbers

for x in df.index:
    if df.loc[x, "Phone_Number"] == '':
        df.drop(x, inplace=True)

# Another way to drop null values

#df = df.dropna(subset="Phone_Number", inplace=True)

#resest the index and drop the original index column
df = df.reset_index(drop=True)

df



