FROM apache/superset:latest

USER root

# Install Trino SQLAlchemy driver
RUN pip install 'trino[sqlalchemy]'

USER superset
