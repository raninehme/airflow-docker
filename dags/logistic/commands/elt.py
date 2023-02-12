import pandas

from common.generate_data import FakeData
from common import db

from logistic.settings import POSTGRES, DagSettings

import csv
import io
import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

psql = db.PGSQL(**POSTGRES)
fake_data = FakeData()


def prep(input_df: pandas.DataFrame, is_snapshot) -> tuple[int, str, io.StringIO]:
    output_buffer = io.StringIO()

    # Remove Duplicates from Dataframe
    input_df.drop_duplicates(subset=['event_id'], keep="first", ignore_index=True, inplace=True)

    # Add housekeeping columns
    input_df['__etl_created_at'] = DagSettings.START_TIMESTAMP
    input_df['__job_name'] = DagSettings.ID

    # Get number of rows
    affected_rows: int = len(input_df.index) + 1

    # Get Columns' names
    df_columns: str = ','.join(list(input_df.columns))

    if not is_snapshot:
        input_df.drop(['event_id'], axis=1, inplace=True)
        input_df = input_df.sort_values('event_timestamp').drop_duplicates('item_id', keep='last', ignore_index=True)

        # Get Columns' names
        df_columns: str = ','.join(list(input_df.columns))

    # fill the data buffer from the data frame
    input_df.to_csv(output_buffer, index=False, header=True, quoting=csv.QUOTE_MINIMAL)

    return affected_rows, df_columns, output_buffer


def run():
    logistic_table = f"{POSTGRES['database']}.{POSTGRES['raw_schema']}.{POSTGRES['target_table']}"
    history_table = f"{POSTGRES['database']}.{POSTGRES['snapshot_schema']}.{POSTGRES['target_table']}"
    tmp_table = f"tmp_{POSTGRES['target_table']}"
    merge_key = POSTGRES['merge_key']

    for fake_df in fake_data.run():
        # Historical Table
        num_row, columns, buffer = prep(fake_df, is_snapshot=True)
        psql.copy(table=history_table, columns=columns, data=buffer)

        psql.commit()
        buffer.close()

        # Normal Data

        num_row, columns, logistic_buffer = prep(fake_df, is_snapshot=False)
        psql.exec(
            f"CREATE TEMPORARY TABLE {tmp_table} ON COMMIT DROP AS SELECT {columns} FROM {logistic_table} WITH NO DATA;")

        psql.copy(table=tmp_table, columns=columns, data=logistic_buffer)
        psql.merge(target_table=logistic_table, source_table=tmp_table, columns=columns, merge_keys=merge_key)

        psql.commit()
        logistic_buffer.close()

    psql.close(commit=True)


if __name__ == '__main__':
    run()
