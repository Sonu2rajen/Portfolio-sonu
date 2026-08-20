select * from Dim_Customers;

select * from Fact_Orders;

-- how many orders has customrID 1 placed
select count(*) as OrderCount
from Fact_Orders
where CustomerID = 1;

-- delete customer with ID 1
delete from Dim_Customers
where CustomerID = 1;

-- This will FAIL because Product 999999 does not exist in Dim_Products
INSERT INTO Fact_OrderDetails (TransactionID, OrderID, ProductID, Quantity, UnitPrice)
VALUES (9999, 1001, 999999, 1, 500.00);

SELECT 
    od.TransactionID,
    od.OrderID,
    p.ProductName,
    p.Category,
    od.Quantity,
    od.UnitPrice
FROM Fact_OrderDetails od
INNER JOIN Dim_Products p 
    ON od.ProductID = p.ProductID;

SELECT 
    o.OrderID,
    c.FirstName,
    c.LastName,
    c.City,
    p.ProductName,
    od.Quantity,
    (od.Quantity * od.UnitPrice) AS TotalLineRevenue
FROM Fact_OrderDetails od
JOIN Fact_Orders o ON od.OrderID = o.OrderID
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
JOIN Dim_Products p ON od.ProductID = p.ProductID
ORDER BY TotalLineRevenue DESC;

-- Write a query that joins Fact_Orders and Dim_Customers.
-- Return a list of all OrderIDs alongside the Email and City of the customer who placed the order, but only for customers living in 'Johannesburg'.
-- How many orders were placed by customers in Johannesburg?
SELECT * FROM Dim_Customers;
SELECT * FROM Fact_Orders;
SELECT
    c.CustomerID,
    o.OrderID,
    c.Email,
    c.City
FROM Fact_Orders o
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
WHERE c.City = 'Johannesburg';

-- Revenue by Category
SELECT 
    p.Category,
    COUNT(od.TransactionID) AS Total_Transactions,
    SUM(od.Quantity * od.UnitPrice) AS Total_Revenue
FROM Fact_OrderDetails od
JOIN Dim_Products p ON od.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY Total_Revenue DESC;

-- Categories with Revenue > 10,000
SELECT 
    p.Category,
    SUM(od.Quantity * od.UnitPrice) AS Total_Revenue
FROM Fact_OrderDetails od
JOIN Dim_Products p ON od.ProductID = p.ProductID
GROUP BY p.Category
HAVING SUM(od.Quantity * od.UnitPrice) > 10000;

-- Day 27: Cities with more than 5 orders
SELECT 
    count(OrderID) as Total_Orders,
    c.City
FROM Fact_Orders o
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
GROUP BY c.City
HAVING count(OrderID) > 5
ORDER BY Total_Orders DESC;

-- Simplified Order Status
SELECT 
    OrderID,
    Status,
    CASE 
        WHEN Status = 'Delivered' THEN 'Success'
        WHEN Status = 'Shipped'   THEN 'In-Transit'
        WHEN Status = 'Returned'  THEN 'Revenue Loss'
        WHEN Status = 'Cancelled' THEN 'Void'
        ELSE 'Check System' -- This catches any new/typo statuses
    END AS OrderCategory
FROM Fact_Orders;


-- Customer Spending Tiers
SELECT 
    c.FirstName,
    c.LastName,
    SUM(od.Quantity * od.UnitPrice) AS TotalSpend,
    CASE 
        WHEN SUM(od.Quantity * od.UnitPrice) >= 5000 THEN 'Gold VIP'
        WHEN SUM(od.Quantity * od.UnitPrice) >= 1000 THEN 'Silver Regular'
        ELSE 'Bronze New'
    END AS CustomerTier
FROM Dim_Customers c
JOIN Fact_Orders o ON c.CustomerID = o.CustomerID
JOIN Fact_OrderDetails od ON o.OrderID = od.OrderID
GROUP BY c.FirstName, c.LastName
ORDER BY TotalSpend DESC;


SELECT * FROM Dim_Products;

-- Day 28: Count of Premium Products

SELECT 
    COUNT(*) AS NumberOfPremiumProducts
FROM (
    SELECT 
        p.ProductID,
        p.ProductName,
        p.Price,
        CASE
        WHEN p.Price >= 500 THEN 'Premium'
        WHEN p.Price >= 100 AND p.Price <= 499 THEN 'Mid-Range'
        ELSE 'Budget'
    END AS PriceCategory
        FROM Dim_Products p
    ) AS CategorizedProducts
WHERE PriceCategory = 'Premium';

-- ===============================================================================================================================

SELECT 
    OrderID,
    OrderDate,
    ShipDate,
    DATEDIFF(DAY, OrderDate, ShipDate) AS DaysToShip
FROM Fact_Orders
WHERE ShipDate IS NOT NULL
ORDER BY DaysToShip DESC;

SELECT 
    AVG(DATEDIFF(DAY, OrderDate, ShipDate)) AS AvgDaysToShip
FROM Fact_Orders
WHERE Status = 'Delivered'; -- We only measure success stories

SELECT 
    OrderID,
    OrderDate,
    YEAR(OrderDate) AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    DATENAME(MONTH, OrderDate) AS MonthName,
    DATENAME(WEEKDAY, OrderDate) AS DayOfWeek
FROM Fact_Orders;

SELECT 
    DATENAME(WEEKDAY, OrderDate) AS DayName,
    COUNT(OrderID) AS TotalOrders
FROM Fact_Orders
GROUP BY DATENAME(WEEKDAY, OrderDate)
ORDER BY TotalOrders DESC;

-- Find the orders with broken dates (188)
SELECT OrderID, OrderDate 
FROM Fact_Orders 
WHERE OrderDate IS NULL;

-- Replace the IDs below with the ones you found in Step 1
SELECT OrderID, OrderDate as RawDateString
FROM Raw_Orders
WHERE OrderID IN (1038, 1092, 1114); -- Example IDs

-- Find all strings that cannot be converted to a date (159)
SELECT DISTINCT OrderDate
FROM Raw_Orders
WHERE TRY_CAST(OrderDate AS DATE) IS NULL;

-- Testing the fix
SELECT 
    OrderDate AS Original,
    COALESCE(
        TRY_CAST(OrderDate AS DATE),             -- Try standard YYYY-MM-DD
        TRY_CONVERT(DATE, OrderDate, 105)        -- Try DD-MM-YYYY
    ) AS FixedDate
FROM Raw_Orders
WHERE TRY_CAST(OrderDate AS DATE) IS NULL;

-- Count every single occurrence of broken dates in the raw data
SELECT COUNT(OrderDate) AS TotalBrokenRows
FROM Raw_Orders
WHERE TRY_CAST(OrderDate AS DATE) IS NULL;

-- Proof: See which broken dates are the "Repeat Offenders"
SELECT OrderDate, COUNT(*) as NumberOfAffectedOrders
FROM Raw_Orders
WHERE TRY_CAST(OrderDate AS DATE) IS NULL
GROUP BY OrderDate
HAVING COUNT(*) > 1
ORDER BY NumberOfAffectedOrders DESC;

SELECT
    OrderID, 
	OrderDate, 
    ShipDate
FROM Fact_Orders
WHERE OrderDate IS NULL;

SELECT
    OrderID, 
	OrderDate, 
    ShipDate
FROM Raw_Orders
WHERE OrderID = 1038;

SELECT DISTINCT OrderDate
FROM Raw_Orders
WHERE TRY_CAST(OrderDate AS DATE) IS NULL;

-- The "Repair" Query
UPDATE f
SET f.OrderDate = COALESCE(
                    TRY_CAST(r.OrderDate AS DATE), 
                    TRY_CONVERT(DATE, r.OrderDate, 105)
                  )
FROM Fact_Orders f
JOIN Raw_Orders r ON f.OrderID = CAST(r.OrderID AS INT)
WHERE f.OrderDate IS NULL;

-- This should now return 0
SELECT COUNT(*) AS Remaining_Nulls
FROM Fact_Orders
WHERE OrderDate IS NULL;

SELECT 
    DATENAME(WEEKDAY, OrderDate) AS DayName,
    COUNT(OrderID) AS TotalOrders
FROM Fact_Orders
GROUP BY DATENAME(WEEKDAY, OrderDate)
ORDER BY TotalOrders DESC;

-- Day 29:
SELECT 
    DATENAME(MONTH, fo.OrderDate) AS MonthName,
    COUNT(fo.OrderID) AS TotalOrders,
    SUM(fod.Quantity * fod.UnitPrice) AS TotalRevenue
FROM Fact_Orders fo
INNER JOIN Fact_OrderDetails fod 
    ON fo.OrderID = fod.OrderID
WHERE DATENAME(MONTH, fo.OrderDate) = 'February'
GROUP BY DATENAME(MONTH, fo.OrderDate);

-- =============================================================================================================================
-- Day 30: Subqueries
-- The Outer query filters the products
SELECT ProductID, ProductName, Price
FROM Dim_Products
WHERE Price > (
    -- The Inner query calculates the average first
    SELECT AVG(Price) FROM Dim_Products
);


SELECT FirstName, LastName, Email
FROM Dim_Customers
WHERE CustomerID IN (
    SELECT DISTINCT CustomerID 
    FROM Fact_Orders 
    WHERE Status = 'Delivered'
);

-- We want to find "High Volume" transactions.
-- 1. Write a subquery to find the Average Quantity sold across all transactions in Fact_OrderDetails. 
-- 2. Use that subquery to filter a list of OrderID and ProductID from Fact_OrderDetails where the Quantity in that specific row is higher than the store average.

-- What is the TransactionID of the row with the highest quantity that passed this filter?
SELECT TOP 1
    OrderID, 
    ProductID, 
    Quantity
FROM Fact_OrderDetails
WHERE Quantity > (
    SELECT AVG(Quantity) FROM Fact_OrderDetails
)
ORDER BY Quantity DESC;
-- ==============================================================================================================================

-- Day 31: CTEs
-- The management team wants a "Daily Performance vs. Target" report.
-- 1. Create a CTE called DailyRevenue that calculates the total revenue per OrderDate from Fact_Orders and Fact_OrderDetails. 
-- 2. In your final query, use that CTE to find the Average Daily Revenue for the entire month of March.
-- What was the average daily revenue for March?
WITH DailyRevenue AS (
    SELECT 
        fo.OrderDate,
        SUM(fod.Quantity * fod.UnitPrice) AS TotalDailyRevenue
    FROM Fact_Orders fo
    JOIN Fact_OrderDetails fod ON fo.OrderID = fod.OrderID
    WHERE MONTH(fo.OrderDate) = 3 -- March
    GROUP BY fo.OrderDate
)
SELECT 
    AVG(TotalDailyRevenue) AS AvgDailyRevenue_March
FROM DailyRevenue;

-- ==============================================================================================================================
-- Day 32: Views
GO
-- 1. Create a View named v_MasterSalesSummary.

CREATE VIEW v_MasterSalesSummary AS
SELECT 
    o.OrderID,
    o.OrderDate,
    c.FirstName + ' ' + c.LastName AS CustomerName,
    c.City,
    p.ProductName,
    p.Category,
    od.Quantity,
    od.UnitPrice,
    (od.Quantity * od.UnitPrice) AS TotalRevenue,
    CASE 
        WHEN o.Status = 'Delivered' THEN 'Success'
        WHEN o.Status = 'Returned'  THEN 'Revenue Loss'
        ELSE 'Pending/Other'
    END AS RevenueStatus
FROM Fact_OrderDetails od
JOIN Fact_Orders o ON od.OrderID = o.OrderID
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
JOIN Dim_Products p ON od.ProductID = p.ProductID;

GO

SELECT * FROM v_MasterSalesSummary;
-- 1. Create a View named v_NairobiVIPs. 
-- 2. Inside this view, use the logic we wrote yesterday to identify customers in Nairobi who have a TotalRevenue (Quantity * UnitPrice) greater than $2,000.
-- Once the view is created, run SELECT COUNT(*) FROM v_NairobiVIPs. How many rows are returned?
GO

CREATE VIEW v_NairobiVIPs AS
SELECT 
    CustomerName,
    City,
    SUM(TotalRevenue) AS AggregateSpend -- We sum it up in case they have multiple orders
FROM v_MasterSalesSummary -- Notice we are using the view we created earlier!
WHERE City = 'Nairobi'
GROUP BY CustomerName, City
HAVING SUM(TotalRevenue) > 2000;

GO
-- 2. The Verification Query (The Answer)
SELECT COUNT(*) AS VIPCount FROM v_NairobiVIPs;

GO

CREATE VIEW v_LagosVIPs AS
SELECT 
    CustomerName,
    City,
    SUM(TotalRevenue) AS AggregateSpend -- We sum it up in case they have multiple orders
FROM v_MasterSalesSummary -- Notice we are using the view we created earlier!
WHERE City = 'Lagos'
GROUP BY CustomerName, City
HAVING SUM(TotalRevenue) > 2000;

GO
-- 2. The Verification Query (The Answer)
SELECT COUNT(*) AS VIPCount FROM v_LagosVIPs;

-- ==============================================================================================================================
-- Day 33:
-- Standardizing customer contact info
SELECT 
    LOWER(TRIM(Email)) AS CleanEmail, 
    UPPER(TRIM(City)) AS StandardCity
FROM Dim_Customers;

-- Cleaning up city abbreviations
SELECT 
    Email AS BrokenEmail,
    REPLACE(Email, 'gamil.com', 'gmail.com') AS FixedEmail
FROM Dim_Customers
WHERE Email LIKE '%gamil.com%';

-- Hunting for broken email structures
SELECT CustomerID, FirstName, Email
FROM Dim_Customers
WHERE Email NOT LIKE '%@%';

-- Repairing email domain typos
SELECT 
    Email AS BrokenEmail,
    REPLACE(Email, 'gamil.com', 'gmail.com') AS FixedEmail
FROM Dim_Customers
WHERE Email LIKE '%gamil.com%';

SELECT DISTINCT city from Dim_Customers;

SELECT CustomerID, Email 
FROM Dim_Customers 
WHERE Email LIKE '%gamil.com%';

UPDATE Dim_Customers
SET Email = REPLACE(Email, 'gamil.com', 'gmail.com')
WHERE Email LIKE '%gamil.com%';

-- Splitting the Transaction ID
SELECT 
    TransactionID,
    SUBSTRING(TransactionID, CHARINDEX('-', TransactionID) + 1, LEN(TransactionID)) AS NumericIDPart
FROM Fact_OrderDetails;

-- Extracting the 2nd segment (fe90) from the UUID
SELECT 
    TransactionID,
    -- 1. Find the first '-'
    -- 2. Move +1 position to start at 'f'
    -- 3. Grab exactly 4 characters
    SUBSTRING(TransactionID, CHARINDEX('-', TransactionID) + 1, 4) AS SegmentTwo
FROM Fact_OrderDetails;

select * from Fact_OrderDetails;

-- The IT department says that the last 12 characters of the TransactionID represent the "Server Node" that processed the sale.
-- 1. Use the RIGHT() function to extract the last 12 characters of the TransactionID. 2. Wrap that in UPPER() to ensure it looks like a serial number.
-- Write the query. What are the last 12 characters for the transaction associated with OrderID = 5967?
SELECT TOP 1
    OrderID,
    TransactionID,
    UPPER(RIGHT(TransactionID, 12)) AS ServerNode
FROM Fact_OrderDetails
WHERE OrderID = 5967;

-- ==============================================================================================================================
-- Day 34: The Integrity Audit & Ranking

WITH DuplicateFinder AS (
    SELECT 
        CustomerID, 
        FirstName, 
        LastName,
        Email,
        ROW_NUMBER() OVER(
            PARTITION BY CustomerID, FirstName, LastName 
            ORDER BY CustomerID
        ) AS Occurrence
    FROM Raw_Customers
)
SELECT * FROM DuplicateFinder 
WHERE Occurrence > 1;

-- Searching for "Ghost Duplicates" in Production
WITH IntegrityCheck AS (
    SELECT 
        CustomerID, 
        ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY CustomerID) AS Occurrence
    FROM Dim_Customers
)
SELECT * FROM IntegrityCheck WHERE Occurrence > 1;

-- Finding the most expensive product in each category
WITH RankedProducts AS (
    SELECT 
        Category, 
        ProductName, 
        Price,
        RANK() OVER(PARTITION BY Category ORDER BY Price DESC) AS PriceRank
    FROM Dim_Products
)
SELECT * FROM RankedProducts WHERE PriceRank = 1;

WITH RankedProducts AS (
    SELECT 
        Category, 
        ProductName, 
        Price,
        DENSE_RANK() OVER(PARTITION BY Category ORDER BY Price DESC) AS PriceRank
    FROM Dim_Products
)
SELECT * FROM RankedProducts WHERE PriceRank = 1;

-- The Sales Director wants to see the "Recent Activity" for every customer.
-- 1. Query the Fact_Orders table. 
-- 2. Use ROW_NUMBER() to partition by CustomerID and order by OrderDate DESCENDING. 
-- 3. Filter the result to show only the latest order for every customer (where Row Number = 1).
-- What is the OrderID and OrderDate of the most recent order placed by CustomerID = 421?

SELECT * FROM Fact_Orders;
WITH RecentOrders AS (
    SELECT 
        CustomerID,
        OrderID,
        OrderDate,
        ROW_NUMBER() OVER(
            PARTITION BY CustomerID 
            ORDER BY OrderDate DESC
        ) AS OrderRank
    FROM Fact_Orders
)
SELECT OrderID, OrderDate FROM RecentOrders WHERE CustomerID = 421 AND OrderRank = 1;

-- We want to identify the "First Sale" for every customer.
-- 1. Query the Fact_Orders table. 
-- 2. Use ROW_NUMBER() to partition by CustomerID and order by OrderDate (ASC). 
-- 3. Filter the result to show only the rows where the Row Number is 1.
-- What is the OrderID of the first-ever order placed by CustomerID = 500?
WITH FirstSales AS (
    SELECT 
        CustomerID,
        OrderID,
        OrderDate,
        ROW_NUMBER() OVER(
            PARTITION BY CustomerID 
            ORDER BY OrderDate ASC
        ) AS OrderRank
    FROM Fact_Orders
)
SELECT OrderID, OrderDate FROM FirstSales WHERE CustomerID = 500 AND OrderRank = 1;


-- ==============================================================================================================================
-- Day 35: Cumulative Analysis (Running Totals)
-- Daily Sales vs. Running Total
WITH DailySales AS (
    SELECT 
        OrderDate, 
        SUM(Quantity * UnitPrice) AS DailyRevenue
    FROM v_MasterSalesSummary
    GROUP BY OrderDate
)
SELECT 
    OrderDate, 
    DailyRevenue,
    SUM(DailyRevenue) OVER(ORDER BY OrderDate) AS RunningTotal
FROM DailySales;

-- Create a query that shows the OrderDate, the Category, and a Running Total of Revenue that resets every time the Category changes.
-- (Hint: You need to use PARTITION BY Category and ORDER BY OrderDate inside your SUM() OVER clause.)
-- On the last day of available data, which Category has the highest Cumulative Revenue?

WITH CategoryDailySales AS (
    SELECT 
        OrderDate,
        Category,
        SUM(TotalRevenue) AS DailyCategoryRevenue
    FROM v_MasterSalesSummary
    GROUP BY OrderDate, Category
)
SELECT 
    OrderDate,
    Category,
    DailyCategoryRevenue,
    SUM(DailyCategoryRevenue) OVER(
        PARTITION BY Category 
        ORDER BY OrderDate
    ) AS CumulativeCategoryRevenue
FROM CategoryDailySales
ORDER BY OrderDate DESC;

-- ==============================================================================================================================
-- Day 36: Question 1
-- 1. The Loyalty Leak (Churn Analysis)
-- Identify customers who were active in 2023 (placed at least one order) but have placed zero orders in 2024. 
-- Provide their Name and Email so Marketing can send them a "We Miss You" discount.
WITH Sales2023 AS (
    SELECT DISTINCT CustomerID 
    FROM Fact_Orders 
    WHERE YEAR(OrderDate) = 2023
),
Sales2024 AS (
    SELECT DISTINCT CustomerID 
    FROM Fact_Orders 
    WHERE YEAR(OrderDate) = 2024
)
SELECT c.FirstName, c.LastName, c.Email
FROM Dim_Customers c
JOIN Sales2023 s23 ON c.CustomerID = s23.CustomerID
LEFT JOIN Sales2024 s24 ON c.CustomerID = s24.CustomerID
WHERE s24.CustomerID IS NULL; -- They exist in 23 but not 24

-- This finds the people the CTE caught but the JOIN/NOT IN missed
WITH Sales2023 AS (
    SELECT DISTINCT CustomerID FROM Fact_Orders WHERE YEAR(OrderDate) = 2023
),
Sales2024 AS (
    SELECT DISTINCT CustomerID FROM Fact_Orders WHERE YEAR(OrderDate) = 2024
),
CTE_Results AS (
    SELECT c.CustomerID
    FROM Dim_Customers c
    JOIN Sales2023 s23 ON c.CustomerID = s23.CustomerID
    LEFT JOIN Sales2024 s24 ON c.CustomerID = s24.CustomerID
    WHERE s24.CustomerID IS NULL
),
Join_Results AS (
    SELECT DISTINCT c.CustomerID
    FROM Dim_Customers c
    JOIN Fact_Orders o ON c.CustomerID = o.CustomerID
    WHERE YEAR(o.OrderDate) = 2023
    AND c.CustomerID NOT IN (
        SELECT DISTINCT CustomerID FROM Fact_Orders WHERE YEAR(OrderDate) = 2024
    )
)
SELECT * FROM CTE_Results
EXCEPT
SELECT * FROM Join_Results;
-- ==============================================================================================================================
-- Day 37: Question 2
-- 2. Product Profitability Audit
-- Which product category has the highest Profit Margin? 
-- (Formula: (Total Revenue - Total Cost) / Total Revenue). 
-- Note: You must join the Dim_Products table to get the cost data.
SELECT * FROM Dim_Products;
SELECT * FROM Fact_OrderDetails;
SELECT * FROM Fact_Orders;
SELECT * FROM Raw_Products;
SELECT * FROM Raw_Orders;
SELECT * FROM Raw_OrderDetails;
SELECT * FROM Raw_Customers;

-- 1. Create the empty slot
ALTER TABLE Dim_Products
ADD Cost DECIMAL(18,2);

-- 2. Pull the data across the bridge
UPDATE d
SET d.Cost = CAST(r.Cost AS DECIMAL(18,2))
FROM Dim_Products d
JOIN Raw_Products r ON d.ProductID = CAST(r.ProductID AS INT);

SELECT ProductName, Price, Cost 
FROM Dim_Products 
WHERE Cost IS NULL;

SELECT 
    p.Category,
    SUM(od.Quantity * od.UnitPrice) AS TotalRevenue,
    SUM(od.Quantity * p.Cost) AS Total_COGS, -- COGS = Cost of Goods Sold
    (SUM(od.Quantity * od.UnitPrice) - SUM(od.Quantity * p.Cost)) / 
     NULLIF(SUM(od.Quantity * od.UnitPrice), 0) AS ProfitMargin
FROM Fact_OrderDetails od
JOIN Dim_Products p ON od.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY ProfitMargin DESC;

-- ==============================================================================================================================
-- Day 38: Question 3
-- 3. City Return Rate Analysis
SELECT 
    c.City,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(CASE WHEN o.Status = 'Returned' THEN 1 ELSE 0 END) AS ReturnedOrders,
    CAST(SUM(CASE WHEN o.Status = 'Returned' THEN 1 ELSE 0 END) AS FLOAT) / 
    COUNT(o.OrderID) * 100 AS ReturnRate
FROM Fact_Orders o
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
GROUP BY c.City
ORDER BY ReturnRate DESC;

-- =============================================================================================================================
-- Day 39: Question 4
-- 4. Unsold Products Identification
-- Identify products that have never been sold (i.e., do not appear in the Fact_Order
SELECT p.ProductName, p.Category
FROM Dim_Products p
LEFT JOIN Fact_OrderDetails od ON p.ProductID = od.ProductID
WHERE od.ProductID IS NULL;


-- =============================================================================================================================
-- Day 40: Question 5
-- 5. Customer Shipping Delay Analysis
-- Find the top 5 customers (Name and City) who have the longest average shipping delay
SELECT TOP 5
    c.FirstName + ' ' + c.LastName AS CustomerName,
    c.City,
    AVG(DATEDIFF(DAY, o.OrderDate, o.ShipDate)) AS AvgWaitTime
FROM Fact_Orders o
JOIN Dim_Customers c ON o.CustomerID = c.CustomerID
WHERE o.ShipDate IS NOT NULL 
  AND o.ShipDate >= o.OrderDate -- Filter out the "Time Travel" dirty data!
GROUP BY c.FirstName, c.LastName, c.City
ORDER BY AvgWaitTime DESC;