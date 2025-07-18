import sqlite3
import pandas as pd
import os

print("✅ Starting basic load...")

# Paths
db_path = os.path.abspath("hris_project.db")
data_dir = os.path.abspath("../data")

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Define files to load
csv_files = {
    "applicants": "Applicants.csv",
    "employees": "Employees.csv",
    "employment_type": "Employment Type.csv"
}

# Load each CSV into a table with its raw structure
for table_name, filename in csv_files.items():
    file_path = os.path.join(data_dir, filename)
    print(f"📄 Loading {filename} into table: {table_name}")
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()
print("✅ Done. All tables loaded without changes.")
