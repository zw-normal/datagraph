from engine.writer import vega_spec


class Writer(vega_spec.Writer):

    JINJA2_TEMPLATE_FILE = 'vega_lite_stacked_area_spec.jinja2'


class Form(vega_spec.Form):
    pass
