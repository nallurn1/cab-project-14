#!/bin/bash 

psql postgres -c "CREATE DATABASE group_test5 WITH ENCODING 'UTF8'" 
username=lion 
database_name=group_test5
 
# for postgresql db 
psql -d $database_name -a -f file.sql 
 

