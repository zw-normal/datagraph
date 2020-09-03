from pandas import DataFrame, concat
from engine.component import Component
from engine.forms import AggregatorForm


class Aggregator(Component):

    def process(self) -> DataFrame:
        data_frames = self.process_source()
        if data_frames:
            return concat(data_frames, axis='columns', sort=False)


class Form(AggregatorForm):
    pass
