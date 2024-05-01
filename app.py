import streamlit as st
import pymysql
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Establish connection to MySQL database
conn = pymysql.connect(host='localhost', user='root', passwd='olamilekan1499', db='salesdatabase')
cursor = conn.cursor()


def get_product_ids():
    cursor.execute("SELECT ProductID FROM Products")
    return [row[0] for row in cursor.fetchall()]

# Function to generate a random date between start_date and end_date
def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to insert a new sale into the database
def insert_sale(product_id, quantity, price):
    sale_date = generate_random_date(start_date, end_date)
    total_sale = quantity * price
    cursor.execute("""
        INSERT INTO Sales (ProductID, Quantity, SaleDate, Price, TotalSale)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, quantity, sale_date, price, total_sale))
    conn.commit()

# Function to generate and insert sales data
def generate_and_insert_sales(num_sales):
    product_ids = get_product_ids()
    # product_prices = {1: 19.99, 2: 29.99, 3: 39.99}  # Corresponding prices
    for _ in range(num_sales):
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        price = random.uniform(10, 100)
        insert_sale(product_id, quantity, price)


# Function to plot total sales quantity for each product
def plot_total_sales_quantity_per_product():
    query = """
        SELECT ProductID, SUM(Quantity) as TotalQuantity
        FROM Sales
        GROUP BY ProductID
        ORDER BY TotalQuantity DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ProductID', 'TotalQuantity'])

    plt.figure(figsize=(10, 6))
    plt.bar(df['ProductID'], df['TotalQuantity'])
    plt.title('Total Sales Quantity Per Product')
    plt.xlabel('Product ID')
    plt.ylabel('Total Quantity')
    plt.tight_layout()
    st.pyplot(plt)

# Function to plot total sales per month
def plot_total_sales_per_month():
    query = """
        SELECT DATE_FORMAT(SaleDate, '%Y-%m') as Month, SUM(TotalSale) as TotalSales
        FROM Sales
        GROUP BY Month
        ORDER BY Month;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Month', 'TotalSales'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['Month'], df['TotalSales'], marker='o')
    plt.title('Total Sales Per Month')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Function to plot profit per product
def plot_profit_per_product():
    query = """
        SELECT Sales.ProductID, (SUM(Sales.TotalSale) - SUM(Sales.Quantity * Products.Price)) as Profit
        FROM Sales
        JOIN Products ON Sales.ProductID = Products.ProductID
        GROUP BY Sales.ProductID;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ProductID', 'Profit'])

    plt.figure(figsize=(10, 6))
    plt.bar(df['ProductID'], df['Profit'])
    plt.title('Profit Per Product')
    plt.xlabel('Product ID')
    plt.ylabel('Profit')
    plt.tight_layout()
    st.pyplot(plt)

# Start and end dates for sales data
start_date = datetime(2023, 1, 1)  
end_date = datetime(2023, 12, 30)  

# Sidebar options
st.sidebar.title("Select option")
generate_data = st.sidebar.button("Generate Data")
delete_data = st.sidebar.button("Delete Data")

if generate_data:
    generate_and_insert_sales(200)

if delete_data:
    cursor.execute("DELETE FROM Sales")
    conn.commit()
    st.success("Sales data deleted successfully!")

st.title('Click on any options below')
if st.button('View Summary of sales'):
    query_summary = """ SELECT ProductID, SUM(Quantity) as TotalQuantity, SUM(TotalSale) as TotalSales
                FROM Sales
                GROUP BY ProductID
                ORDER BY TotalSales DESC;
                    
                """
    cursor.execute(query_summary)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ProductID', 'TotalQuantity', 'TotalSales'])
    st.title("Summary of Sales")
    st.table(df)

if st.button('Visualize the data'):
    st.title("Sales Data Analysis")

    st.subheader("Total Sales Quantity Per Product")
    plot_total_sales_quantity_per_product()

    st.subheader("Total Sales Per Month")
    plot_total_sales_per_month()

    st.subheader("Profit Per Product")
    plot_profit_per_product()

# Close cursor and connection
cursor.close()
conn.close()
