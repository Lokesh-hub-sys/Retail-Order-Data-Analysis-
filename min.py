import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Caching the database connection
@st.cache_resource
def connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="loki",
            user="postgres",
            password="Lokesh#7"
        )
        return conn
    except Exception as e:
        st.error(f'Failed to connect to the database: {e}')
        return None

# Running a query
def run_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description] if cursor.description else []
        return pd.DataFrame(results, columns=colnames)
    except Exception as e:
        st.error(f"Error running query: {e}")
        return pd.DataFrame()

# Establish database connection
conn = connection()
if not conn:
    st.stop()

# Streamlit UI
st.title("Retail Order Data Analyst Mini Project")
choice = st.sidebar.radio("**Hello everyone :sunglasses: and welcome to my menu**", ("Guvi Query📊", "Own Query📈"))

# Queries Dictionary
guvi_queries = {
    "1. Find top 10 highest revenue generating products": """
        SELECT o.category, s.product_id, CAST(SUM(s.sale_price * s.quantity) AS INT) AS total_revenue
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.category, s.product_id
        ORDER BY total_revenue DESC LIMIT 10;
    """,
    "2. Find the top 5 cities with the highest profit margins": """
        SELECT o.city, SUM(s.profit) AS total_profit
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.city
        ORDER BY total_profit DESC LIMIT 5;
    """,
    "3. Calculate the total discount given for each category": """
        SELECT o.category, CAST(SUM(s.discount * s.quantity) AS INT) AS total_discount
        FROM order_details AS o
        JOIN sales_details AS s ON s.order_id = o.order_id
        GROUP BY o.category;
    """,
    "4. Find the average sale price per product category": """
        SELECT o.category, CAST(AVG(s.sale_price) AS REAL) AS avg_sale_price
        FROM order_details AS o
        JOIN sales_details AS s ON s.order_id = o.order_id
        GROUP BY o.category ORDER BY avg_sale_price DESC;
    """,
    "5. Find the region with the highest average sale price": """
        SELECT o.region, CAST(AVG(s.sale_price) AS REAL) AS avg_sale_price
        FROM order_details AS o
        JOIN sales_details AS s ON s.order_id = o.order_id
        GROUP BY o.region ORDER BY avg_sale_price DESC;
    """,
    "6. Find the total profit per category": """
        SELECT o.category, CAST(SUM(s.profit) AS REAL) AS total_profit
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.category;
    """,
    "7. Identify the top 3 segments with the highest quantity of orders": """
        SELECT o.category, o.segment, SUM(s.quantity) AS highest_quantity_orders
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.segment, o.category
        ORDER BY highest_quantity_orders DESC LIMIT 3;
    """,
    "8. Determine the average discount percentage given per region": """
        SELECT o.region, AVG(s.discount_percent) AS avg_discount_percentage
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.region;
    """,
    "9. Find the product category with the highest total profit": """
        SELECT o.category, SUM(s.profit) AS total_profit
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.category
        ORDER BY total_profit DESC LIMIT 1;
    """,
    "10. Calculate the total revenue generated per year": """
        SELECT EXTRACT(YEAR FROM o.order_date) AS year, CAST(SUM(s.sale_price * s.quantity) AS INT) AS total_revenue
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY year ORDER BY year;
    """
}

own_queries = {
    "1. Identify the top-selling product in each region": """
        SELECT o.region, o.category, CAST(SUM(s.quantity * s.sale_price) AS INT) AS total_sales
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY region, category
        ORDER BY total_sales DESC LIMIT 10;
    """,
    "2. Calculate the total revenue generated per month": """
        SELECT EXTRACT(MONTH FROM o.order_date) AS month, CAST(SUM(s.sale_price * s.quantity) AS INT) AS total_revenue
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY month ORDER BY month;
    """,
    "3. Find the Top-Selling Products by Category": """
        SELECT o.category, SUM(s.quantity) AS top_sales
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.category ORDER BY top_sales DESC;
    """,
    "4. Find the Yearly Profit Analysis": """
        SELECT EXTRACT(YEAR FROM o.order_date) AS year, CAST(SUM(s.profit) AS INT) AS total_profit
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY year;
    """,
    "5. Calculate Order Count by Region": """
        SELECT o.region, SUM(s.quantity) AS order_count
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.region;
    """,
    "6. What Are Products with Discounts Above 3%": """
        SELECT o.category, s.discount_percent
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        WHERE s.discount_percent > 3 AND s.discount_percent IS NOT NULL
        GROUP BY s.discount_percent, o.category ORDER BY s.discount_percent;
    """,
    "7. Find the Low-Revenue Products below 1 Lakh": """
        SELECT o.sub_category, CAST(SUM(s.sale_price * s.quantity) AS INT) AS total_revenue
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.sub_category HAVING SUM(s.sale_price * s.quantity) < 100000 ORDER BY total_revenue ASC;
    """,
     "8. Find the top 10 order_id who generated the highest total revenue": """
        SELECT o.order_id, CAST(SUM(s.sale_price * s.quantity) AS INT) AS total_revenue
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.order_id
        ORDER BY total_revenue DESC LIMIT 10;
    """,
    "9. Calculate the total amount of discount in all months": """
        SELECT EXTRACT(MONTH FROM o.order_date) AS month, CAST(SUM(s.discount) AS INT) AS discount_amount
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY month
        ORDER BY month;
    """,
    "10. Calculate the average discount percentage for each region": """
        SELECT o.region, ROUND(AVG(s.discount_percent), 2) AS avg_discount_percent
        FROM sales_details AS s
        JOIN order_details AS o ON o.order_id = s.order_id
        GROUP BY o.region;
    """,
    "11. Find the region with the highest average sale price": """
        SELECT o.region, CAST(AVG(s.sale_price) AS REAL) AS avg_sale_price
        FROM order_details AS o
        JOIN sales_details AS s ON s.order_id = o.order_id
        GROUP BY o.region
        ORDER BY avg_sale_price DESC LIMIT 1;
    """
}

# Select appropriate queries
queries = guvi_queries if choice == "Guvi Query📊" else own_queries
selected_query = st.selectbox("**Select Query**", list(queries.keys()))
query = queries[selected_query]

# Run and display results
data = run_query(conn, query)
if not data.empty:
    st.subheader(f"Results for: {selected_query}")
    st.dataframe(data)

    # Add download button
    st.download_button(
        label="Download data as CSV",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name=f'{selected_query}.csv',
        mime='text/csv'
    )

    # Visualization Type Selection
    chart_type = st.selectbox(
        "**Choose Visualization Type**",
        ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot", "Heatmap"]
    )

    # Visualization Logic
    if chart_type == "Line Chart":
        st.line_chart(data.set_index(data.columns[0]))
    elif chart_type == "Bar Chart":
        st.bar_chart(data.set_index(data.columns[0]))
    elif chart_type == "Area Chart":
        st.area_chart(data.set_index(data.columns[0]))
    elif chart_type == "Scatter Plot":
        fig = px.scatter(data, x=data.columns[0], y=data.columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Pie Chart":
        fig = px.pie(data, names=data.columns[0], values=data.columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Histogram":
        fig = px.histogram(data, x=data.columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Box Plot":
        fig = px.box(data, x=data.columns[0], y=data.columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Heatmap":
        numeric_data = data.select_dtypes(include='number')
        if numeric_data.shape[1] > 1:
            fig, ax = plt.subplots()
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Not enough numeric columns for Heatmap.")
else:
    st.warning("No data returned for this query.")

st.write("Thank you for exploring! 🎉")
