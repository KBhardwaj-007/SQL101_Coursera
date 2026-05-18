import sqlite3
import pandas as pd
import os

# =========================================
# CONNECT TO DATABASE
# =========================================

conn = sqlite3.connect("production.db")
cursor = conn.cursor()

# =========================================
# CREATE TABLES
# =========================================

cursor.executescript("""
CREATE TABLE IF NOT EXISTS cheese_production (
    Year INTEGER,
    Period TEXT,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Domain TEXT,
    Value INTEGER
);

CREATE TABLE IF NOT EXISTS honey_production (
    Year INTEGER,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Value INTEGER
);

CREATE TABLE IF NOT EXISTS milk_production (
    Year INTEGER,
    Period TEXT,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Domain TEXT,
    Value INTEGER
);

CREATE TABLE IF NOT EXISTS coffee_production (
    Year INTEGER,
    Period TEXT,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Value INTEGER
);

CREATE TABLE IF NOT EXISTS egg_production (
    Year INTEGER,
    Period TEXT,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Value INTEGER
);

CREATE TABLE IF NOT EXISTS state_lookup (
    State TEXT,
    State_ANSI INTEGER
);

CREATE TABLE IF NOT EXISTS yogurt_production (
    Year INTEGER,
    Period TEXT,
    Geo_Level TEXT,
    State_ANSI INTEGER,
    Commodity_ID INTEGER,
    Domain TEXT,
    Value INTEGER
);
""")

# =========================================
# CSV FILE PATHS
# =========================================

DATA_FOLDER = "data"

tables = {
    "cheese_production": "cheese_production.csv",
    "honey_production": "honey_production.csv",
    "milk_production": "milk_production.csv",
    "coffee_production": "coffee_production.csv",
    "egg_production": "egg_production.csv",
    "state_lookup": "state_lookup.csv",
    "yogurt_production": "yogurt_production.csv"
}

# =========================================
# LOAD CSV FILES INTO DATABASE
# =========================================

for table_name, file_name in tables.items():

    file_path = os.path.join(DATA_FOLDER, file_name)

    df = pd.read_csv(file_path)

    df.to_sql(table_name, conn, if_exists="append", index=False)

    print(f"{table_name} loaded successfully")

# =========================================
# SAMPLE SQL QUERIES
# =========================================


# Example 1
query1 = """
SELECT *
FROM cheese_production
LIMIT 5;
"""

result1 = pd.read_sql_query(query1, conn)
print(result1)

# Example 2
query2 = """
SELECT Year,
       SUM(Value) AS Total_Milk_Production
FROM milk_production
GROUP BY Year
ORDER BY Year;
"""

result2 = pd.read_sql_query(query2, conn)
print(result2)

# Example 3
query3 = """
SELECT s.State,
       c.Year,
       c.Value
FROM cheese_production c
JOIN state_lookup s
    ON c.State_ANSI = s.State_ANSI
LIMIT 10;
"""

result3 = pd.read_sql_query(query3, conn)
print(result3)


# =========================================
# SAVE AND CLOSE
# =========================================

conn.commit()
conn.close()