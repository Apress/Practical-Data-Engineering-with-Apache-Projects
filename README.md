# Practical-Data-Engineering-with-Apache-Projects
This repository contains the source code for the book "Practical Data Engineering with Apache Projects". 

This book is organized into three distinct parts, each focusing on different aspects of modern data engineering:

## Part 1: Foundational Data Engineering
The first part of the book covers essential data engineering concepts and tools, including data storage in lakehouses, ETL pipelines, data visualization, and pipeline automation. 

- **Chapter 02** - You will set up an Apache Iceberg data lakehouse infrastructure from the ground up. This lakehouse provides a strong foundation for the OneShop data engineering team. You will see how they build several projects based on this infrastructure.
- **Chapter 03** - You will model the Iceberg lakehouse (set up in Chapter 02) with Medallion architecture. You'll develop batch ETL pipelines with Apache Spark to load data into the bronze layer and transform this data for the silver layer.
- **Chapter 04** - You will define gold layer tables in the lakehouse using Trino. Then, you will use Apache Superset to create business intelligence dashboards from these gold tables.
- **Chapter 05** - You will use Apache Airflow to orchestrate an ETL pipeline that computes customer segments based on silver tables in the lakehouse, exports the results to MinIO as a CSV file, and sends an email reminder.

## Part 2: Streaming and Real-Time Analytics
The second part focuses on handling real-time data and stream processing with Apache Kafka ecosystem. You'll explore: 

- **Chapter 06** - You will implement a change data capture (CDC) pipeline with Debezium to capture inventory level changes from Postgres and reliably update a search index in OpenSearch.
- **Chapter 07** - You will develop a real-time analytics dashboard with Apache Kafka, Clickhouse, and Streamlit to visualize OneShop's flash sale campaigns in real-time.
- **Chapter 08** - You will use Kafka and Apache Flink to build a user login anomaly detection system.

## Part 3: Data Engineering for AI and ML
The final part demonstrates how data engineering enables modern AI and machine learning applications. Projects include:

- **Chapter 09** - You will build a product recommendation engine for OneShop. We will use Spark MLlib library to create a machine learning feature engineering pipeline based on the data available in the silver layer tables, computing the features required for the recommender model, and storing the refined features in a gold layer table.
- **Chapter 10** - As the final project, you will implement a semantic similarity search engine to analyze customer reviews left by OneShop customers. You will use the pgvector extension on Postgres for this.

Each part builds upon the previous sections, providing you with a comprehensive understanding of modern data engineering practices and tools. The hands-on projects will give you practical experience in implementing real-world solutions using industry-standard Apache technologies.

## Prerequisites

Before diving into the practical projects in this book, there are a few prerequisites you should have in place to ensure a smooth learning experience:

### Docker Environment

Almost all the projects you will explore in this book are available as Docker Compose projects. This approach offers several benefits:

- **Self-contained environments:** Each project runs in isolated containers, preventing conflicts between different technology stacks.
- **Easy reproducibility:** You can quickly spin up complex multi-service architectures with a single command.
- **Consistent experience:** The containerized setup ensures that the projects work the same way across different operating systems and environments.
- **Simplified cleanup:** When you're done with a project, you can remove all associated resources without affecting your local system.

To run these projects, you will need to have the following installed on your local machine:

- **Docker Engine** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)

For the resource requirements, we recommend:

- **CPU:** At least 4 cores (8 cores recommended for smoother performance)
- **Memory:** Minimum 8GB RAM (16GB or more recommended, especially for projects involving Apache Spark)
- **Storage:** At least 20GB of free disk space

### Project Code Repository

All code for the projects discussed in this book is available in the accompanying GitHub repository.

To clone the repository using a Git client:

```bash
https://github.com/Apress/Practical-Data-Engineering-with-Apache-Projects
```

Alternatively, you can download the code as a ZIP file.

The repository is structured to optimize your learning experience, with separate folders organized by chapter. 

```bash
.
├── chapter-02
├── chapter-03
├── chapter-04
├── chapter-05
├── chapter-06
├── chapter-07
├── chapter-08
├── chapter-09
├── chapter-10
```

To make your learning experience smoother, we've pre-implemented the difficult or boilerplate parts of each project, allowing you to focus on building the core data engineering components while following along with each chapter. This approach saves you valuable time by letting you concentrate on the concepts that matter most. Additionally, each project comes with clear instructions on how to get started and which components you need to implement.

### Programming Knowledge

To get the most out of this book, you should have familiarity with the following technologies and languages:

- **Python:** Most examples use Python for data processing, transformation, and pipeline development.
- **PySpark:** Basic knowledge of PySpark APIs will be helpful for working with large-scale data processing.
- **Java:** Some components, particularly those related to Apache Kafka and Flink, use Java.
- **YAML:** Configuration files for Docker Compose and various services are written in YAML.
- **SQL:** You should be comfortable with basic to intermediate SQL queries for data analysis and transformation.

If you need to brush up on any of these skills, we recommend spending some time refreshing your knowledge before diving into the more complex projects. There are many online resources available for quick reviews of these technologies.