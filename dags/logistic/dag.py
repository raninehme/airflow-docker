from airflow import DAG
from airflow.operators.python import PythonOperator

from logistic.settings import DagSettings
from logistic.commands import elt

import logging


logging.basicConfig(level='INFO')
logger = logging.getLogger(DagSettings.ID)

with DAG(dag_id=DagSettings.ID,
         default_args=DagSettings.DEFAULT_ARGS,
         description=DagSettings.DESCRIPTION,
         schedule_interval=DagSettings.SCHEDULE_INTERVAL,
         tags=DagSettings.TAGS,
         dagrun_timeout=DagSettings.Timeout
         ) as dag:

    pipeline = PythonOperator(
        dag=dag,
        task_id=f"elt_{DagSettings.ID}",
        python_callable=elt.run
    )

