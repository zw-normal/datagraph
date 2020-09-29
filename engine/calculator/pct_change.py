from pandas import DataFrame

from engine.component import Component
from engine.forms import CalculatorForm


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()
        if data_frame is not None:
            return data_frame.sort_index().pct_change()
        return DataFrame()


class Form(CalculatorForm):
    pass
