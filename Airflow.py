from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define DAG
dag = DAG(
    'my_data_pipeline',
    schedule_interval=None,  # Set your desired schedule (e.g., '@daily')
    start_date=datetime(2023, 1, 1),  # Set your start date
    catchup=False,
)

# Define tasks for scraping sources
scrape_task1 = BashOperator(
    task_id='scrape_source1',
    bash_command='docker-compose run selenium-source1',
    dag=dag,
)

scrape_task2 = BashOperator(
    task_id='scrape_source2',
    bash_command='docker-compose run selenium-source2',
    dag=dag,
)

scrape_task3 = BashOperator(
    task_id='scrape_source3',
    bash_command='docker-compose run selenium-source3',
    dag=dag,
)

# Define task for PySpark processing
spark_task = BashOperator(
    task_id='process_data',
    bash_command='docker-compose run spark-job',
    dag=dag,
)

# Set task dependencies
[scrape_task1, scrape_task2, scrape_task3] >> spark_task
