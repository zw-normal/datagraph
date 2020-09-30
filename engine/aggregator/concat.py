from pandas import DataFrame, concat

from engine.component import Component
from engine.forms import AggregatorForm


class Aggregator(Component):

    def process(self):
        data_frames = self.process_source()
        assert len(data_frames) > 0

        return concat(data_frames, axis='columns', sort=False)


class Form(AggregatorForm):
    pass
