import csv
import pandas as pd
#Not working with installing this, have issues with my python...
#..path on my machine
#from currency.converter import CurrencyConverter

#Creating the currency object
#cur = CurrencuConverter()
curr_eur_usd = []

with open('Car_brands.csv') as file:

	f1 = csv.DictReader(file, delimiter='\t')
	print(f1.fieldnames)

	for row in f1:
		euro = row['PriceEuro']
		euro = int(euro)

		try:
			#Coverting EUR to USD
			# c = cur.convert(euro, 'EUR', 'USD')
			c = int(euro*1.087)
			curr_eur_usd.append(c)
		except:
			c = int(euro*1.087)
			#print(c)
			curr_eur_usd.append("None")
			continue

# Add pricedollar column to dataframe and write to output file
df = pd.read_csv('Car_brands.csv', delimiter='\t')
df.drop('PriceDollar', axis=1, inplace=True)
df.insert(loc=8, column='PriceDollar', value=pd.Series(curr_eur_usd))
df.to_csv('Car_brands_output.csv', index=False)
