from graph.models import DataNodeType
from engine.aggregator.concat import Form as ConcatForm
from engine.tests import CommonTestCase


class ConcatTestCase(CommonTestCase.AggregatorTestCase):
    node_name = 'concat'
    node_type = DataNodeType.AGGREGATOR
    form_class = ConcatForm

    def assertProcess(self, result):
        columns = list(result.columns)
        self.assertListEqual(
            sorted(columns), sorted(['A', 'B', 'C', 'D']))
