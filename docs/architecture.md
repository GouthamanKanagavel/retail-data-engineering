# Retail Data Engineering & Analytics Platform

## 1. Project Overview

This project implements an end-to-end retail data engineering and analytics
platform using multiple enterprise and cloud technologies.

The platform demonstrates:

- Batch data ingestion
- ETL and ELT
- Data quality and validation
- Incremental processing
- Change data capture concepts
- Data transformation
- Data warehouse dimensional modeling
- Workflow orchestration
- CI/CD
- Containerization
- Cloud storage and messaging
- Business intelligence

---

## 2. Business Scenario

The project represents a retail organization operating multiple stores and
an online sales channel.

The business generates data related to:

- Customers
- Products
- Stores
- Orders
- Order items
- Payments

Data originates from both legacy databases and cloud file sources.

The objective is to consolidate the data into Snowflake and provide trusted
analytics datasets for business reporting.

---

## 3. Source Systems

### Oracle

Oracle represents the organization's legacy transactional database.

Example data:

- Customers
- Products
- Stores
- Historical orders

Oracle data will be extracted using Informatica.

### AWS S3

S3 represents cloud-based file data received from external systems.

Example files:

- Daily sales
- Order updates
- Product updates
- Customer updates

---

## 4. Data Ingestion

### Oracle → Snowflake

Oracle
   ↓
Informatica
   ↓
Snowflake RAW

# S3 → Snowflake
AWS S3
   ↓
AWS Glue
   ↓
Snowflake RAW

# Snowflake Data Layers
RAW
 ↓
STAGING
 ↓
CORE
 ↓
ANALYTICS / MART

# RAW

Contains data loaded from source systems with minimal transformation.

# STAGING

Performs standardization, type conversion, cleansing and basic validation.

# CORE

Contains integrated business entities and reusable business logic.

# ANALYTICS / MART

Contains reporting-ready dimensional models.

# Dimensional Model
DIM_DATE
DIM_CUSTOMER
DIM_PRODUCT
DIM_STORE
      |
      |
   FACT_SALES

FACT_SALES will contain measurable business events such as sales quantity,
sales amount, discount and payment amount.

# Transformation
Snowflake RAW
     ↓
dbt
     ↓
STAGING
     ↓
CORE
     ↓
ANALYTICS

dbt will also be used for:

Data tests
Documentation
Model dependencies
Incremental models
Reusable SQL transformations

# Incremental Processing
RAW TABLE
    ↓
STREAM
    ↓
TASK
    ↓
TARGET TABLE

# Orchestration
Start
  ↓
Check source
  ↓
Ingest data
  ↓
Validate data
  ↓
Run dbt
  ↓
Run Snowflake transformations
  ↓
Run data quality checks
  ↓
Send notification
  ↓
End

# CI/CD
GitHub will store the project source code.

Jenkins will automate validation and deployment activities.

Developer
    ↓
Git
    ↓
GitHub
    ↓
Jenkins
    ↓
Validation
    ↓
Deployment

# Containerization

Docker will be used to containerize development and orchestration components.
Example:
    Docker
        ├── Airflow
        ├── PostgreSQL metadata database
        └── Supporting services
# Messaging
AWS SQS will be used to demonstrate queue-based event processing.

AWS SNS will be used for notification and publish/subscribe scenarios.

Event
 ↓
SQS
 ↓
Processing

and:

Pipeline Event
     ↓
SNS
 ├── Email
 └── Other Subscribers

 # Business Intelligence
 Snowflake
    ↓
Power BI
    ↓
Reports
    ↓
Dashboards

# Complete Architecture

                         ┌──────────────┐
                         │    Oracle    │
                         └──────┬───────┘
                                │
                           Informatica
                                │
                                ▼
┌──────────────┐          ┌──────────────┐
│   AWS S3     │──Glue───►│ Snowflake RAW│
└──────────────┘          └──────┬───────┘
                                 │
                                dbt
                                 │
                                 ▼
                         ┌──────────────┐
                         │   STAGING    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │     CORE     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   ANALYTICS  │
                         │     MART     │
                         └──────┬───────┘
                                │
                                ▼
                           ┌─────────┐
                           │ Power BI│
                           └─────────┘


GitHub ─────► Jenkins ─────► CI/CD

Airflow ─────► Pipeline Orchestration

SQS/SNS ─────► Events & Notifications

Docker ──────► Containerization

# Technology Responsibilities

| Technology  | Responsibility                      |
| ----------- | ----------------------------------- |
| Oracle      | Legacy source database              |
| Informatica | Oracle ETL                          |
| AWS S3      | Cloud file storage                  |
| AWS Glue    | Cloud ingestion/transformation      |
| Snowflake   | Cloud data warehouse                |
| dbt         | SQL transformation/modeling/testing |
| Streams     | Change capture                      |
| Tasks       | Incremental processing              |
| Airflow     | Orchestration                       |
| Git         | Version control                     |
| GitHub      | Remote repository                   |
| Jenkins     | CI/CD                               |
| Docker      | Containerization                    |
| SQS         | Message queue                       |
| SNS         | Notifications/pub-sub               |
| Power BI    | Analytics and visualization         |

# Project Goal

The final solution should demonstrate an end-to-end production-style data
engineering workflow rather than isolated technology exercises.

The same retail business scenario and datasets will be used throughout the
project.

