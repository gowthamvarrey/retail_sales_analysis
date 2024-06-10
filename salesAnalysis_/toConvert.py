import pandas as pd

# Load the dataset
data = pd.read_excel('Online Retail.xlsx')

# Get the number of rows in the dataset
n_rows = len(data)

# Select a random half of the rows
random_indices = data.sample(frac=0.01).index

# Create a new DataFrame with the selected rows
data_small = data.loc[random_indices].reset_index(drop=True)

# Save the smaller dataset as a CSV file
data_small.to_csv('Online Retail_small.csv', index=False)
