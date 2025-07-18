from fastapi import FastAPI, HTTPException, Query
import sqlite3
import pandas as pd

app = FastAPI(title="HRIS API")

DB_PATH = "hris_project.db"  # Adjust if needed

def query_db(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the HRIS API!"}

# ✅ Fixed: This now uses your prebuilt time_to_hire_view
@app.get("/hiring-metrics")
def get_hiring_metrics():
    query = """
    SELECT
        department,
        ROUND(AVG(time_to_hire_days), 1) AS avg_time_to_hire
    FROM time_to_hire_view
    GROUP BY department
    ORDER BY avg_time_to_hire;
    """
    df = query_db(query)
    return df.to_dict(orient="records")

@app.get("/applicants/status-summary")
def get_status_summary(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    query = """
    SELECT Status AS status, COUNT(*) AS count
    FROM applicants
    GROUP BY Status
    ORDER BY count DESC
    LIMIT ? OFFSET ?;
    """
    df = query_db(query, (limit, offset))
    return df.to_dict(orient="records")
