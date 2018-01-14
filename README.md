# SQL-project-00-DA

### [Contents] 

__Case-01.__ Northwind-SQLite3 Data set
  - encoding: cp1252 

__Case-02.__ 
  - func: 
-------------------------------------------------------------------------------------------------------------------------------------  
#### >Case-01.
  
__Data:__ Northwind-SQLite3 Data set

This is a version of the Microsoft Access 2000 Northwind sample database, re-engineered for SQLite3. It was provided with Microsoft Access as a tutorial schema for managing small business customers, orders, inventory, purchasing, suppliers, shipping, and employees. All the TABLES and VIEWS from the MSSQL-2000 version have been converted to Sqlite3 and included here. Also included are two versions prepopulated with data - a small verison and a large version. Should you decide to, you can use the included python script to pump the database full of more data.

<img src="https://user-images.githubusercontent.com/31917400/33221409-2b39887a-d147-11e7-99bf-b19ffe2c36de.jpg" />


__Story:__ You’re a business intelligence analyst for a wholesaler of various food products. You’re in charge of putting together analytics dashboards for management. They have requested that you focus on one area of the business and create a dashboard that provides various summary statistics related to that area. For Each of the following area, create a presentation with visualizations that provides high level summary information about that area.
 - Customers
 - Suppliers
 - Products
 - Employees

### Possible Questions to guide our analysis:
 - 1) Customers_section
   - _Where are my customers located?
   - _How much money is being spent by customers in each country on average ?
   - _Which shipping companies customers have used in each country ? 
   - _When, how often, how much freight was ordered by the shipments from the specific country ?
   - _Show by percentage, what country is bringing most profit?
   - _For customer appreciation day, we are going to call our top customers and state our appreciation. Number of orders placed (OrderIDs) will be our determining factor for top customers to recognize for this event. Which customer has the maximum number of orders ? 
   - _Which customers in each country made more than the average number of orders?

 - 2) Suppliers_section
   - _How many supplier’s discontinued products were ordered and what’s the loss we could get? 
   - _What companies supply the majority of the products we sell?

 - 3) Products_section
   - _What products, product categories are growing in terms of sales? (advanced)

 - 4) Employees_section
   - _Which employees have sold to customers in the same city that they live in ?
   - _How many days on average does it take for each country from a placed order until for it to be shipped? Is there any relationship between this processing time and employees’ performance? 
   - _Which employee has the most shipped orders before or on required date and how long they have worked ?? 
   
### Q1. Where are my customers located? And how much money is being spent by customers in each country on average ?
 - It seems that most of our trades are occurring in Europe and America. 
 - Germany, USA, Brazil, France, Austria are the major countries where most of our customers are located and seemingly their average spend is directly proportional to the size of customer.  
```
SELECT Country, count(*), avg(od.UnitPrice*od.Quantity*(1 - od.Discount)) avg_spent
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
JOIN OrderDetails od
ON o.OrderID = od.OrderID
GROUP BY Country
ORDER BY avg_spent DESC
```
<img src="https://user-images.githubusercontent.com/31917400/34425618-661e5d00-ec25-11e7-9b6b-53ec5d671642.jpg" width="600" height="350" />

### Q2. Which shipping companies customers have used in each country ? When, how often, how much freight was ordered by the shipments from the specific country ?
 - It seems that all 3 shipping companies are used in each country but particularly, in USA, ‘Speedy Express’ is losing ground to others.
 - In major countries – Brazil, France, Germany, USA – the shipments are fluctuating from month to month.    
```
SELECT c.Country, c.CompanyName, o.OrderDate, s.CompanyName, count(o.ShipVia) freq, sum(o.Freight) total_freight
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
JOIN Shippers s
ON o.ShipVia = s.ShipperID
GROUP BY c.Country, s.CompanyName, o.OrderDate, s.CompanyName
```
<img src="https://user-images.githubusercontent.com/31917400/34425622-6e11b0b6-ec25-11e7-8ef0-d16bd6a17720.jpg" width="600" height="350" />

### Q3. Show by percentage what country is bringing most profit?
 - Although the average spending of USA is not the biggest, this country is taking up the largest in total profit and percentage.  
```
WITH t1 AS (
SELECT sum(UnitPrice*Quantity) AS total_profit
FROM OrderDetails od
JOIN Orders o
ON od.OrderID = o.OrderID),

t2 AS (
SELECT sum(UnitPrice*Quantity) AS profit_by_country, ShipCountry AS country
FROM OrderDetails od
JOIN Orders o
ON od.OrderID = o.OrderID
GROUP BY country)

SELECT country, profit_by_country, (profit_by_country/total_profit) AS percentage
FROM t2
JOIN t1
ORDER BY percentage DESC;
```
<img src="https://user-images.githubusercontent.com/31917400/34425623-72ae6128-ec25-11e7-8c6a-05ffbd9efbca.jpg" width="300" height="250" />

### Q4. Which customer has the maximum number of orders ? and which customers in each country made more than the average number of orders?
 - In the bar-chart above, ‘Save-a-lot Market’ is the company who has the maximum number of orders. 
 - Those are the companies all above the average number of orders (9.4)  
```
SELECT c.Country, c.CompanyName, c.Phone, count(o.OrderID) num_orders
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
ORDER BY num_orders DESC

WITH t1 AS 
(SELECT c.Country, c.CompanyName, c.Phone, count(o.OrderID) num_orders
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID)

SELECT Country, CompanyName, Phone, num_orders
FROM t1
GROUP BY CompanyName, Country
HAVING num_orders > 9.3258
ORDER BY num_orders DESC
```
<img src="https://user-images.githubusercontent.com/31917400/34425626-7781df72-ec25-11e7-888f-41da51f4b175.jpg" width="600" height="350" />
















































