TechGadget Inc. Data Engineering & Analytics Project
SQL Module Final Submission
Project Overview
This project involved the end-to-end transformation of a "messy" localized dataset containing 1 million transactions into a structured, optimized Star Schema. The goal was to repair data integrity issues and provide actionable insights for the CEO to drive 2026 strategy.
## Part 1: The "Dirty 12" Repair Log
I successfully identified and repaired the following data quality issues during the migration from Raw_Orders to the Fact and Dim tables:
- Date Normalization: Fixed 188 rows where dates were stored as DD-MM-YYYY using TRY_CONVERT (Style 105).
- Alphanumeric ID Handling: Migrated TransactionID from UUID strings while maintaining referential integrity.
- Email Domain Typos: Used REPLACE() to correct "gamil.com" to "gmail.com" for 5% of the customer database.
- Duplicate Prevention: Implemented DISTINCT and ROW_NUMBER() logic to ensure 0 duplicate records in Dim_Customers.
- Negative Quantity Fix: (Optional: Add how you handled Scenario 8).
## Part 2: Executive Insights (The Final 10)
#Business QuestionSQL Technique UsedKey Insight/Result1Loyalty LeakCTE + Left Join96 Customers churned between 2023 and 2024.2ProfitabilityAggregate MathThe [Insert Category] category has the highest margin.3Return RatesCASE + Aggregation[City Name] has the highest return rate at X%.4Ghost InventoryLeft Join (IS NULL)X products have never been sold.5Logistics WaitDATEDIFF + AVGThe average wait time is X days.6Peak HoursDATEPARTMost orders occur at [Hour].7BundlingSelf-Join[Product A] and [Product B] are the top pair.8Channel AOVCOALESCE + Subquery[Channel] generates the highest average order value.9Kenya GrowthWindow FunctionKenya accounts for X% of global revenue.10VelocityLEAD/LAGAverage days to 2nd purchase: X days.
## Part 3: Technical Reflections
### The "NOT IN" vs. "LEFT JOIN" Discovery
During the churn analysis, I discovered a discrepancy between using NOT IN and LEFT JOIN. Even though CustomerID had no NULLs, the LEFT JOIN via a CTE proved to be more robust for year-over-year comparisons. I opted for the CTE result as the source of truth.
## How to Run the Scripts
- Open SQL Server Management Studio (SSMS) or VS Code.
- Run the 01_Database_Setup.sql to create the schema.
- Run the 02_Data_Cleaning.sql to apply the repairs.
- Run the 03_Final_Audit.sql to view the executive results.