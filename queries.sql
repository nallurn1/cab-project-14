SELECT municipality, population, year FROM census_data WHERE municipality='Aberdeen township';

SELECT municipality, square_miles, year FROM census_data WHERE county= 'Union';

SELECT nj_ev_reg.brand, nj_ev_reg.num_cars, avg_topspeed_km_h FROM car_brand_info INNER JOIN nj_ev_reg ON car_brand_info.brand = nj_ev_reg.brand;



