FROM apache/superset:latest

USER root

# Install Trino SQLAlchemy driver and all dependencies
RUN pip install trino[sqlalchemy] 

USER superset
