import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load DB
DB_PATH = "../hris_project.db"  # adjust if script is outside scripts/ folder
conn = sqlite3.connect(DB_PATH)

# Output folder
output_dir = "charts"
os.makedirs(output_dir, exist_ok=True)

# 1. Applicants by Status
status_query = """
SELECT Status, COUNT(*) AS Count
FROM applicants
GROUP BY Status
ORDER BY Count DESC;
"""
df_status = pd.read_sql_query(status_query, conn)

plt.figure(figsize=(8, 6))
plt.bar(df_status["Status"], df_status["Count"], color="steelblue")
plt.title("Applicants by Status")
plt.xlabel("Status")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/applicants_by_status.png")
plt.close()

# 2. Average Time-to-Hire by Department
ttf_query = """
SELECT
    department,
    ROUND(AVG(time_to_hire_days), 1) AS avg_time_to_hire
FROM time_to_hire_view
GROUP BY department
ORDER BY avg_time_to_hire;
"""
df_ttf = pd.read_sql_query(ttf_query, conn)

plt.figure(figsize=(10, 6))
plt.barh(df_ttf["department"], df_ttf["avg_time_to_hire"], color="darkorange")
plt.title("Average Time-to-Hire by Department")
plt.xlabel("Avg Days")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(f"{output_dir}/avg_time_to_hire.png")
plt.close()

# 3. (Optional) Hires per Department
hire_query = """
SELECT e.Department, COUNT(*) AS Hires
FROM employees e
JOIN applicants a ON e.Name = a.Name
WHERE a.Status = 'hired'
GROUP BY e.Department
ORDER BY Hires DESC;
"""
df_hires = pd.read_sql_query(hire_query, conn)

plt.figure(figsize=(10, 6))
plt.bar(df_hires["Department"], df_hires["Hires"], color="seagreen")
plt.title("Hires per Department")
plt.xlabel("Department")
plt.ylabel("Hires")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/hires_per_department.png")
plt.close()

print("✅ Charts saved in 'charts/' folder.")
