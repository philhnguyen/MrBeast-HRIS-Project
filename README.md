
MrBeast HRIS Take-Home Project

This project simulates an end-to-end HR data platform using Python, SQLite, FastAPI, and scheduled automation. It includes data ingestion, transformation, API development, visualization, and deployment-ready components.

Full Transparency!
This was a really fun project that I was excited to work on. I have very little coding experience and had little exposure to all of these tools going into this assignment. With the help of ChatGPT and AI, I was able to learn about each piece along the way. 
Even though we were given 3 days to complete this assignment, I decided to challenge myself to complete this in the recommended 3 hours. This includes downloading and installing all of these tools to learning how to use them at a basic level. 
As such, the majority of my time was spent asking questions to get a full understanding of why and how we use each tool and what the limitations are and what that translates to in a real HRIS environment. 
If given more time and access to actual test/production data, I would love to explore actually working with different vendor APIs to pull data into these localized SQL environments and work with different stakeholders 
at MrBeast to come up with definitions of useful metrics that we can track, call, and easily visualize on demand.
Moreover, once we centralize all of the HR, recruiting, and performance datapoints, it would be really exciting to see how we can integrate a LLM using MrBeast trained data to supercharge these metrics even further.


---

Project Structure

```
├── scripts/
│   ├── load_data.py              # Loads and cleans data from CSVs
│   ├── main.py                   # FastAPI app with two endpoints
│   ├── visualize.py              # Generates static charts
│   ├── cron_sample.txt           # Sample cron expression
│   ├── run_loader.sh             # Sample shell script
├── charts/
│   ├── applicants_by_status.png
│   ├── avg_time_to_hire.png
│   ├── hires_per_department.png
├── hris_project.db               # SQLite database
├── README.md                     # This file
```

---

Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/mrbeast-hris-project.git
cd mrbeast-hris-project/scripts
```

### 2. Install Dependencies

```bash
pip install pandas matplotlib fastapi uvicorn
```

### 3. Load the Data

```bash
cd scripts
python load_data.py
```

This loads three CSVs into a local SQLite DB (`hris_project.db`) and creates key views.

### 4. Run the API

```bash
uvicorn main:app --reload
```

Visit:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger docs
- `/hiring-metrics`: average time-to-hire by department
- `/applicants/status-summary`: applicant counts by status

### 5. Generate Visualizations

```bash
python visualize.py
```

Charts will be saved in the `charts/` folder.

---

Automation

#Windows (Live)

Scheduled daily load at 2AM via Task Scheduler pointing to `load_data.py`.

Cross-platform Examples (Documentation Only)
- `scripts/cron_sample.txt` – sample Linux cron:
  ```
  0 2 * * * /usr/bin/python3 /path/to/load_data.py
  ```
- `scripts/run_loader.sh` – sample shell script:
  ```bash
  #!/bin/bash
  python3 /path/to/load_data.py
  ```

---

Design Decisions

Schema Normalization

- Each CSV is loaded as its own table:
  - `applicants`, `employees`, and `employment_type`
- Employee and employment type tables are joined 1:1 via `ID`
- Applicant and employee matches are performed using `Name`

Data Cleaning

- Dates converted to ISO format (dates may still display `00:00:00` time)
- Views use `julianday()` to calculate `time_to_hire_days`
- Created `time_to_hire_view` for easier aggregation and reuse

API Design

- FastAPI used for fast setup and native Swagger UI
- Endpoints follow REST conventions
- Errors like missing tables are caught and logged (though limited time meant not all errors were fully handled)

---

Visualizations

Charts saved in `/charts/`:
- `applicants_by_status.png`
- `avg_time_to_hire.png`
- `hires_per_department.png`

---

Assumptions & Known Limitations

- Applicant to employee match uses `Name`, which is not ideal in real systems
- Some employees may not have a matching applicant record (or vice versa)
- Timestamps (`00:00:00`) appear in some date fields; efforts to strip failed due to SQLite's datetime behavior
- The `time_to_hire_view` must exist before API endpoints will work properly
- API currently reads directly from SQLite; production systems would likely use PostgreSQL or an API layer above DBT

---

Metrics for Leadership

Designed with CHRO/CPO visibility in mind:
- Time-to-hire: key hiring efficiency KPI
- Status summary: hiring pipeline health
- Hires per department: where growth is happening

Additional metrics I'd explore with more time:
- Application-to-interview conversion rates
- Offer acceptance rates
- Diversity metrics across hiring stages

---

Notes

This was built under a ~3-hour constraint. If more time were available:
- I would normalize applicant → employee mapping using emails or IDs
- Add unit tests and logging to `load_data.py` and API routes
- Containerize with Docker
- Add DBT for modular SQL transformations


Thanks for reviewing this project — it was a fun and practical challenge!
