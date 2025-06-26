# datavista.py

import pandas as pd

# Load the dataset
df = pd.read_csv("ecommerce data.csv", encoding='ISO-8859-1')

# Display basic info
print("📊 Dataset Preview:")
print(df.head())

print("\n🧱 Dataset Shape (Rows, Columns):")
print(df.shape)

print("\n🧼 Dataset Info:")
print(df.info())
# Data cleaning

print("\n🔍 Checking for duplicate rows...")
duplicate_count = df.duplicated().sum()
print(f"→ Found {duplicate_count} duplicates.")

# Remove duplicates
df = df.drop_duplicates()
print("✅ Duplicates removed.\n")

print("🔍 Checking for missing values:")
print(df.isnull().sum())

# Drop rows with missing CustomerID (important field)
df = df.dropna(subset=['CustomerID'])

# Fill missing values in Description with 'Unknown'
df['Description'] = df['Description'].fillna('Unknown')

print("\n✅ Missing values handled.")

# Display updated shape
print("\n📦 Updated Dataset Shape:")
print(df.shape)

# Visualizations


import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure plots folder exists
os.makedirs("plots", exist_ok=True)

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create a Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.to_period('M')

# Monthly Sales Trend
monthly_sales = df.groupby('MonthYear')['Quantity'].sum()
monthly_sales.plot(kind='line', figsize=(10,5), marker='o')
plt.title("📅 Monthly Sales Trend")
plt.xlabel("Month-Year")
plt.ylabel("Quantity Sold")
plt.tight_layout()
plt.savefig("plots/monthly_sales.png")
plt.clf()  

#  Sales by Country
top_countries = df.groupby('Country')['Quantity'].sum().sort_values(ascending=False).head(10)
top_countries.plot(kind='bar', color='skyblue')
plt.title("🌍 Top 10 Countries by Quantity Sold")
plt.ylabel("Quantity")
plt.tight_layout()
plt.savefig("plots/top_countries.png")
plt.clf()

#Top 10 Customers by Revenue
df['Revenue'] = df['Quantity'] * df['UnitPrice']
top_customers = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind='bar', color='green')
plt.title("🧾 Top 10 Customers by Revenue")
plt.ylabel("Revenue (£)")
plt.tight_layout()
plt.savefig("plots/top_customers.png")
plt.clf()

#  Top 10 Most Returned Products
returns = df[df['Quantity'] < 0]
top_returns = returns['Description'].value_counts().head(10)
top_returns.plot(kind='barh', color='red')
plt.title("🔁 Top 10 Returned Products")
plt.xlabel("Return Count")
plt.tight_layout()
plt.savefig("plots/top_returns.png")
plt.clf()

#  Revenue per Product (Top 10)
product_revenue = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)
product_revenue.plot(kind='bar', color='purple')
plt.title("💸 Revenue per Product (Top 10)")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig("plots/revenue_per_product.png")
plt.clf()

print("\n📈 Visualizations created and saved in 'plots/' folder.")


#insights summary

os.makedirs("output", exist_ok=True)

with open("output/insights.txt", "w", encoding='utf-8') as file:
    file.write("📊 E-Commerce Data Analysis Summary\n")
    file.write("===================================\n\n")
    
    file.write(f"🧾 Total Records Analyzed: {len(df)}\n")
    file.write(f"🧑‍💼 Unique Customers: {df['CustomerID'].nunique()}\n")
    file.write(f"🌍 Countries Involved: {df['Country'].nunique()}\n")
    
    top_country = df['Country'].value_counts().idxmax()
    file.write(f"🏆 Country with Most Transactions: {top_country}\n\n")
    
    # Top Product
    top_product = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).idxmax()
    file.write(f"💡 Highest Revenue Product: {top_product}\n")
    
    # Month with highest sales
    top_month = df.groupby('MonthYear')['Quantity'].sum().idxmax()
    file.write(f"📅 Month with Highest Sales: {top_month}\n\n")

    file.write("📈 For more insights, check the charts in the 'plots/' folder.\n")
