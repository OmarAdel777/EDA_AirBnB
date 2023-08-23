#!/usr/bin/env python
# coding: utf-8

# Import necessary libraries
import os 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the directory path where the data is located
directory_path = r"D:\Datascience\Electropi\0.Data science python\2.EDA-python\3.capstone"

# Loop through the directory to find the filenames
for dirname, _, filenames in os.walk(directory_path):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Define the filepath for the Airbnb listings data
filepath = "D:\\Datascience\\Electropi\\0.Data science python\\2.EDA-python\\3.capstone\\listings.csv"

# Load the Airbnb listings data into a DataFrame
df = pd.read_csv(filepath)

# Display the first few rows of the DataFrame
df.head()

# Display the last few rows of the DataFrame
df.tail()

# Get the dimensions of the DataFrame
df.shape

# Display information about the DataFrame's columns and data types
df.info()

# Check for missing values in each column
df.isna().sum()

# Check for duplicated rows
df.duplicated().sum()

# Get the number of unique values in each column
df.nunique()

# Display unique host names
df.host_name.unique()

# Check for duplicated host IDs
df.host_id.duplicated().sum()

# Display unique values in the 'neighbourhood_group' column
df["neighbourhood_group"].unique()

# Drop columns with excessive missing values or duplicates
df.drop(["neighbourhood_group", "last_review", "license", "host_name", "host_id"], axis=1, inplace=True)

# Fill missing values in the 'reviews_per_month' column with zeros
df.fillna({"reviews_per_month": 0}, inplace=True)
df.reviews_per_month.isnull().sum()

# Check for any remaining missing values
df.isnull().sum()

# Display summary statistics for numeric columns
df.describe().T

# Convert 'neighbourhood' and 'room_type' columns to categorical for efficiency
df["neighbourhood"] = df["neighbourhood"].astype("category")
df["room_type"] = df["room_type"].astype("category")

# Clean column names by replacing underscores and converting to title case
df.columns = df.columns.str.replace('_', ' ').str.title()

# Replace a specific text format in the 'Room Type' column
df['Room Type'].replace('Entire home/apt', 'Entire Home/Apt', inplace=True)

# Display counts of listings per neighborhood
df['Neighbourhood'].value_counts()

# Rename the 'Price' column to 'Price in Dollars'
df.rename(columns={'Price': 'Price in Dollars'}, inplace=True)

# Calculate the correlation matrix and visualize it as a heatmap
correlation = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.show()

# Create a histogram of the 'Price in Dollars' column
plt.figure(figsize=(12, 6))
sns.histplot(data=df["Price in Dollars"], bins=10, kde=False, color='blue')
plt.xlabel('Price in Dollar')
plt.ylabel('Frequency')
plt.title('Histogram of Price in Dollar')
plt.show()

# Create a boxplot of 'Price in Dollars' by 'Room Type'
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Room Type', y='Price in Dollars', showfliers=False)
plt.show()

# Create a boxplot of 'Availability 365' by 'Neighbourhood'
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Neighbourhood', y='Availability 365')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ...
# (continued from the previous code snippet)

# Create a violin plot of 'Availability 365' by 'Neighbourhood'
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='Neighbourhood', y='Availability 365')
plt.xticks(rotation=90)
plt.show()

# Display value counts for the 'Neighbourhood' column
df['Neighbourhood'].value_counts()

# Get value counts for the 'Room Type' column
a = df["Room Type"].value_counts()
print(a)

# Create a DataFrame to organize the value counts of 'Room Type'
x = pd.DataFrame(a.values, columns=['Count'], index=a.index).reset_index()
x.rename(columns={'index': 'Room Type'}, inplace=True)
print(x)

# Create a bar plot to visualize counts of each 'Room Type'
plt.figure(figsize=(10, 8))
plt.bar(x=a.index, height=a.values, width=0.6, color=['orange', 'blue', 'green', 'red', 'black'], alpha=0.5, label=a.index)
for i, j in enumerate(a.values):
    plt.text(i, j+1, j, ha='center', va='bottom')

# Get value counts for the 'Name' column and create a horizontal bar plot
y = df['Name'].value_counts().head(10)
plt.barh(y=y.index, width=y.values, height=0.6, alpha=0.5, label=y.index)
plt.legend(bbox_to_anchor=(1, 0.8))
plt.show()

# Group and aggregate data to calculate mean prices by 'Neighbourhood', 'Room Type', and 'Availability 365'
n = df.groupby(['Neighbourhood', 'Room Type', 'Availability 365'])['Price in Dollars'].mean().sort_values(ascending=False).round(1)
n

# Reshape the aggregated data for better visualization
n1 = n.unstack(level=1)
n1

# Create a subplot with multiple histograms
fig = plt.figure(figsize=(15, 20))
ax = fig.gca()
df.hist(ax=ax)

# Create pair plots to visualize relationships between numeric columns
ax = sns.pairplot(df, y_vars="Availability 365", x_vars=["Price in Dollars", "Minimum Nights", "Latitude", "Longitude"], kind='reg')
ax.map(sns.scatterplot)

# Identify top host IDs based on listing counts
hid = df['Id'].value_counts().sort_values(ascending=False).head(10).index
hid

# Filter the DataFrame to show listings associated with the top host IDs
i = df[df['Id'].isin(hid)]
i

# Group and count listings by 'Neighbourhood' for the top host IDs
i1 = i.groupby('Neighbourhood').agg('count')['Id'].sort_values(ascending=True)
i1

# Create a horizontal bar plot to visualize the top host's neighbourhoods
fig, ax = plt.subplots(1, 1, figsize=(8, 10))
fig1 = ax.barh(y=i1.index, width=i1.values, color='red', alpha=0.5)
plt.ylabel('Neighbourhood', fontdict={'fontsize': 20})
plt.xlabel('No of Airbnb services', fontdict={'fontsize': 15})
plt.title("Top 10 host's neighbourhood", fontdict={'fontsize': 18})
plt.bar_label(container=fig1, labels=i1.values, label_type='edge')
plt.yticks(fontsize=9)
plt.show()
