from engine.forms import WriterForm
from engine.component import Component


class Writer(Component):

    def process(self) -> str:
        # TODO: Process the data frame and return vega spec json by using tpl
        data_frame = self.process_source()
        return data_frame


class Form(WriterForm):
    pass
