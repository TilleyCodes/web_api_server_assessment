# Investment Portfolio Management Web API Server

## Table Of Contents

1. [Overview and Purpose](#overview-and-purpose)
2. [Features and Functions](#features-and-functions)
3. [Stystem Requirements](#system-requirements)
4. [Installation](#installation)
5. [Set Up](#set-up)
6. [Ethical Impact of the Licenses](ethical-impact-of-the-licenses)
7. [Database System](#database-system)

---

## Overview and Purpose

This Investment Portfolio Management Web Application is designed to simplify the investment activities of it's users.  
The purpose of this application is to allow the investors on the platform to manage their investment activities as well as execute trades,track their portfolio performance and monitor thier stocks of interest.    

---

## Features and Functions

- Trading and Transactions  
    - Place BUY and SELL orders for stocks.  
	- Record all financial activities (deposits, withdrawals, buys, sells).  
	- Store transaction details (date, type, amount, status) for history tracking.  
- User Accounts and Profiles  
    - Create accounts with personal information (name, email).  
	- View account registration date and current balance.  
- Portfolios and Holdings  
	- Manage portfolios with specific stock holdings and units.  
	- Track portfolio performance and included stocks.  
- Watchlists  
	- Create watchlists to monitor stocks of interest.  
	- Keep a record of stocks invetors are tracking.  
- Stock Information  
	- Access stock details (name, ticker, market price).    
	- View information about stocks in portfolios or watchlists.     

---

## System Requirements

- Operating System:   
    - macOS, Windows or Linux  
- RAM:
    - minimum 1-2 GB
- Storage:
    - minimum 2-4 GB free space
- CPU:
    - 1 GHz single core processor or 2 GHz dual-core processer or better (recommended)
- Programming Language:
    - Python: version 3.9 or higher 
- Relational Database Management System (RDBMS):
    - PostdreSQL

---

## Installation

1. Please ensure to downlod the latest [Python3](https://realpython.com/installing-python/)
2. Install [Terminal for Windows](https://medium.com/@bonguides25/how-to-install-and-update-windows-terminal-in-windows-10-11-b85361b1aa07#:~:text=The%20first%20and%20easiest%20way,minutes%20to%20download%20and%20install.), or [Terminal for Mac](https://medium.com/@latusikl/the-ultimate-setup-for-macos-terminal-7fd340f58366)
3. Optional download: [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) is another terminal that can be used to run the applciation
4. Clone from repository to local machine with the following command in terminal:
```bash
git clone https://github.com/TilleyCodes/web_api_server_assessment
```
5. **Virtual Environment Set Up:** Dependant packages are installed through the terminal virtual environment for dependancy isolation and system python protection.  
    Follow these steps in terminal **before** installing the dependant packages:  
    i. enter virtual environment 
```bash
    python -m venv env
```  
- once the the program has run you will see a folder named .venv     
   
    iia. activate environment for macOS/Linux 
```bash
    source .venv/bin/activate
```  

or,  

    iib. activate environment for windows input:  
 ```bash
    .\env\Scripts\activate
  ```
- this will activate virtual environment. You can then run the pip install command for the corresponding packages per below.    

    iii. deactivate virtual environment  
```bash
    deactivate
```  
- this will exit out of the virtual environment   

6. Install the depandent packages as listed in requirements.txt in bulk with the following command or skip this step if you prefer to install the packages separately - follow the commands under packages:  
```bash
    pip install -r requirements.txt
``` 

---

### Packages

Installation for the following packages are required for the web API server to run successfully. Steps 5.i-iib under Installation must be completed before running the pip install command below.
List of required packages are under requirements.txt file and can be used to bulk install per step 6 above.  

- Flask==3.1.0 - a web framework fro python used to design web application, APIs and microservices.
    - dependencies: 
        - Werkzeug: 3.1.3  
        - Jinja2: 3.1.4 
            - MarkupSafe: 3.0.2 
        - itsdangerous: 2.2.0
        - click: 8.1.7
        - blinker: 1.9.0  
    - license: [BSD License (BSD-3-Clause)](https://flask.palletsprojects.com/en/stable/license/).  
    - Copyright 2010, Armin Ronacher    
    - for installation:    
```bash
    pip install Flask
```

- Flask-SQLAlchemy 3.1.1 - an extention of Flask to add support for SQLAlchemy to the web application.  
    - license: [BSD License](https://github.com/pallets-eco/flask-sqlalchemy/blob/main/LICENSE.txt).  
    - Copyright 2010 Pallets    
```bash
    pip install Flask-SQLAlchemy
```

- flask-marshmallow 1.2.1 - a thin integration layer for Flask and marshmallow used to serialise and deserialise.  
    - dependencies:   
        - marshmallow==3.23.1  
    - license: [MIT License(MIT)](https://github.com/marshmallow-code/flask-marshmallow/blob/dev/LICENSE).    
    - Copyright Steven Loria and contributors      
```bash
    pip install flask-marshmallow
```

- marshmallow-sqlalchemy==1.1.0 - SQLAlchemy integration with the marshmallow serialise and deserialise.  
    - license: [MIT License (MIT)](https://github.com/marshmallow-code/marshmallow-sqlalchemy/blob/dev/LICENSE).  
    - Copyright Steven Loria and contributors  
```bash
    pip install marshmallow-sqlalchemy  
```  

- psycopg2-binary==2.9.10 - a PostgreSQL database adapter for Python used to connect applications to databases.      
    - license: [Lesser General Public License (LGPL) (LGPL with exceptions)](https://github.com/psycopg/psycopg2/blob/master/LICENSE).    
    - copywrite 2001-2021, Federico Di Gregorio, Daniele Varrazzo, The Psycopg Team.      
```bash
    pip install psycopg2-binary
```  

- python-dotenv==1.0.1 - This package allows users to store key-value pairs from a ".env" file and sets them as environmental variables, allowing the storage of sensitive data that can be excluded from deployment to the public.  
    - license: BSD License (BSD-3-Clause)  
    - copywrite 2014 Saurabh Kumar (python-dotenv), 2013 Ted Tieken (django-dotenv-rw), 2013 Jacob Kaplan-Moss (django-dotenv)  
```bash
    pip install python-dotenv
```  

---  

## Set Up

### PostgreSQL  

1. Run the following command in terminal to enter into the postrgreSQL repol environment:  
   ```bash
   psql
   ```    

2. Create a database:
```sql
   CREATE DATABASE web_api_db;
```     

3. Create a user and password (choose you own user and password):
```sql
    CREATE USER <user_name> WITH PASSWORD <'******'>;
```    

4. Grant permission to interact with the database (replace user_name with the name created in step 3): 
```sql
    GRANT ALL PRIVILEGES ON DATABASE web_api_db TO <user_name>;
```  

5. Create .env file and add to DATABASE_URI with the following (replace user name and password per set up):
```bash
    DATABASE_URI=postgresql://<username>:<password>@localhost:5432/web_api_db
```
  
### zsh  

Run the following command in a new terminal to create and seed the tables before starting the development server:    

1. Create the tables:  
```bash
    flask db create
```  

2. Seed the tables:
```bash
    flask db seed
``` 

3. Drop the tables: 
```bash
    flask db seed
```     

**Note:** If you do drop the tables, ensure to re-create and seed the tables again.  

4. Start the development server:  
```bash
    flask run
```     

**** Need to update the insomia and render part****

---  

## Ethical Impact of the Licenses

### MIT License 

The MIT License is a permissive license that allows users to freely use, modify, distribute, and sublicense the software with minimal restrictions. The only condition is to include the original copyright notice and license terms in any distribution.

- Promotes freedom and flexibility for developers and businesses, encouraging innovation and wide adoption.  
- Ensures minimal barriers for commercial use, which can support economic growth.  
- Does not enforce ethical constraints or obligations on how the software is used, which might allow it to be utilised in ways that the original developers might ethically oppose.  


### GNU Lesser General Public License

The LGPL is a more permissive version of the GNU General Public License (GPL). It allows linking to proprietary software without requiring the proprietary code to also be open-sourced, but modifications to the LGPL-covered code must remain open-source.

- Balances between the freedom to use software in proprietary systems and the commitment to open-source principles by requiring contributions back to the open-source community for modifications.
- Promotes collaborative development and prevents proprietary monopolisation of core libraries, which supports fairness and equity in software use.
- May not go far enough in ensuring all derived works remain open-source.  

### BSD License (BSD-3-Clause)

The BSD License is a permissive and allows users to freely use, modify, and redistribute the software.    
  
- Encourages wide adoption and reuse of code by placing few restrictions.
- Supports both open-source and proprietary development, facilitating economic opportunities and innovation.  
- Lacks ethical guardrails on how the software might be used, meaning it could be applied in contexts or for purposes that the original developers might not support.    

---

## Database System

### Why PostgreSQL is the chosen databse for this web API:  

- PostgreSQL is a reliable, enterprise-grade relational database.
- It enforces data consistency and integrity, crucial for financial applications.
- PostgreSQL has advanced SQL capabilities for complex querying and analytics.
- It can handle large data volumes and high user concurrency, providing scalability.
- The extensible ecosystem allows adding specialised features as needed.
- PostgreSQL's relational model aligns well with the structured financial data.
- Compared to NoSQL databases, PostgreSQL is a better fit for this application.
- Overall, PostgreSQL provides the necessary data integrity, querying power, scalability, and extensibility for this investment portfolio management API.  

### PostgreSQL (RDBMS) vs MongoDB (NoSQL Database)

- Data Structure:    
    - PostgreSQL organises data in structured tables with predefined schemas.  
    - MongoDB uses a schema-less model, storing data in document-oriented JSON-like BSON objects.    

- Data Integrity:  
    - PostgreSQL enforces data consistency through strict schemas, primary keys, and foreign keys.  
    - MongoDB trades data integrity for flexibility, allowing loosely defined data structures but risking inconsistency.    
 
- Querying:    
    - PostgreSQL excels at complex queries involving multiple tables and joins.    
    - MongoDB performs well with simple queries and high-speed data retrieval but lacks the querying power of SQL.    

- Flexibility:  
    - PostgreSQL supports structured and semi-structured data (via JSONB), but requires schema changes for major structural adjustments.  
    - MongoDB’s schema-less nature allows for dynamic changes, making it better suited for applications with rapidly evolving data models.  

---  

## Application Help

Open the terminal and run the application.  
(Ensure the set-up and installation steps have been completed).  

- Check python version by inputing in command line.  
```bash
python --version
``` 
or 
```bash
python3 --version
```  
- To run the application, depending on your system and set-up, you may use <u>python</u> or <u>python3</u> and the file name. In this case main.py  
```bash
python main.py
``` 
or 
```bash
python3 main.py
```  

You will see a welcome message and a list of selections below.

Simply enter the number corresponding to your selection.  

![screenshot of app main page](screenshots/app_main_page.png)

- ```Enter 1 to convert currencies using live FX rate.```
    - ```Please enter the amount you wish to convert:``` *This needs to be a numerical value.*
    - ```Please enter the currency code you wish to convert from:``` *The currency code is a 3 letter code representing the currency of choice, you are allowed 3 attempts to enter the correct currency code (if unsure you can view the currency code by entering 4 in the main menu).*
    - ```Please enter the currency code you wish to convert to:``` *The currency code is a 3 letter code representing the currency of choice you are allowed 3 attempts to enter the correct currency code (if unsure you can view the currency code by entering 4 in the main menu).*
    - ```Enter a short description to save a history or enter to exit:``` *If you want to save a history of this conversion, enter a short description otherwise enter with no description will not save.*

![screenshot for currency code error](screenshots/convert_with_live_rate.png)
    
- ```Enter 2 to convert currencies using your personalised FX rate.```
    - ```Please enter the FX rate you received during your exchange:``` *This is the FX rate given when you the the exchange. You are allowed 3 attempts to enter the a numerical value and cannot be zero*
    - ```Please enter the value you wish to convert:``` *This is the monetary value. You are allowed 3 attempts to enter the a numerical value and cannot be zero*
    - ```Do you want this value "x" converted to your base currency? Enter Y or N:``` *to assist with the calculation, enter Y if this is to be converted back to your base currency, (if the value you had input in the above line is the foreign value) otherwise enter N.*

![screenshot for converting with personalised FX rate](screenshots/convert_with_personal_rate.png)

- ```Enter 3 to calculate the FX rate.```
    - ```Please enter the from value to calculate the FX rate:``` *This is the base monetary value. You are allowed 3 attempts to enter the a numerical value and cannot be zero*
    - ```Please enter the to value to calculate the FX rate:``` *This is the foreign monetary value. You are allowed 3 attempts to enter the a numerical value and cannot be zero*

![screenshot for calculating FX rate](screenshots/calculate_fx_rate.png)

- ```Enter 4 to view the currency code list.```
    - *By entering 4, the Currency Code table will automatically populate.*

![screenshot currency code list](screenshots/currency_code_list.png)

- ```Enter 5 to view conversion history.```
    - *By entering 5, the conversion history list will appear if available.*

![screenshot to view conversion history](screenshots/view_conversion_history.png)

- ```Enter 6 to exit.```
    - *By entering 6, you will exit the application and a farewell message will appear.*

![screenshot for exit application](screenshots/exit_app.png)

---

