-- CREATE DATABASE IF NOT EXISTS salesdatabase;

USE salesdatabase;

DROP TABLE IF EXISTS Sales;

DROP TABLE IF EXISTS Products;

CREATE TABLE Products (
    ProductID int AUTO_INCREMENT PRIMARY KEY,
    Name varchar(255),
    Category varchar(255),
    Price decimal(10, 2)
);

INSERT INTO Products (Name, Category, Price) VALUES 
    ('Product 1', 'Category A', 19.99),
    ('Product 2', 'Category B', 29.99),
    ('Product 3', 'Category C', 39.99);

CREATE TABLE Sales (
    SaleID int AUTO_INCREMENT PRIMARY KEY,
    ProductID int,
    Quantity int,
    SaleDate datetime,
    Price decimal(10, 2),
    TotalSale decimal(10, 2),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


SELECT DATE(SaleDate) as SaleDay, SUM(TotalSale) as TotalSales
FROM Sales
GROUP BY SaleDay
ORDER BY SaleDay;

SELECT ProductID, SUM(Quantity) as TotalQuantity
FROM Sales
GROUP BY ProductID
ORDER BY TotalQuantity DESC;

SELECT DATE_FORMAT(SaleDate, '%Y-%m') as Month, SUM(TotalSale) as TotalSales
FROM Sales
GROUP BY Month
ORDER BY Month;


SELECT Sales.ProductID, (SUM(Sales.TotalSale) - SUM(Sales.Quantity * Products.Price)) as Profit
FROM Sales
JOIN Products ON Sales.ProductID = Products.ProductID
GROUP BY Sales.ProductID;




