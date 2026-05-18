import sqlite3
import pandas as pd

# =========================================
# CONNECT TO EXISTING DATABASE
# =========================================

conn = sqlite3.connect("production.db")

# =========================================
# QUERY 1
# =========================================

query1 = """
SELECT M.Year, SUM(REPLACE(M.Value, ',', '')) as Total_Milk
FROM milk_production M
WHERE M.Year = '2023';
"""

# query1 = """
# SELECT M.Year, SUM(REPLACE(M.Value, ',', '')) as Total_Milk_2023
# FROM milk_production M
# WHERE M.Year = 2023;
# """

df1 = pd.read_sql_query(query1, conn)

print("Milk Production")
print(df1)

# =========================================
# QUERY 2
# =========================================

query2 = """
SELECT Year, Period, State_ANSI, SUM(REPLACE(Value, ',', '')) AS Cheese_Production
FROM cheese_production
WHERE Period = 'APR' AND Year = '2023'
GROUP BY State_ANSI, Year, Period
HAVING SUM(REPLACE(Value, ',', '')) > 100000000;
"""

df2 = pd.read_sql_query(query2, conn)

print("\nCheese Production In APR 2023")
print(df2)

# =========================================
# QUERY 3
# =========================================

query3 = """
SELECT Year, SUM(REPLACE(Value, ',', '')) AS Coffee_Production
FROM coffee_production
GROUP BY Year
HAVING Year = '2011';
"""

df3 = pd.read_sql_query(query3, conn)

print("\nCoffee Production Over Years")
print(df3)

# =========================================
# QUERY 4
# =========================================

query4 = """
SELECT Year, Count(*) Total_Entry, SUM(REPLACE(Value, ',', '')) Honey_Production, (SUM(REPLACE(Value, ',', '')) / Count(*)) Average_Honey_Production
FROM honey_production
GROUP BY Year
HAVING Year = '2022';
"""

df4 = pd.read_sql_query(query4, conn)

print("\nAverage Honey Production for 2022")
print(df4)

# =========================================
# QUERY 5
# =========================================

query5 = """
SELECT *
FROM state_lookup
WHERE State = 'FLORIDA';
"""

df5 = pd.read_sql_query(query5, conn)

print("\nState_ANSI code for States")
print(df5)

# =========================================
# QUERY 6
# =========================================

query6 = """
SELECT s.State, SUM(REPLACE(c.Value, ',', '')) AS Cheese_Production
FROM state_lookup s
INNER JOIN cheese_production c ON c.State_ANSI = s.State_ANSI
WHERE c.Period = 'APR' AND c.Year = '2023'
GROUP BY s.State_ANSI
HAVING s.State = 'NEW JERSEY';
"""

df6 = pd.read_sql_query(query6, conn)

print("\nStates with Cheese_Production in 2023")
print(df6)

# =========================================
# QUERY 7
# =========================================

query7 = """
SELECT y.Year, SUM(REPLACE(y.Value, ',', '')) Yogurt_Production_2022
FROM yogurt_production y
WHERE y.Year = '2022'
AND y.State_ANSI IN (
SELECT DISTINCT c.State_ANSI
FROM cheese_production c
WHERE c.Year = '2023');
"""

df7 = pd.read_sql_query(query7, conn)

print("\nYogurt Production in 2022 based on Cheese_Production in 2023")
print(df7)

# =========================================
# QUERY 8
# =========================================

# query8 = """
# SELECT COUNT(State) Missing_States
# FROM state_lookup
# WHERE State_ANSI NOT IN (
# SELECT DISTINCT m.State_ANSI
# FROM milk_production m
# WHERE m.Year = '2023');
# """

# query8 = """
# SELECT COUNT(*) Missing_States
# FROM state_lookup S
# WHERE NOT EXISTS (
# SELECT 1
# FROM milk_production P
# WHERE P.State_ANSI = S.State_ANSI
# AND P.Year = 2023);
# """

query8 = """
SELECT COUNT(DISTINCT s.State) Missing_States
FROM state_lookup s
LEFT JOIN milk_production m
ON s.State_ANSI = m.State_ANSI AND m.Year = '2023'
WHERE m.State_ANSI IS NULL;
"""

df8 = pd.read_sql_query(query8, conn)

print("\nAll states that are missing from milk_production in 2023")
print(df8)

# =========================================
# QUERY 9
# =========================================

query9 = """
SELECT s.State, c.Value
FROM state_lookup s
LEFT JOIN cheese_production c ON s.State_ANSI = c.State_ANSI AND c.Period = 'APR' AND c.Year = '2023'
WHERE s.State = 'DELAWARE';
"""

df9 = pd.read_sql_query(query9, conn)

print("\nAll states with their cheese production values, including states that didn't produce any cheese in April 2023")
print(df9)

# =========================================
# QUERY 10
# =========================================

query10 = """
SELECT
    CAST(AVG(REPLACE(Value, ',', '')) AS INTEGER) AS AVERAGE_COFFEE_PRODUCTION
FROM coffee_production P
WHERE P.Year IN (
    SELECT HP.Year
    FROM honey_production HP
    GROUP BY HP.Year
    HAVING SUM(REPLACE(HP.Value, ',', '')) > 1000000
);
"""

df10 = pd.read_sql_query(query10, conn)

print("\nAverage coffee production for all years where the honey production exceeded 1 million")
print(df10)

# =========================================
# CLOSE CONNECTION
# =========================================

conn.close()