import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('Online Retail_small.csv')  # total -- 5419
pd.set_option('display.max_columns', None)
print(data)

# Remove rows with missing values in the required columns
data = data[~data['CustomerID'].isnull()]  # len(data) -- 5419 - 1369 = 4050
data = data[~data['InvoiceDate'].isnull()]  # len(data) -- 5040 - 0 = 5040

# Convert InvoiceDate to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Add a Year column for easier grouping
data['Year'] = data['InvoiceDate'].dt.year
data['Month'] = data['InvoiceDate'].dt.month

# Remove any cancelled transactions
data = data[~data['InvoiceNo'].str.contains('C', na=False)]

# Reset the index
data = data.reset_index(drop=True)

# Summary statistics
print(data.describe())

# Explore categorical columns
print(data['Country'].value_counts())
print(data['Description'].value_counts())

# Check for outliers in numerical columns
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
axes[0].boxplot(data['Quantity'].dropna())
axes[0].set_title('Box Plot of Quantity')
axes[0].set_ylabel('Quantity')

axes[1].boxplot(data['UnitPrice'].dropna())
axes[1].set_title('Box Plot of Unit Price')
axes[1].set_ylabel('Unit Price')

plt.show()

# Group by Month and Year, and calculate total sales
monthly_sales = data.groupby(['Year', 'Month'])['Quantity'].sum().reset_index()

# Plot the monthly sales trend
monthly_sales.set_index(['Year', 'Month'], inplace=True)
monthly_sales.index = monthly_sales.index.set_levels([monthly_sales.index.levels[0].astype(int),
                                                      monthly_sales.index.levels[1].astype(int)])
monthly_sales.index.names = ['Year', 'Month']
monthly_sales['Quantity'].plot(figsize=(12, 6))
plt.xlabel('Month-Year')
plt.ylabel('Total Sales')
plt.title('Monthly Sales Trend')
plt.show()

# Top 10 products by quantity sold
top_products = data.groupby('Description')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False).head(10)
print(top_products)

# Top 5 categories by quantity sold
top_categories = data.groupby('StockCode')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False).head(5)
print(top_categories)

# Bar plot for top products
top_products.set_index('Description', inplace=True)
top_products['Quantity'].plot(kind='bar', figsize=(12, 6))
plt.xlabel('Product')
plt.ylabel('Total Quantity Sold')
plt.title('Top 10 Products by Sales Quantity')
plt.xticks(rotation=45)
plt.show()

# Bar plot for top categories
top_categories.set_index('StockCode', inplace=True)
top_categories['Quantity'].plot(kind='bar', figsize=(12, 6))
plt.xlabel('Category')
plt.ylabel('Total Quantity Sold')
plt.title('Top 5 Categories by Sales Quantity')
plt.xticks(rotation=45)
plt.show()
