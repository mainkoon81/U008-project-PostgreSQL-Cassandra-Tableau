### [Contents] 

__Case-01.__ Northwind-SQLite3 Dataset
  - encoding: cp1252 
  - Summary: SQL-Queries and visualization 

__Case-02.__ 
  - Summary: Define `fact` and `dimension` tables for a **star schema** for a particular analytic focus, and write an **ETL pipeline** that transfers data from [files in two local directories] into [these tables] in Postgres using Python and SQL.
-------------------------------------------------------------------------------------------------------------------------------------  
#### >Case-01.

__Data:__ Northwind-SQLite3 Dataset

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
### Q5. How many supplier’s discontinued products were ordered and what’s the loss we could get? 
 - Plutzer’s discontinued product -Thringer and Rssie - are ordered the most often , accordingly, we can expect some loss.  
```
SELECT p.ProductName, s.CompanyName, o.OrderID, SUM(p.Discontinued) No_More, SUM(o.UnitPrice*o.Quantity*(1 - o.Discount)) Loss
FROM Products p
JOIN Suppliers s
ON p.SupplierID = s.SupplierID
JOIN OrderDetails o
ON p.ProductID = o.ProductID
WHERE p.Discontinued = 1
Group by p.ProductName, s.CompanyName, o.OrderID
```
<img src="https://user-images.githubusercontent.com/31917400/34916038-d05abf78-f928-11e7-8ecf-4c2680c241e6.jpg" width="600" height="300" />
### Q6. Which employees have sold to customers in the same city that they live in ?
 - It turns out there are only two country where our staff can offer offline service – USA & UK. Callahan and Davolio in Seatle, USA and the rest in London, UK. 
```
SELECT DISTINCT e.LastName, e.Title, e.City, c.CompanyName
FROM Employees e
JOIN Orders o
ON e.EmployeeID = o.EmployeeID 
JOIN Customers c
ON c.CustomerID = o.CustomerID
WHERE c.City = e.City
ORDER BY 1
```
<img src="https://user-images.githubusercontent.com/31917400/34916041-d8915aa8-f928-11e7-9ebc-eba39937046e.jpg" width="600" height="300" />
### Q7. How many days on average does it take for each country from a placed order until for it to be shipped? Is there any relationship between this processing time and employees’ performance? 
 - The visual left shows average processing time by each Staff ID and country. The visual right shows average processing time by country but in a bubble diagram.  
```
SELECT ShipCountry, EmployeeID, avg(julianday(OrderDate) - julianday(ShippedDate)) avg_process 
FROM Orders 
GROUP BY ShipCountry, EmployeeID
ORDER BY ShipCountry, avg_process;
```
<img src="https://user-images.githubusercontent.com/31917400/34916042-db52950e-f928-11e7-8584-4563bb365b1f.jpg" width="600" height="810" />
#### >Case-02.
__Data:__ Million Song Dataset + Log Dataset
 - Song Dataset: The first dataset is a subset of real data from the **Million Song Dataset**(http://millionsongdataset.com/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```
Below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```
 - Log Dataset: The second dataset consists of log files in JSON format generated by this **event simulator**(https://github.com/Interana/eventsim) based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations. The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset. 
```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```
Below is an example of what the data in a log file, 2018-11-12-events.json, looks like.
<img src="https://user-images.githubusercontent.com/31917400/65054431-733fdc00-d965-11e9-95fb-e12e5b6347a6.png" />

Look at the JSON data within **log_data** files:`df = pd.read_json('data/log_data/2018/11/2018-11-01-events.json', lines=True)`

__Story:__ A startup called "Sparkify" wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. My role is to create a database schema and ETL pipeline for this analysis.

__Schema for this task:__ Create a star schema optimized for queries on song play analysis. This includes the following tables.
 - `Fact Table`
   - **songplays:** records in log data associated with song plays i.e. records with page NextSong
     - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

 - `Dimension Tables`
   - **users:** users in the app
     - user_id, first_name, last_name, gender, level
   - **songs:** songs in music database
     - song_id, title, artist_id, year, duration
   - **artists:** artists in music database
     - artist_id, name, location, latitude, longitude
   - **time:** timestamps of records in songplays broken down into specific units
     - start_time, hour, day, week, month, year, weekday
<img src="https://user-images.githubusercontent.com/31917400/65378294-3f8aec00-dcae-11e9-961c-8231e7736534.png" />



