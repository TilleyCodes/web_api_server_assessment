# Investment Portfolio Management Web API Server

## Table Of Contents

1. [Overview and Purpose](#overview-and-purpose)  
2. [Entity Relationship Diagram ](#entity-relationship-diagram)  
    - [Entities, Relationships, and Foreign Keys](#entities-relationships-foreign-keys)  
3. [Features and Functions](#features-and-functions)  
4. [System Requirements](#system-requirements)  
5. [Installation](#installation)  
    - [Virtual Environment Set Up](#virtual-environment-set-up)
    - [Packages](#packages)  
6. [Set Up](#set-up)  
    - [PostgreSQL](#postgreSQL)  
    - [zsh](#zsh)  
7. [Deployment](#deployment)    
8. [Testing](#testing)    
    - [API Endpoints](#api-endpoints)  
9. [License](#license)  
10. [Database System](#database-system)  

---

## Overview and Purpose

This Investment Portfolio Management Web Application is designed to simplify the investment activities of its users.  
The purpose of this application is to allow the investors on the platform to manage their investment activities as well as execute trades, track their portfolio performance and monitor their stocks of interest.    

---

## Entity Relationship Diagram  

![Investment Portfolio Management ERD](<images/API ERD.png>)

### Legend

![One and only One](<images/One and only One.png>) - One and only One    
![One to Many](<images/One to Many.png>) - One to many  
![Zero to Many](<images/Zero to Many.png>) - Zero to Many  

### Entities, Relationships, and Foreign Keys 

- Investor  
    - one and only one investor can:  
        - place zero or many orders.  
        - have zero or many portfolios.  
        - have zero or many watchlists.  
        - have zero or many transactions.  

- Stocks  
    - one and only one stock can be:  
        - bought or sold zero or many times in an order placement.    
        - added zero or many times to the watchlists.    
        - added zero or many times to the portfolios.    

- Orders 
    - one and only one order can be added to one and only one transaction.        
        - investor_id Foreign Key.     
        - stock_id Foreign Key.      

- Transactions 
    - one and only one transaction can be added to one and only one order.   
    - zero or many transactions can have one and only one investor.    
        - investor_id Foreign Key.         
        - order_id Foreign Key.  

-  Portfolio  
    - zero or many portfolios can have one and only one investor.    
    - zero or many portfolios can have one and only one stock.  
        - investor_id Foreign Key.     
        - stock_id Foreign Key.

- Watchlists (junction between investors and stocks) 
    - zero or many watchlists can have one or many investors and stocks.  
        - investor_id Foreign Key.         
        - stock_id Foreign Key.  

---  

## Features and Functions

- Trading and Transactions:   
    - Place BUY and SELL stock orders.  
    - Record financial activities, including deposits, withdrawals, buys, and sells.  
    - Store transaction details (date, type, amount, and status).  

- Investor Accounts and Profiles:  
    - Create investor accounts with personal details (name, email).  
    - View account registration dates and current balances.  

- Portfolios and Holdings:  
    - Manage portfolios with specific stock holdings and units.  
    - Monitor portfolio performance.  

- Watchlists:  
    - Create watchlists to monitor stocks of interest.  
    - Track stocks investors are following.  

- Stock Information:  
    - Access stock details, including name, ticker, and market price.  
    - Retrieve stock details in portfolios or watchlists.       

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

This section provides step-by-step instructions to set up the web API server, including creating a virtual environment, installing dependencies, and configuring the database.

1. Please ensure to download the latest [Python3](https://realpython.com/installing-python/)
2. Install [Terminal for Windows](https://medium.com/@bonguides25/how-to-install-and-update-windows-terminal-in-windows-10-11-b85361b1aa07#:~:text=The%20first%20and%20easiest%20way,minutes%20to%20download%20and%20install.), or [Terminal for Mac](https://medium.com/@latusikl/the-ultimate-setup-for-macos-terminal-7fd340f58366) is another terminal that can be used to run the application
3. Optional download: [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) is another terminal that can be used to run the application  
4. Download [Insomia](https://insomnia.rest/download) for testing API  
5. Clone from repository to local machine with the following command in terminal:
```bash
git clone https://github.com/TilleyCodes/web_api_server_assessment
```
6. **Virtual Environment Set Up:** Dependent packages are installed through the terminal virtual environment for dependency isolation and system python protection.  

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
    .\venv\Scripts\activate
```
- this will activate virtual environment. You can then run the pip install command for the corresponding packages per below.    

    iii. deactivate virtual environment  
```bash
    deactivate
```  
- this will exit out of the virtual environment   

7. Install the dependent packages as listed in requirements.txt in bulk with the following command or skip this step if you prefer to install the packages separately - follow the commands under packages:  
```bash
    pip install -r requirements.txt
``` 

---

### Packages

Installation for the following packages are required for the web API server to run successfully. Steps 5.i-iib under Installation must be completed before running the pip install command below.
List of required packages are under requirements.txt file and can be used to bulk install per step 6 above.  

- Flask==3.1.0 - a web framework for python used to design web application, APIs and microservices.
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

- Flask-SQLAlchemy 3.1.1 - an extension of Flask to add support for SQLAlchemy to the web application.  
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
    - copyright 2001-2021, Federico Di Gregorio, Daniele Varrazzo, The Psycopg Team.      
```bash
    pip install psycopg2-binary
```  

- python-dotenv==1.0.1 - this package allows users to store key-value pairs from a ".env" file and sets them as environmental variables, allowing the storage of sensitive data that can be excluded from deployment to the public.  
    - license: BSD License (BSD-3-Clause)  
    - copyright 2014 Saurabh Kumar (python-dotenv), 2013 Ted Tieken (django-dotenv-rw), 2013 Jacob Kaplan-Moss (django-dotenv)  
```bash
    pip install python-dotenv
```    

- gunicorn==23.0.0 - a Python HTTP server for WSGI application.  
    - license: [MIT License (MIT)](https://github.com/benoitc/gunicorn/blob/master/LICENSE)    
    - copyright 2009-2024 (c) Benoît Chesneau, 2009-2015 (c) Paul J. Davis  
```bash
    pip install gunicorn
```   

---  

## Set Up

### PostgreSQL  

1. Run the following command in terminal to enter into the postrgreSQL repl environment:  
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
    DATABASE_URI=postgresql://<username>:<password>@localhost:<port_number>/web_api_db
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
    flask db drop
```     

**Note:** If you do drop the tables, ensure to re-create and seed the tables again.  

4. Start the development server:  
```bash
    flask run
```     

---  

## Deployment    

The API was deployed using Render: [https://tilley-investment-portfolio-web-api.onrender.com]   

Example: Create a stock.

![Create stock Render](<images/Create a stock using Render.png>)

---

## Testing    

Insomia will be used to test the CRUD operations on all entities for the Investment Portfolio Managemnt WEB API. Using the default http://localhost:5000 as the base URL.         
Follow step 4 in [Installation](#installation) if Insomia is not yet downloaded.    

Note: If the database is hosted on Neon, update the `DATABASE_URI` in the `.env` file accordingly. Also Gunicorn default URL localhost port number is 8000 eg. http://localhost:8000  
Start the development server using gunicorn:   
```bash
    gunicorn 'main:create_app()'
```  

### API Endpoints    

Add the endpoint to the end of URL. Example: http://localhost:5000/investors    

#### investors entity  

- Retrieve all investors:     
    - Method: GET `/investors`    
- Retrieve a single investor:       
    - Method: GET `/investors/<investor_id>`    
- Retrieve a list of investors by f_name:     
    - Method: GET `/investors?f_name=<name>`     
- Retrieve a list of investors by registration_date:     
    - Method: GET `/investors?registration_date=<YYYY-MM-DD>`    
- Retrieve a list of investors by account_balance:     
    - Method: GET `/investors?account_balance=<account_balance>`      
- CREATE investor:     
    - Method: POST /investors    
- Update investor:     
    - Method: PATCH `/investors/<investor_id>`    
- Delete investor:      
    - Method: DELETE `/investors/<investor_id>`    

Example: GET a single investor with output.  

![GET a single investor](<images/Example for GET a single investor.png>)  

#### stocks entity  

- Retrieve all stocks:     
    - Method: GET `/stocks`    
- Retrieve a single stock:       
    - Method: GET `/stocks/<stock_id>`    
- Retrieve a stock by ticker:     
    - Method: GET `/stocks?ticker=<ticker>`      
- Retrieve a stock by price:     
    - Method: GET `/stocks?price=<price>`   
- Retrieve a stock by account_balance:     
    - Method: GET `/stocks?account_balance=<account_balance>`     
- CREATE stock:     
    - Method: POST `/stocks`    
- Update stock:     
    - Method: PATCH `/stocks/<stock_id>`    
- Delete stock:      
    - Method: DELETE `/stocks/<stock_id>`    

Example: Get a stock by ticker with output.  

![Get a stock by ticker](<images/Get a stocker by ticker.png>)  

#### orders entity  

- Retrieve all orders:     
    - Method: GET `/orders`    
- Retrieve a single order:       
    - Method: GET `/orders/<order_id>`    
- Retrieve a list of orders by order_type:     
    - Method: GET `/orders?order_type=<order_type>`      
- Retrieve a list of orders by order_status:     
    - Method: GET `/orders?order_status=<order_status>`   
- Retrieve a list of orders by investor_id:     
    - Method: GET `/orders?investor_id=<investor_id>`   
- Retrieve a list of orders by stock_id:     
    - Method: GET `/orders?stock_id=<stock_id>`       
- CREATE order:     
    - Method: POST `/orders`    
- Update order:     
    - Method: PATCH `/orders/<order_id>`    
- Delete order:      
    - Method: DELETE `/orders/<order_id>`  

Example: Create order with output.

![Create order](<images/Create order.png>)

#### transactions entity  

- Retrieve all transactions:   
    - Method: GET `/transactions`  
- Retrieve a single transaction:     
    - Method:G ET `/transactions/<transaction_id>`  
- Retrieve a list of transactions by transaction_type:   
    - Method: GET `/transactions?transaction_type=<transaction_type>`   
- Retrieve a list of transactions by investor_id:   
    - Method: GET `/transactions?investor_id=<investor_id>` 
- Retrieve a list of transactions by order_id:   
    - Method: GET `/transactions?order_id=<order_id>`      
- CREATE transaction:   
    - Method: POST `/transactions`  
- Update transaction:   
    - Method: PATCH `/transactions/<transaction_id>`  
- Delete transaction:    
    - Method: DELETE `/transactions/<transaction_id>` 

Example: Update transaction with output.

![Update transaction](<images/Update transaction.png>)

#### portfolios entity  

- Retrieve all portfolios:   
    - Method: GET `/portfolios`  
- Retrieve a single portfolio:     
    - Method: GET `/portfolios/<portfolio_id>`     
- Retrieve a list of portfolios by investor_id:   
    - Method: GET `/portfolios?investor_id=<investor_id>` 
- Retrieve a list of portfolios by stock_id:   
    - Method: GET `/portfolios?stock_id=<stock_id>`      
- CREATE portfolio:   
    - Method: POST `/portfolios`  
- Update portfolio:   
    - Method: PATCH `/portfolios/<portfolio_id>`  
- Delete portfolio:    
    - Method: DELETE `/portfolios/<portfolio_id>` 

Example: Delete portfolio with output.  

![Delete portfolio](<images/Delete Portfolio.png>)  

#### watchlists entity
 
- Retrieve all watchlists:   
    - Method: GET `/watchlists`  
- Retrieve a single watchlist:     
    - Method: GET `/watchlists/<watchlist_id> `    
- Retrieve a watchlist by investor_id:   
    - Method: GET `/watchlists?investor_id=<investor_id> `
- Retrieve a list of watchlists by stock_id:   
    - Method: GET `/watchlists?stock_id=<stock_id>`      
- CREATE watchlist:   
    - Method: POST `/watchlists`  
- Update watchlist:   
    - Method: PATCH `/watchlists/<watchlist_id>`  
- Delete watchlist:    
    - Method: DELETE `/watchlists/<watchlist_id>` 

Example: Get all watchlists using Gunicorn.  

![Get all watchlists using Gunicorn](<images/Get all watchlist using Gunicorn.png>)
  
---

## License        

This project is licensed under the MIT License. Please see [LICENSE](https://github.com/TilleyCodes/web_api_server_assessment/blob/main/LICENSE) for more details.

---

## Database System

### Why PostgreSQL is the chosen database for this web API:  

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
