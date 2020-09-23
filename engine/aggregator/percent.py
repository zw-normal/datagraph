from engine.component import Component
from engine.forms import AggregatorForm


class Aggregator(Component):

    def process(self):
        data_frames = self.process_source()
        assert len(data_frames) == 2
        return data_frames[0].div(data_frames[1].iloc[:, 0], axis='index')


class Form(AggregatorForm):
    pass

