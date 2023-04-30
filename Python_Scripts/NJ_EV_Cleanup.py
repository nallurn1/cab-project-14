import csv
import pandas as pd


# Group the DataFrame by County and Brand, and count the number of occurrences
brand_names = []
with open('NJ_EV_clean.csv') as file:

	f1 = csv.DictReader(file)
	print(f1.fieldnames)

	for row in f1:
		 brand = row['Brand']
		 brand = brand.capitalize()
		 brand_names.append(brand)
		 # if brand == '':
		 # 	csv.remove(f1)



# Read the CSV file into a DataFrame
df = pd.read_csv('NJ_EV_clean.csv')
df = df.dropna()
df.drop(['Brand'], axis=1, inplace=True)
df.insert(loc=1, column='Brand', value=pd.Series(brand_names))
grouped_df = df.groupby(['County', 'Brand']).size().reset_index(name='Count')

# Group the DataFrame by County and sum the counts for each Brand
grouped_df = grouped_df.groupby(['County', 'Brand']).agg({'Count': 'sum'}).reset_index()
grouped_df = grouped_df.dropna(inplace)
#Write the output to a CSV file
grouped_df.to_csv('NJ_EV_output_grouped.csv', index=False)
