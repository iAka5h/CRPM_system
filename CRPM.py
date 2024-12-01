import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Establish database connection
conn = pymysql.connect(
    host="localhost",
    user="root",  
    password="root",  
    port=3306,
    database='CRPM_System1'
)
cursor = conn.cursor()

# Create Tables
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            Email VARCHAR(255) UNIQUE NOT NULL,
            Phone VARCHAR(15) NOT NULL,
            Status VARCHAR(50) DEFAULT 'Active'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            Price DECIMAL(10, 2) NOT NULL,
            Stock INT NOT NULL,
            Status VARCHAR(50) DEFAULT 'Active'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Purchases (
            PurchaseID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT NOT NULL,
            ProductID INT NOT NULL,
            Quantity INT NOT NULL,
            TotalCost DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    ''')
    conn.commit()

# Call the function to create tables
create_tables()

# Streamlit
#set up page configuration for streamlit
icon='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScwOS_5ho-eMIg6J6HbGMZ25PxC_CcpJPdMg&s'
st.set_page_config(page_title='CRPM_System', page_icon=icon,initial_sidebar_state='expanded', layout='wide')
                        
st.title("Customer Relationship and Product Management System")

# Add background image
def add_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image URL
add_background_image("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHCBIHBggQBgYGDQsPBgYHCw8ICQYWFREWFhURExMYHSggGBolGxMTITEhJSkrLi4uFx8zODMsNygtLisBCgoKDQ0NEg0NFSsZFRkrKysrKzcrKy0rKysrKzcrKysrKys3KysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAKgBKwMBEQACEQEDEQH/xAAWAAEBAQAAAAAAAAAAAAAAAAAAAQf/xAAWEAEBAQAAAAAAAAAAAAAAAAAAEQH/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAQL/xAAVEQEBAAAAAAAAAAAAAAAAAAAAAf/aAAwDAQACEQMRAD8Aw5GgBUAUABFIAAAAAoggAACiogKgigAAAAKoggCioIAAAoqCKKAiIKACKACCigIIKoCgAIACoIAAAAIoAAAAIKAAKKggACigAAAIIAooAIgAAAAAAAAKAKCIAACoCqiAAqAAAAKKggCigAAAIgKiooAACKgiqoAAAggACigAAAIIoqCAKKggAAAAACigAiAAAoICooAAAoAAAIACgCCKAKAAiCqIIoqCAKKggAAAACigAIIAAAqKAUBQAQFABAAAAVERQFABAVQQFRAVFRUAEBQAABRQEEAAUUBBFRUBQAFAAABAABAVQAQQFAAAAUQRRQAEEAAAAUVBAFFAAAEAAAAABQAAQAAAAQFUQQBUVFRUUVAAVBBFVRBAAFFAQRRQARAAVFAFQRQABRBFRQAAAABQBBAFAAAFAEAEVAFFQQARRUAUEAAABUUBFRUUAAUQRUUAAAUAEAAAAEVAFBEVQARUAAAAAAAAAAUEBUUBFRUUAAUAEABUQFRRQRAUAAAUAAREBRUAVFFEEAAAAAAUVBAFRQEVFFEABQAQFQAFAAAAEABQAQFERAVVARAAAUVBAAAAAAAFBAUEBUUAUAAAAAQRUEFUAABQBEFBFRUUAVEAAAAABRQEEAAAAAUVBFRQBQAAQFAAEEVAVRAgAAAAIqKiiiCCKAAKgCigAAIIAAqKKAIIqKAiooogAKAACAIKAogAAAAKIgCKoiKAAAKgAACggAAKjQqAAgigIqKKIAAAACgIAgAKKIAAACiCAAAKgCoqAAAAAAAKiiggBAABQQFBAAAAAAUBAEBRQABAAAUABAUAABBAAAAAFRQBUEUAAUEABQAAQFBAERQRRUAUAUAAABEFAAUAAAQQAAABRRBFRUUFNEooAICgAgQEBQFQRQBUQAFAFAAEAAAABQQFEEAAAAVFARUVFBTRKAKCAAAAAAoIAAIqKCAIoCqiAoAoAgKAAIgKgACigCAqAACKAKACAAAAAoIAAAIqKCAAoACCAooAqAqIKCAKiggAKK//2Q==")





select= option_menu(None,
                        options=["Users", "Products", "Purchases", "Insights"],
                        icons = ["house","bar-chart","toggles","at"],
                        default_index=0,
                        orientation="horizontal",
                        styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#0080FF"}}
                                 )

# Customer Management
if select == "Users":
    st.subheader("Customer Management")
    action = st.radio("Action", ["Add Customer", "View Customers", "Update Customer", "Delete Customer"])
    
    if action == "Add Customer":
        with st.form("Add Customer"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            submit = st.form_submit_button("Add")
            if submit:
                cursor.execute("INSERT INTO Customers (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
                conn.commit()
                st.success("Customer added successfully!")
    
    elif action == "View Customers":
        data = pd.read_sql_query("SELECT * FROM Customers", conn)
        st.dataframe(data)
    
    elif action == "Update Customer":
        customer_id = st.number_input("Enter Customer ID", min_value=1)
        with st.form("Update Customer"):
            name = st.text_input("New Name")
            email = st.text_input("New Email")
            phone = st.text_input("New Phone")
            submit = st.form_submit_button("Update")
            if submit:
                cursor.execute("UPDATE Customers SET Name = %s, Email = %s, Phone = %s WHERE CustomerID = %s", (name, email, phone, customer_id))
                conn.commit()
                st.success("Customer updated successfully!")
    
    elif action == "Delete Customer":
        customer_id = st.number_input("Enter Customer ID to Delete", min_value=1)
        if st.button("Delete"):
            cursor.execute("UPDATE Customers SET Status = 'Inactive' WHERE CustomerID = %s", (customer_id,))
            conn.commit()
            st.success("Customer deactivated successfully!")

# Product Management
elif select == "Products":
    st.subheader("Product Management")
    action = st.radio("Action", ["Add Product", "View Products", "Update Product", "Delete Product"])
    
    if action == "Add Product":
        with st.form("Add Product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.0)
            stock = st.number_input("Stock", min_value=0)
            submit = st.form_submit_button("Add")
            if submit:
                cursor.execute("INSERT INTO Products (Name, Price, Stock) VALUES (%s, %s, %s)", (name, price, stock))
                conn.commit()
                st.success("Product added successfully!")
    
    elif action == "View Products":
        data = pd.read_sql_query("SELECT * FROM Products", conn)
        st.dataframe(data)
    
    elif action == "Update Product":
        product_id = st.number_input("Enter Product ID", min_value=1)
        with st.form("Update Product"):
            name = st.text_input("New Product Name")
            price = st.number_input("New Price", min_value=0.0)
            stock = st.number_input("New Stock", min_value=0)
            submit = st.form_submit_button("Update")
            if submit:
                cursor.execute("UPDATE Products SET Name = %s, Price = %s, Stock = %s WHERE ProductID = %s", (name, price, stock, product_id))
                conn.commit()
                st.success("Product updated successfully!")
    
    elif action == "Delete Product":
        product_id = st.number_input("Enter Product ID to Delete", min_value=1)
        if st.button("Delete"):
            cursor.execute("UPDATE Products SET Status = 'Inactive' WHERE ProductID = %s", (product_id,))
            conn.commit()
            st.success("Product deactivated successfully!")

# Customer Purchases
elif select == "Purchases":
    st.subheader("Customer Purchases")
    action = st.radio("Action", ["Record Purchase", "View Purchase History"])
    
    if action == "Record Purchase":
        with st.form("Record Purchase"):
            customer_id = st.number_input("Customer ID", min_value=1)
            product_id = st.number_input("Product ID", min_value=1)
            quantity = st.number_input("Quantity", min_value=1)
            submit = st.form_submit_button("Record")
            if submit:
                cursor.execute("SELECT Price, Stock FROM Products WHERE ProductID = %s", (product_id,))
                product = cursor.fetchone()

                if product and product[1] >= quantity:
                    total_cost = product[0] * quantity
                    cursor.execute("INSERT INTO Purchases (CustomerID, ProductID, Quantity, TotalCost) VALUES (%s, %s, %s, %s)", (customer_id, product_id, quantity, total_cost))
                    cursor.execute("UPDATE Products SET Stock = Stock - %s WHERE ProductID = %s", (quantity, product_id))
                    conn.commit()
                    st.success("Purchase recorded successfully!")
                else:
                    st.error("Insufficient stock!")
    
    elif action == "View Purchase History":
        customer_id = st.number_input("Enter Customer ID", min_value=1)
        data = pd.read_sql_query("SELECT * FROM Purchases WHERE CustomerID = %s", conn, params=(customer_id,))
        st.dataframe(data)

# Analytics and Reports
elif select == "Insights":
    st.subheader("Analytics and Reports")
    option = st.radio("Select Report", ["Sales Report", "Top Customers", "Product Performance"])
    
    if option == "Sales Report":
        sales = pd.read_sql_query("SELECT SUM(TotalCost) as Revenue, COUNT(*) as TotalSales FROM Purchases", conn)
        st.write(sales)
    
    elif option == "Top Customers":
        top_customers = pd.read_sql_query("SELECT CustomerID, SUM(TotalCost) as TotalSpent FROM Purchases GROUP BY CustomerID ORDER BY TotalSpent DESC LIMIT 5", conn)
        st.dataframe(top_customers)
    
    elif option == "Product Performance":
        product_perf = pd.read_sql_query("SELECT ProductID, SUM(Quantity) as TotalSold FROM Purchases GROUP BY ProductID ORDER BY TotalSold DESC", conn)
        st.bar_chart(product_perf.set_index("ProductID"))

