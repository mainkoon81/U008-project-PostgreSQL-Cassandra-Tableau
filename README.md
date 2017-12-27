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
   
### Q1. 

