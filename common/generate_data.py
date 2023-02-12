import pandas
import logging
from typing import Iterable

from faker import Faker
from faker.providers import date_time, BaseProvider

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

fake = Faker()
fake.add_provider(date_time)
fake.add_provider(BaseProvider)


class FakeData:
    def __init__(self):
        self.num_events = 70
        self.num_batches = 3
        self.version = ['1.1', '1.2', '2.0', '2.3']
        self.event_type = ['item_received', 'item_sent']
        self.item_format = '????-##??-###?-????'
        self.full_duplicate = False

    def generate(self) -> Iterable[list]:
        """
        Generate event like fake data
        """
        events = []

        logger.info(f'Generating {self.num_batches} batches with {self.num_events} events')

        for _ in range(self.num_batches):
            events = []
            for _ in range(self.num_events):
                event = {
                    "event_id": fake.uuid4(),
                    "event_timestamp": str(fake.date_time_between(start_date='-1y', end_date='now')),
                    "version": fake.random_element(self.version),
                    "type": fake.random_element(self.event_type),
                    "item_id": fake.bothify(text=self.item_format).lower()
                }

                events.append(event)

            yield events

    def duplicate(self, data: list) -> pandas.DataFrame:
        """
        Duplicate data fully or 50%
        :param data: Data to be sampled
        :return: Dataframe of all the data
        """
        pd = pandas.DataFrame(data)

        if self.full_duplicate:
            logger.info(f'Duplicating all the data')
            data_df = pandas.concat([pd, pd], ignore_index=True)
        else:
            logger.info(f'Duplicating 50% the data')
            data_df = pandas.concat([pd, pd.sample(frac=0.50)], ignore_index=True)

        return data_df

    def create_item_events(self, data: list) -> pandas.DataFrame:
        """
        Create new events for 20% of existing items
        :param data: Reference data to be used
        :return: Dataframe of the new data
        """
        pd = pandas.DataFrame(data)

        sample_df = pd.sample(frac=0.20, ignore_index=True)
        # update columns
        sample_df['type'] = sample_df.apply(lambda _: fake.random_element(self.event_type), axis=1)
        sample_df['version'] = sample_df.apply(lambda _: fake.random_element(self.version), axis=1)
        sample_df['event_timestamp'] = sample_df.apply(
            lambda _: str(fake.date_time_between(start_date='-1y', end_date='now')), axis=1)
        sample_df['event_id'] = sample_df.apply(lambda _: fake.uuid4(), axis=1)

        return sample_df

    def run(self):
        for events_data in self.generate():
            new_item_events = self.create_item_events(data=events_data)
            event_data_df = self.duplicate(events_data)
            yield pandas.concat([new_item_events, event_data_df], ignore_index=True)


if __name__ == '__main__':
    fake_date = FakeData()
    fake_date.run()
