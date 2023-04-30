from config import config
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# read connection parameters
params = config()

# connect to the PostgreSQL server
# this will connect to group_test5 database
print('Connecting to the %s database...' % (params['database']))
conn = psycopg2.connect(**params)
print('Connected.')   			
cur = conn.cursor()
print(params['database'])

#Website Landing Page
@app.route('/')
def index():
	#the html format for tha index page
    return render_template('index.html')

#home page: where you need to select a nj municipality, county to see their stats
@app.route('/home')
def home():
	print(params['database'])
	cur = conn.cursor()
	cur.execute("ROLLBACK")
	cur.close()
	cur = conn.cursor()

	# This line is where the magic happens, and it somehow just gets called counties. 
	#If we want moree queries here we have to specify on that return line.
	cur.execute("SELECT DISTINCT municipality, county FROM census_data")
	counties = cur.fetchall()

	#Logic for cleaning up the format of the counties
	counties = sorted(counties)
	county = []
	for row in counties:
		c1 = (row[0].replace('(', ''))
		c2 = (row[1].replace(')', ''))
		county.append(f"{c1}, {c2}")

	conn.commit()
	#the html format for tha home page
	return render_template('home.html', county=county)

#the map page shows us the stats for the selected municipality, county
@app.route('/map/<county>')
def show_map(county):
    # get the range from the query parameter, or use the default value of 5% if not provided
	range_percent = request.args.get('range', default=5, type=int) / 100.0
    
	#Creating the cur object to allow us to do live sql queries on the website
	cur = conn.cursor()

	# update the normalizations with current informations
	cur.execute("""
		CREATE VIEW for_score AS 
		SELECT census_data.municipality, census_data.county, census_data.year, census_data.pop_density, emissions.total_mtco2e, electric_vehicle.percent_of_evs, (electric_vehicle.percent_of_evs / (SELECT MAX(electric_vehicle.percent_of_evs) FROM electric_vehicle) * 5) + (emissions.total_mtco2e / (SELECT MAX(emissions.total_mtco2e) FROM emissions) * 3) + (census_data.pop_density / (SELECT MAX(census_data.pop_density) FROM census_data) * 2) AS score 
		FROM census_data 
		LEFT JOIN electric_vehicle ON census_data.municipality = electric_vehicle.municipality AND census_data.county = electric_vehicle.county AND census_data.year = electric_vehicle.year 
		LEFT JOIN emissions ON census_data.municipality = emissions.municipality AND census_data.county = emissions.county AND census_data.year = emissions.year""")

	# Insert the Scores here to hold onto them
	cur.execute("""
		UPDATE census_data
		SET score = for_score.score
		FROM for_score
		WHERE census_data.municipality = for_score.municipality AND census_data.county = for_score.county AND census_data.year = for_score.year
		""")

	# Drop the view
	cur.execute("DROP VIEW for_score")
	

    # Query the database to get the counties within a given range of ev_cars and population
	cur.execute("""
        SELECT DISTINCT c.municipality, c.county
        FROM census_data c
        JOIN electric_vehicle ev
        ON c.municipality = ev.municipality AND c.county = ev.county
        WHERE
        (ev.percent_of_evs >= ((SELECT AVG(percent_of_evs) FROM electric_vehicle) * (1 - %s)))
        AND
        (ev.percent_of_evs <= ((SELECT AVG(percent_of_evs) FROM electric_vehicle) * (1 + %s)))
        AND
        (c.population >= ((SELECT AVG(population) FROM census_data) * (1 - %s)))
        AND
        (c.population <= ((SELECT AVG(population) FROM census_data) * (1 + %s)))""", (range_percent, range_percent, range_percent, range_percent,))
	counties_ev = cur.fetchall()

    # Query the database to get the counties within a given range of emission and population
	cur.execute("""
        SELECT DISTINCT c.municipality, c.county
        FROM census_data c
        JOIN emissions em
        ON c.municipality = em.municipality AND c.county = em.county
        WHERE
        (em.total_mtco2e >= ((SELECT AVG(total_mtco2e) FROM emissions) * (1 - %s)))
        AND
        (em.total_mtco2e <= ((SELECT AVG(total_mtco2e) FROM emissions) * (1 + %s)))
        AND
        (c.population >= ((SELECT AVG(population) FROM census_data) * (1 - %s)))
        AND
        (c.population <= ((SELECT AVG(population) FROM census_data) * (1 + %s)))""", (range_percent, range_percent, range_percent, range_percent,))
	counties_em = cur.fetchall()

	# this block of code is me getting the parts of the municipality county combo that the user clicked
	county = county.replace("\'", "")
	county = county.replace("(", "")
	county = county.replace(")", "")
	county = county.lower()
	county = county.strip()
	parts = county.split(',')
	parts[0] = parts[0].strip()
	parts[1] = parts[1].strip()

	#Creating a new cur object
	cur = conn.cursor()

	# Query to get the score for the given county for 2020
	cur.execute("SELECT score FROM census_data WHERE year = '2020' AND county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	scr2020X = cur.fetchall()
	scr2020 = scr2020X[0][0]

	# Query to get the score for the given county for 2015
	cur.execute("SELECT score FROM census_data WHERE year = '2015' AND county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	scr2015X = cur.fetchall()
	scr2015 = scr2015X[0][0]

	# Query to get the census data for the given county for 2020
	cur.execute("SELECT population, square_miles, year FROM census_data WHERE year = '2020' AND county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	census_data_2020 = cur.fetchall()

	# Query to get the census data for the given county for 2020
	cur.execute("SELECT population, square_miles, year FROM census_data WHERE year = '2015' AND county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	census_data_2015 = cur.fetchall()

	# Query to get the census data for the given county for 2015 and 2020
	cur.execute("SELECT population, square_miles, year FROM census_data WHERE county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	census_data = cur.fetchall()
	# the census data is sent back as a list containing two tuples, one for each year. 
	#I was gonna try to make it a list but it doesnt have to be
	final_census = []
	for i in range(len(census_data)):
		my_list = list(census_data[i])
		final_census.append(my_list)

	# Normalizing  the population and square miles data
	pop_norm = [round(float(row[0]), 2) / round(float(row[1]), 2) for row in census_data]
	sqmiles_norm = [round(float(row[1]), 2) / round(float(row[0]), 2) for row in census_data]

	# Query to get the electric vehicle data for the given county
	cur.execute("SELECT number_of_evs, total_personal_vehicles, year FROM electric_vehicle WHERE county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	ev_data = cur.fetchall()

	# Normalizing the EV data
	ev_norm = [round(float(row[0]), 3) / round(float(row[1]), 3) for row in ev_data]

	# Query to get the emissions data for the given county
	cur.execute("SELECT total_mtco2e, year FROM emissions WHERE county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	emissions_data = cur.fetchall()

	# Calculate the average emissions per capita for the given county
	total_pop = sum([float(row[0]) for row in census_data])
	total_emissions = sum([int(row[0]) for row in emissions_data])
	emissions_per_capita = round((total_emissions / total_pop), 2)


	#-----------------------------------------------------WORKING ON THIS QUERY: CAR BRAND----------------------------------------------------------#
		
	# Query to get the top 5 car brands
	cur.execute("SELECT brand FROM county_brand_data WHERE county=\'{0}\' ORDER BY num_cars DESC LIMIT 5".format(parts[1]))
	top5carbrands = cur.fetchall()

	# Query to get all the top 5 fastest brands
	cur.execute("SELECT brand, avg_accel_sec, avg_topspeed_km_h, avg_range_km, avg_efficiency_wh_km, avg_fastcharge_km_h, avg_priceEuro, avg_priceDollar FROM county_brand_data WHERE county=\'{0}\' ORDER BY num_cars LIMIT 5".format(parts[1]))
	brand_info = cur.fetchall()
	
	#cur.execute("SELECT brand, avg_accel_sec, avg_topspeed_km_h, avg_range_km, avg_efficiency_wh_km, avg_fastcharge_km_h, avg_priceEuro, avg_priceDollar FROM car_brand_info")
	#brand_info = cur.fetchall()
	#brand_info = [tuple(str(e).lower().strip() for e in tpl) for tpl in brand_info]

	# Query to get the NJ EV registration data for the given county
	#Error line => Fixed
	#cur.execute("SELECT num_cars, brand FROM nj_ev_reg WHERE county=\'{0}\' AND municipality=\'{1}\'".format(parts[1],parts[0]))
	#cur.execute("SELECT brand FROM nj_ev_reg")
	#nj_ev_reg = cur.fetchall()
	#nj_ev_reg = [tuple(str(e).replace('County','').lower().strip() for e in tpl) for tpl in nj_ev_reg]


	#cur.execute("SELECT DISTINCT b.brand, b.avg_accel_sec, b.avg_topspeed_km_h, b.avg_range_km, b.avg_efficiency_wh_km, b.avg_fastcharge_km_h, b.avg_priceEuro, b.avg_priceDollar FROM car_brand_info b JOIN nj_ev_reg r ON b.brand = r.brand JOIN electric_vehicle ev ON r.county = ev.county")
	#test_1 = cur.fetchall()

	#cur.execute("SELECT DISTINCT r.brand FROM nj_ev_reg r JOIN electric_vehicle ev ON r.county = ev.county")
	#test = cur.fetchall()

	# Create a dictionary of average car information by brand
	#brand_dict = {}
	#for row in brand_info: 
	#	for r in nj_ev_reg:
#			if r[0] == row[0]:
#				brand_dict[row[0]] = {"accel_sec": row[1], "topspeed_km_h": row[2], "range_km": row[3], "efficiency_wh_km": row[4], "fastcharge_km_h": row[5], "price_euro": row[6], "price_dollar": row[7]}
	#-----------------------------------------------------WORKING ON THIS QUERY: CAR BRAND--------------------------------------------------------#


	#---------------------------------------------------NJ EV REG Query ISSUE---------------------------------------------------------------------#
	#cur.execute("SELECT DISTINCT county FROM nj_ev_reg ")
	#nj_ev_reg = cur.fetchall()
	#nj_ev_reg = [tuple(str(e).replace('County','').lower().strip() for e in tpl) for tpl in nj_ev_reg]

	#cur.execute("SELECT DISTINCT county FROM electric_vehicle")
	#electric_vehicle = cur.fetchall()
	#electric_vehicle = [tuple(str(e).lower().strip() for e in tpl) for tpl in electric_vehicle]

	#Issue: cur.execute("SELECT DISTINCT r.brand, r.num_cars FROM nj_ev_reg r JOIN electric_vehicle ev ON ev.county=\'{0}\' AND ev.municipality=\'{1}\'".format(parts[1],parts[0]))	
	#cur.execute("SELECT DISTINCT r.brand FROM nj_ev_reg r JOIN electric_vehicle ev ON ev.county=\'{0}\' AND ev.municipality=\'{1}\'".format(parts[1],parts[0]))

	#THIS PART IS NOT WORKING EVEN THO THE COUNTYS ARE FORMATED RIGHT FOR NJ_EV_REG and ELEECTRIC_VEHICLE
	#cur.execute("SELECT r.brand, COUNT(*) AS count FROM nj_ev_reg r JOIN electric_vehicle ev ON r.county = ev.county GROUP BY r.brand ORDER BY count DESC")
	#test2 = cur.fetchall()
	#---------------------------------------------------NJ EV REG Query ISSUE---------------------------------------------------------------------#
	

	# Render the template and return it as a response
	return render_template('county.html', census_data=census_data, ev_data=ev_data,pop_norm=pop_norm, sqmiles_norm=sqmiles_norm, ev_norm=ev_norm, emissions_per_capita=emissions_per_capita, total_pop=total_pop, total_emissions=total_emissions, county=county, counties_ev=counties_ev, counties_em=counties_em, brand_info=brand_info , top5carbrands=top5carbrands, scr2015=scr2015, scr2020=scr2020)

if __name__ == '__main__':
    app.run(debug=True)
