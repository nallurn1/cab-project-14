\c group_test5
CREATE TABLE census_data_temp (
Municipality VARCHAR (50) NOT NULL,
County VARCHAR(50) NOT NULL,
Muni_and_County VARCHAR(50),
Year INTEGER NOT NULL,
Square_Miles FLOAT NOT NULL,
Population INTEGER NOT NULL,
PRIMARY KEY(Municipality, County, Year)
);

\copy census_data_temp FROM 'cleaned_cd.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

ALTER TABLE census_data_temp DROP COLUMN Muni_and_County;

CREATE TABLE pop_density_data AS SELECT Population, Square_Miles FROM census_data_temp;
ALTER TABLE pop_density_data ADD PRIMARY KEY (population, square_miles);

ALTER TABLE pop_density_data ADD pop_density FLOAT;

UPDATE pop_density_data SET pop_density = population / square_miles;

ALTER TABLE pop_density_data ADD score FLOAT;

CREATE TABLE census_data_table AS SELECT municipality, county, year, population, square_miles FROM census_data_temp;

CREATE TABLE census_data AS SELECT census_data_table.*, pop_density_data.pop_density, pop_density_data.score FROM census_data_table JOIN pop_density_data ON census_data_table.population = pop_density_data.population AND census_data_table.square_miles = pop_density_data.square_miles;

CREATE TABLE electric_vehicle (
Municipality VARCHAR (50) NOT NULL,
County VARCHAR(50) NOT NULL,
Year INTEGER NOT NULL,
Total_Personal_Vehicles INTEGER NOT NULL,
number_of_EVs INTEGER NOT NULL,
percent_of_EVs FLOAT NOT NULL,
PRIMARY KEY(Municipality, County, Year)
);

\copy electric_vehicle FROM 'cleaned_ev.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

CREATE TABLE emissions (
Municipality VARCHAR (50) NOT NULL,
County VARCHAR(50) NOT NULL,
Muni_and_County VARCHAR(50),
Year INTEGER,
Total_MTCO2e FLOAT NOT NULL,
PRIMARY KEY(Municipality, County, Year)
);

\copy emissions FROM 'cleaned_em.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

ALTER TABLE emissions DROP COLUMN Muni_and_County;

CREATE TABLE car_brand_info (
Brand VARCHAR(20) NOT NULL,
Model VARCHAR(40) UNIQUE NOT NULL,
Accel_sec FLOAT,
TopSpeed_km_h INTEGER,
Range_Km INTEGER,
Efficiency_Wh_km INTEGER,
FastCharge_km_h INTEGER,
PriceEuro INTEGER,
PriceDollar INTEGER,
PRIMARY KEY(Model)
);

\copy car_brand_info FROM 'Car_brands_output.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

CREATE TABLE revised_car_brand_info AS SELECT brand, AVG(Accel_sec) avg_accel_sec, ROUND(AVG(topspeed_km_h), 0) avg_topspeed_km_h, ROUND(AVG(range_km), 0) avg_range_km, ROUND(AVG(efficiency_wh_km),0) avg_efficiency_wh_km, ROUND(AVG(fastcharge_km_h),0) avg_fastcharge_km_h, ROUND(AVG(PriceEuro),0) avg_priceEuro, ROUND(AVG(PriceDollar),0) avg_priceDollar FROM car_brand_info GROUP BY brand ORDER BY brand;

ALTER TABLE revised_car_brand_info ADD PRIMARY KEY (Brand);

DROP TABLE car_brand_info;

ALTER TABLE revised_car_brand_info RENAME TO car_brand_info;

CREATE TABLE nj_ev_reg (                                                                  
County VARCHAR(30) NOT NULL,
Brand VARCHAR(40) NOT NULL,
num_cars INTEGER, 
PRIMARY KEY(County, Brand)
);

\copy nj_ev_reg FROM 'NJ_EV_output_grouped.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

CREATE VIEW county_brand_data AS SELECT car_brand_info.*, nj_ev_reg.county, nj_ev_reg.num_cars FROM car_brand_info INNER JOIN nj_ev_reg ON car_brand_info.brand=nj_ev_reg.brand ORDER BY nj_ev_reg.num_cars DESC;


