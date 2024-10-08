# Sales Dashboard in Python

This is a dynamic dashboard built using Python, Dash, and MySQL. It provides real-time visualizations of sales, gross profit (GP%), quantity sold, profit, and year-to-date (YTD) vs previous year-to-date (PYTD) comparisons. The data is fetched from a MySQL database.

## Features

- Product and country-level filtering.
- Dynamic time range selection.
- Interactive visualizations including Sales Over Time, Gross Profit %, Quantity Sold, Profit Over Time, and YTD vs PYTD comparisons.
- Custom styling with Bootstrap.

## Folder Structure

Here is the completion of the README.md and the .gitignore files:

7. README.md - Instructions for Setup
md
Copy code
# Sales Dashboard in Python

This is a dynamic dashboard built using Python, Dash, and MySQL. It provides real-time visualizations of sales, gross profit (GP%), quantity sold, profit, and year-to-date (YTD) vs previous year-to-date (PYTD) comparisons. The data is fetched from a MySQL database.

## Features

- Product and country-level filtering.
- Dynamic time range selection.
- Interactive visualizations including Sales Over Time, Gross Profit %, Quantity Sold, Profit Over Time, and YTD vs PYTD comparisons.
- Custom styling with Bootstrap.

## Folder Structure

├── app.py # Main application file 
├── callbacks.py # Callbacks to handle dynamic updates 
├── db_config.py # MySQL database connection 
├── queries.py # SQL queries for fetching data 
├── assets 
│ └── styles.css # Custom styles 
├── data # Folder to store any necessary data files 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation


## Prerequisites

Before running the dashboard, ensure that the following are installed:

1. **Python 3.x**: You can download it [here](https://www.python.org/downloads/).
2. **MySQL Server**: Make sure MySQL is installed and the required tables are populated.
3. **Pip**: Pip is included with Python installation. If not, install it from [here](https://pip.pypa.io/en/stable/installation/).

## Database Setup

1. Create the `sales_dashboard_db` database in MySQL.
2. Create the required tables (`fact_sales`, `accounts`, `product`) and import the data into MySQL using your `.csv` files.
3. Update the `db_config.py` file with your MySQL credentials.

```python
# db_config.py
import MySQLdb

def db_connection():
    conn = MySQLdb.connect(
        host='localhost',         # Change to your MySQL host
        user='your_user',          # Change to your MySQL username
        password='your_password',  # Change to your MySQL password
        db='sales_dashboard_db'    # Ensure the correct database name
    )
    return conn
