[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-8d59dc4de5201274e310e4c54b9627a8934c3b88527886e3b421487c677d23eb.svg)](https://classroom.github.com/a/-Nv0cKFk)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10766694&assignment_repo_type=AssignmentRepo)

# Project Name: Positive Point System

## What is Positive Point System?
Positive Point System, is cutting-edge web application designed to help you access important information about New Jersey's municipalities in an engaging and user-friendly way. Powered by Flask, a robust Python web framework, our platform is a one-stop-shop for data on population density, electric vehicle ownership, carbon emissions, and much more.
At Positive Point System, we believe in the power of data to drive positive change. That's why we use these stats to empower citizens and lawmakers alike to make informed decisions about energy usage and green energy adoption. Our platform is designed to be accessible and easy to use, so you can quickly find the information you need to make a difference in your community.

## Want to learn more about Positive Point System and how to improve our website??? 
* [Learn More About Our Project & Our Code :)](documentation/pps.md)

## How does the website work? 
> Graphical User Interface Instructions
* [Click here to see the GUI Figures](documentation/gui.md)

## How to get the website running? 
> Database Creation, Population and Lauching Flask Server Instruction
* Step 1. Create Database_Project folder, path should be /home/lion/Database_Project
###### Note: You can do this in the termial by doing mkdir Database_Project
* Step 2. Then in the termial do this command: cd Database_Project
* Step 3. Clone Repository git clone https://github.com/TCNJ-degoodj/cab-project-14.git
###### Note: Make sure to clone the main branch
* Step 4: git config --global user.name "your username"
* Step 5: git config --global user.email "your email@tcnj.edu"
###### Note: Make an ssh key or a github token that will allow you to clone, pull, push and etc this repo
* Step 6. Type into your command line: chmod 700 sql_script.sh && ./sql_script.sh
###### Note: The database name is group_test5
* Step 7. Type into your command line: psql -d group_test5 -f queries.sql
###### Note: This will run some test queries on database
* Step 8: python -m venv venv
* Step 9: source venv/bin/activate
* Step 10. Type into your command line: chmod 700 run_flask.sh && ./run_flask.sh
###### Note: This will allow for the website to be running
* Step 11. In a browser, like Chrome, on the server type into the search bar: http://127.0.0.1:5000
###### Note: Now the website is live
* Step 12. Now have fun with our project :)

## Extra Resources 
### SSH KEY Instructions
Please see the guides below for instructions on how to set up an SSH key and clone this repository:
* [Setting up SSH keys with GitHub](documentation/Setting_up_SSH_keys_GitHub.md)
