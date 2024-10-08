import pandas as pd
from sqlalchemy import create_engine

# Replace these with your actual database credentials
username = 'root'   # Your MySQL username
password = 'Kd.128987550'     # Your MySQL password
host = 'localhost'             # Your MySQL server (localhost or IP)
database = 'sales_dashboard'   # Your database name

# Create a database engine
DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{database}'
engine = create_engine(DATABASE_URI)

# Function to fetch sales data
def fetch_sales_data():
    query = """
    SELECT fs.Product_id, fs.Sales_USD, fs.Quantity, fs.Price_USD, fs.COGS_USD, fs.Date_time, 
           a.Account_name, p.Product_Name, p.Produt_Type, 
           (fs.Sales_USD - fs.COGS_USD) AS Gross_Profit
    FROM fact_sales fs
    JOIN Accounts a ON fs.Account_id = a.Account_id
    JOIN Product p ON fs.Product_id = p.Product_Name_id
    """
    return pd.read_sql(query, engine)

# Function to fetch product data
def fetch_product_data():
    query = "SELECT * FROM Product"
    return pd.read_sql(query, engine)

# Function to fetch account data
def fetch_account_data():
    query = "SELECT * FROM Accounts"
    return pd.read_sql(query, engine)

# Fetch data
df_sales = fetch_sales_data()
df_product = fetch_product_data()
df_account = fetch_account_data()
