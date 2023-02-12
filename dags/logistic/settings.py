from datetime import datetime, timedelta
import os

POSTGRES = {'host': os.getenv('DWH_HOST'),
            'port': os.getenv('DWH_PORT'),
            'database': os.getenv('DWH_DATABASE'),
            'user': os.getenv('DWH_USER'),
            'password': os.getenv('DWH_PASSWORD'),
            'raw_schema': 'raw_data',
            'snapshot_schema': 'snapshot',
            'target_table': 'logistic',
            'merge_key': 'item_id',
            }

class DagSettings:
    ID: str = 'logistic'
    START_TIMESTAMP: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    DESCRIPTION: str = 'DAG to load logistics event data'
    SCHEDULE_INTERVAL: str = None
    TAGS: list = [ID, 'foodspring']
    Timeout = timedelta(minutes=10)

    DEFAULT_ARGS: dict = {
        'owner': 'Foodspring',
        'depends_on_past': False,
        'start_date': datetime(2022, 2, 5),
        'retries': 2,
        'retry_delay': timedelta(seconds=15),
        'execution_timeout': timedelta(minutes=120)
    }
