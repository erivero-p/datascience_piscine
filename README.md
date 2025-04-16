## 🛠️ Data Science Piscine – 42

This repo contains my solutions for the **42 Data Science Piscine**.

Each folder represents a project with its own steps and scripts to clean, prepare, and process data using **PostgreSQL** and **bash scripting**.
I’m not uploading the csv files for security (and storage) reasons, so please, make sure to place them in the correct route (X_ProjectDir/csv_files/). 

---

### 📁 Projects

- [Project 0 – Data Engineer](#project-0---data-engineer)
- [Project 1 – Data Warehouse](#project-1---data-warehouse)

---

### Project 0 - Data Engineer

In this first project we focus on the basics of Data Engineering: setting up a PostgreSQL environment, and preparing raw data from CSV files to make it ready for analysis.

### 🚀 What’s included

- **ex00 & ex01**: Create database, user and connect via `psql` and `pgAdmin`.
- **ex02 / ex03 / ex04**: Create SQL tables from CSVs using different data types.

If you’re not using pgAdmin, you can use:

```bash
\dt                    # list all tables
\d <table_name>       # show structure of a table
SELECT * FROM <table_name> LIMIT 10;  # show a few rows
```

### ▶️ How to run

Use Docker Compose if you don’t have PostgreSQL installed locally.

Each exercise includes a `Makefile` and an entrypoint that runs the script automatically.

---

### Project 1 - Data Warehouse

In this project, we clean and combine raw CSV data to build a small warehouse using PostgreSQL.

### 🚀 What’s included

- **ex01**: Merge all monthly `customer` CSVs into a single `customers` table.
- **ex02**: Remove duplicate rows (including near-duplicates within ≤1s).
- **ex03**: Enrich `customers` by joining it with product info from `items.csv`.

(ex00 is not included as is the same as project 0 ex01)

### ▶️ How to run

You can use the provided Docker Compose to run Postgres and pgAdmin.
As in this project each exercise is one step further than the previous one, this time, I made a common docker-compose so you can run each script manually.
