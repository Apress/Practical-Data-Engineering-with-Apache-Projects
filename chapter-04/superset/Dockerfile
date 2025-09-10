FROM apache/superset:latest

USER root

# Install Trino SQLAlchemy driver and all dependencies
RUN pip install trino[sqlalchemy] lz4 zstandard orjson tzlocal

# Copy all packages to virtual environment
RUN cp -r /usr/local/lib/python3.10/site-packages/trino* /app/.venv/lib/python3.10/site-packages/ && \
    cp -r /usr/local/lib/python3.10/site-packages/lz4* /app/.venv/lib/python3.10/site-packages/ && \
    cp -r /usr/local/lib/python3.10/site-packages/zstandard* /app/.venv/lib/python3.10/site-packages/ && \
    cp -r /usr/local/lib/python3.10/site-packages/orjson* /app/.venv/lib/python3.10/site-packages/ && \
    cp -r /usr/local/lib/python3.10/site-packages/tzlocal* /app/.venv/lib/python3.10/site-packages/

USER superset
