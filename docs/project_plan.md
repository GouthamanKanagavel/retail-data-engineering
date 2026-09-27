# Project Plan

## Phase 1 - Project Setup
- [x] Create project repository
- [x] Configure Git
- [x] Configure GitHub
- [x] Create project directory structure
- [x] Create architecture document
- [ ] Validate development environment

## Phase 2 - Source Data
- [ ] Define retail business entities
- [ ] Define source data structure
- [ ] Create/generate retail datasets
- [ ] Introduce realistic data quality issues
- [ ] Define source-to-target mappings

## Phase 3 - Snowflake
- [ ] Configure Snowflake database
- [ ] Create RAW schema
- [ ] Create STAGING schema
- [ ] Create CORE schema
- [ ] Create ANALYTICS schema
- [ ] Create file formats
- [ ] Create stages
- [ ] Load initial data

## Phase 4 - Oracle
- [ ] Create Oracle source tables
- [ ] Load transactional data
- [ ] Validate source data
- [ ] Prepare Oracle extraction

## Phase 5 - Informatica
- [ ] Configure Oracle connection
- [ ] Configure Snowflake connection
- [ ] Build Oracle-to-Snowflake mapping
- [ ] Execute ETL
- [ ] Validate results

## Phase 6 - AWS S3 and Glue
- [ ] Create S3 data structure
- [ ] Upload daily retail files
- [ ] Configure Glue
- [ ] Create Glue job
- [ ] Load Snowflake RAW

## Phase 7 - dbt
- [ ] Initialize dbt project
- [ ] Configure Snowflake connection
- [ ] Create staging models
- [ ] Create core models
- [ ] Create analytical models
- [ ] Add tests
- [ ] Add documentation
- [ ] Create incremental models

## Phase 8 - Snowflake Incremental Processing
- [ ] Create Streams
- [ ] Create Tasks
- [ ] Process incremental records
- [ ] Test updates
- [ ] Test inserts
- [ ] Test duplicate scenarios

## Phase 9 - Airflow
- [ ] Configure Airflow
- [ ] Create DAG
- [ ] Add ingestion tasks
- [ ] Add validation tasks
- [ ] Add dbt tasks
- [ ] Add Snowflake tasks
- [ ] Add notification tasks
- [ ] Test failure recovery

## Phase 10 - Jenkins CI/CD
- [ ] Configure Jenkins
- [ ] Connect GitHub
- [ ] Create Jenkinsfile
- [ ] Validate SQL
- [ ] Validate Python
- [ ] Run dbt tests
- [ ] Implement pipeline

## Phase 11 - Docker
- [ ] Create Docker configuration
- [ ] Containerize Airflow
- [ ] Configure supporting services
- [ ] Test local environment

## Phase 12 - AWS Messaging
- [ ] Configure SQS
- [ ] Configure SNS
- [ ] Implement event flow
- [ ] Test notifications

## Phase 13 - Power BI
- [ ] Connect Power BI to Snowflake
- [ ] Create data model
- [ ] Create measures
- [ ] Create dashboards
- [ ] Validate business metrics

## Phase 14 - Testing
- [ ] Data quality testing
- [ ] Duplicate testing
- [ ] Null testing
- [ ] Incremental testing
- [ ] Failure testing
- [ ] Pipeline recovery testing

## Phase 15 - Final Documentation
- [ ] Architecture documentation
- [ ] Data dictionary
- [ ] Source-to-target mapping
- [ ] Pipeline documentation
- [ ] Deployment documentation
- [ ] Troubleshooting guide
- [ ] Interview explanation