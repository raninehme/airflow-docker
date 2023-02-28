"""
This DAG defines two tasks: generate_random_number_task and print_random_number_task.
The generate_random_number_task task generates a random number between 1 and 100, and stores the result in an XCom variable.
The print_random_number_task task retrieves the random number from the XCom variable and prints it to the logs.
The >> operator indicates that generate_random_number_task should be executed before print_random_number_task.
The DAG is scheduled to run once at the start date specified in the default_args dictionary.
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random

default_args = {
    'start_date': datetime(2023, 2, 28)
}

def generate_random_number():
    return random.randint(1, 100)

def print_random_number(**kwargs):
    ti = kwargs['ti']
    random_number = ti.xcom_pull(task_ids='generate_random_number_task')
    print(f"The random number is {random_number}")

with DAG(dag_id='simple_example', default_args=default_args, schedule_interval='@once') as dag:
    generate_random_number_task = PythonOperator(
        task_id='generate_random_number_task',
        python_callable=generate_random_number
    )

    print_random_number_task = PythonOperator(
        task_id='print_random_number_task',
        python_callable=print_random_number
    )

    generate_random_number_task >> print_random_number_task
