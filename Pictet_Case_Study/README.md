# Pictet Case Study – FIX Message Processing

## Overview
This repository contains my submission for the **Pictet Trading & Sales – Data Engineer** case study.

It includes:
- **Presentation** – Slides summarizing the proposed solution and architecture.
- **Assignment** – The original problem statement provided by Pictet.
- **Code** – Scripts and notebooks implementing the FIX message processing pipeline.

The solution demonstrates:
- Ingestion of FIX logs into Databricks using **Auto Loader**.
- Parsing and structuring of messages for downstream analytics.
- Deduplication and incremental processing using **Lakeflow Declarative Pipelines (DLT)**.
- Aggregation logic to produce trading activity summaries.

---

## How to Run

### 1) Environment
- **Platform:** Databricks (AWS)
- **Runtime:** DBR 14.x (Spark 3.x)
- **Languages:** Python 3.10, SQL
- **Features:** Lakeflow Declarative Pipelines (DLT), Auto Loader

### 2) Prerequisites
- Access to a Databricks workspace + permission to create **Lakeflow Declarative Pipelines** and **Jobs**
- An **S3 bucket** where you can write (for raw data + checkpoints)
- A Unity Catalog **catalog** and **schema** (or default Hive metastore)

> Recommended pipeline config keys (in DLT “Configuration”):
- `RAW_PATH` = `s3://<bucket>/fix/raw/`
- `CHECKPOINT_PATH` = `s3://<bucket>/fix/checkpoints/`
- `CATALOG` = `<your_catalog>`
- `SCHEMA` = `<your_schema>`

### 3) Setup
1. In Databricks, go to **Repos** → **Clone** this repository.
2. (Optional) Open `code/notebooks/*` and adjust any defaults (paths, table names) to match your `RAW_PATH`, `CATALOG`, `SCHEMA`.

### 4) Load sample data
1. Upload `data/fix_logs.txt` to S3 at `s3://<bucket>/fix/raw/`  
   (You can also use DBFS, then set `RAW_PATH` accordingly.)

### 5) Create the DLT pipeline
1. Left sidebar → **Workflows** → **Delta Live Tables** → **Create pipeline**.
2. **Source**: point to the notebook(s) in `code/notebooks/` (or the DLT Python script if you use one).
3. **Target**: set `CATALOG.SCHEMA`.
4. **Configuration**: add the keys from step 2.
5. **Mode**: 
   - **Triggered** for batch runs, or  
   - **Continuous** if you want near-real-time ingestion (streaming).
6. **Start** the pipeline and wait for tables to materialize.

### 6) (Optional) Schedule as a Job
1. **Workflows** → **Jobs** → **Create Job**.
2. Add a **Delta Live Tables** task that runs the pipeline from step 5.
3. Set a schedule (e.g., every 15 minutes) or keep it continuous.

### 7) Build dashboards
1. Left sidebar → **Dashboards (Lakeview)**.
2. Create visuals on the produced tables in `CATALOG.SCHEMA` (e.g., `fix_messages`, `fix_sessions`, `trade_activity_agg`).
3. **Refresh** and verify the latest data appears.

---

## Notes
- **Sample Data**: `data/` contains anonymized synthetic FIX logs for demonstration.
- **Scalability**: Designed for incremental ingestion (Auto Loader) and managed state (DLT).
- **Deduplication**: Composite keys on message metadata ensure idempotency and integrity.

---

## Contact
**Minh Truong**  
📧 minh.truong@ik.me


