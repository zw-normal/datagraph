from engine.component import Component
from engine.calculator.forms import RollingForm


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()

        window = getattr(self, 'window', 1)
        return data_frame.rolling(window).sum()


class Form(RollingForm):
    pass
