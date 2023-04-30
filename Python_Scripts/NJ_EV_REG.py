import csv
import pandas as pd
from pyzipcode import ZipCodeDatabase
from uszipcode import SearchEngine

# Creating a ZipCodeDatabase object
zip_db = ZipCodeDatabase()

# Creating a SearchEngine object
search = SearchEngine()

# Defining lists
# Add the county to the CSV
county = []
c = 1

# Open NJ_EV_Registration file
with open('NJ_EV.csv') as file_obj:

    # Create reader object by passing the file
    # object to DictReader method
    reader_obj = csv.DictReader(file_obj, delimiter= '\t')

    # Check column names in the CSV file
    print(reader_obj.fieldnames)
    # Expected output: ['State', 'ZIP Code', 'Registration Date', 'Vehicle Make', 'Vehicle Model', 'Vehicle Model Year', 'Drivetrain Type', 'Vehicle GVWR Class', 'Vehicle Category', 'Vehicle Count', 'DMV Snapshot (Date)', 'DMV Snapshot ID', 'Latest DMV Snapshot Flag']
    
    # Loop through the rows of the CSV file
    for row in reader_obj:
        # Get the postal code for the current row
        zip_code = row['ZIP Code']
        
        try:
            zip_info = zip_db[zip_code]
            state = zip_info.state
            result = search.by_zipcode(zip_code, state)
            county.append(result.county)
        except:
            print("Location Not Found", zip_code)
            continue

# Add county column to dataframe and write to output file
df = pd.read_csv('NJ_EV.csv', delimiter='\t')
df.drop('State', axis=1, inplace=True)
df.drop('ZIP Code', axis=1, inplace=True)
df.drop(['Registration Date', 'Vehicle Model', 'Vehicle Model Year', 'Drivetrain Type', 'Vehicle GVWR Class', 'Vehicle Category', 'Vehicle Count', 'DMV Snapshot (Date)', 'DMV Snapshot ID', 'Latest DMV Snapshot Flag'], axis=1, inplace=True)
df = df.rename(columns={'Vehicle Make':'Brand'})
df.insert(loc=0, column='County', value=pd.Series(county))
df.to_csv('NJ_EV_output.csv', index=False)
