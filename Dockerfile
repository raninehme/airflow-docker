FROM apache/airflow:latest

USER airflow
WORKDIR ${AIRFLOW_HOME}
# Copy resources
COPY --chown=airflow:root ./requirements.txt requirements.txt
# Install Python packages
RUN pip install --no-cache-dir -q -r requirements.txt