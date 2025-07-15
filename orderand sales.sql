select * from order_details;
select * from sales_details;
alter table sales_details alter column profit type int;
alter table sales_details alter column discount type real;
alter table sales_details alter column sale_price type real;

alter table order_details add constraint pk_order_id primary key (order_id);
alter table sales_details add constraint fk_order_id foreign key (order_id) references order_details(order_id);
# --1.#Find top 10 highest revenue generating products
select o.category,s.product_id,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
from sales_details as s join order_details as o on o.order_id=s.order_id
group by o.category,s.product_id order by total_revenue desc limit 10;
# --2.#Find the top 5 cities with the highest profit margins
select o.city,sum(s.profit) as total_profit from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.city order by total_profit desc limit 5;

# --3.# Calculate the total discount given for each category
select o.category,cast(sum(s.discount*s.quantity)as int)as total_discount from order_details as o
join sales_details as s on s.order_id=o.order_id group by o.category ;

# --4.# Find the average sale price per product category
select o.category,cast(avg(s.sale_price)as real) as avg_sale_price from order_details as o
join sales_details as s on s.order_id=o.order_id group by o.category order by avg_sale_price desc;

# --5.# Find the region with the highest average sale price

select o.region,cast(avg(s.sale_price)as real) as avg_sale_price from order_details as o
join sales_details as s on s.order_id=o.order_id group by o.region order by region desc;

# --6.# Find the total profit per category
select o.category,cast(sum(s.profit)as real) as total_profit from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.category;

# --7.# Identify the top 3 segments with the highest quantity of orders
select o.category,o.segment,sum(s.quantity) as highest_quantity_orders from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.segment,o.category order by highest_quantity_orders desc limit 3;

# --8.# Determine the average discount percentage given per region
select o.region,avg(s.discount_percent)as avg_discount_percentage from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.region;

# --9.# Find the product category with the highest total profit
select o.category ,s.profit from sales_details as s
join order_details as o on o.order_id=s.order_id order by profit desc limit 1;

# --10.# Calculate the total revenue generated per year
select extract(year from o.order_date) as year,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
from sales_details as s join order_details as o on o.order_id=s.order_id group by year;

# --11 question from me
# --1.# Identify the top-selling product in each region
select o.region,o.category,cast(sum(s.quantity*s.sale_price)as int) as total_sales from sales_details as s
join order_details as o on o.order_id=s.order_id group by region,category order by total_sales desc limit 10;

# --2.# Calculate the total revenue generated per month
select extract(month from o.order_date) as month,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
from sales_details as s join order_details as o on o.order_id=s.order_id group by month order by month;

# --3.# Find the Top-Selling Products by Category
select o.category,sum(s.quantity) as top_sales from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.category order by top_sales desc ;

# --4.# Find the Yearly Profit Analysis
select extract(year from o.order_date)as year,cast(sum(s.profit)as int) as total_profit from sales_details as s
join order_details as o on o.order_id=s.order_id group by year;

# --5.# Calculate Order Count by Region
select o.region,sum(s.quantity) as order_count from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.region;

# --6# What Are Products with Discounts Above 3%
select o.category,s.discount_percent from sales_details as s
join order_details as o on o.order_id=s.order_id  where discount_percent >3
group by discount_percent,category order by discount_percent;

# --7# Find the Low-revenue Products below 1lack
select o.sub_category,cast(sum(s.sale_price * s.quantity)as int) as total_revenue from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.sub_category having sum(s.sale_price * s.quantity) < 100000 order by total_revenue asc

# --8#Find the top 10 order_id who generated the highest total revenue
select o.order_id,cast(sum(s.sale_price * s.quantity)as int) as total_revenue from sales_details as s
join order_details as o on o.order_id=s.order_id group by o.order_id order by total_revenue desc limit 10;

# --9#Calculate the total amount of discount in all month
select extract(month from o.order_date)as month ,cast(sum(s.discount)as int)as discount_amount from sales_details as s
join order_details as o on o.order_id=s.order_id group by month order by month;

# --10#Calculate the average discount percentage for each region.
select o.region, round(avg(s.discount_percent),2) as avg_discount_percent from sales_details as s
join order_details as o on o.order_id=s.order_id group by region;
# --11#for first highest average sale price in region
select o.region,cast(avg(s.sale_price)as real) as avg_sale_price from order_details as o
join sales_details as s on s.order_id=o.order_id group by o.region order by region desc limit 1;

