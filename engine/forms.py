from django import forms
from django.core.exceptions import ValidationError

from graph.models import DataNode, DataEdge
from graph.queries import \
    get_units, get_data_readers, get_data_nodes_by_dest, \
    set_data_node_sources, link_data_nodes


class DataNodeUnitChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class DataNodeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class DataNodeModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class DataReadersForm(forms.Form):
    source_nodes = DataNodeModelMultipleChoiceField(
        queryset=get_data_readers(),
        required=False,
        to_field_name='id',
        widget=forms.SelectMultiple(
            attrs={
                'id': 'data-sources-picker',
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
                'data-max-options': '3',
            }
        ))


class ComponentForm(forms.Form):
    id = forms.UUIDField(
        widget=forms.HiddenInput(), required=False)
    title = forms.CharField(
        label='Title', max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(
        label='Name', max_length=128,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True}))
    type = forms.CharField(
        label='Type', max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True}))
    public = forms.BooleanField(
        label='Public', initial=True, required=False)
    unit = DataNodeUnitChoiceField(
        queryset=get_units(),
        required=False,
        to_field_name='name',
        label='Unit',
        widget=forms.Select(
            attrs={'class': 'form-control selectpicker'}
        ))

    @classmethod
    def load_from_node(cls, node: DataNode):
        form_args = {
            'id': node.id,
            'title': node.title,
            'name': node.name,
            'type': node.type,
            'public': node.public,
            'unit': node.unit
        }
        form_args.update(
            cls.load_special_fields(node)
        )
        return cls(form_args)

    @staticmethod
    def load_special_fields(node: DataNode):
        return {}

    def save_to_node(self):
        if self.is_valid():
            node_id = self.cleaned_data.get('id')
            if node_id is not None:
                node = DataNode.objects.get(id=node_id)
                node.type = self.cleaned_data['type']
                node.name = self.cleaned_data['name']
                node.title = self.cleaned_data['title']
                node.public = self.cleaned_data['public']
                node.unit = self.cleaned_data['unit']
            else:
                node = DataNode(
                    type=self.cleaned_data['type'],
                    name=self.cleaned_data['name'],
                    title=self.cleaned_data['title'],
                    public=self.cleaned_data['public'],
                    unit=self.cleaned_data['unit']
                )
            self.save_special_fields(node)
            node.save()
            return node.id
        return None

    def save_special_fields(self, node: DataNode):
        pass


class CalculatorForm(ComponentForm):
    source_node = DataNodeModelChoiceField(
        queryset=DataNode.objects.all(),
        to_field_name='id',
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
            }
        ))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        edge = DataEdge.objects.get(dest_id=node.id)
        fields.update({'source_node': edge.source})
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.save()

        source = self.cleaned_data['source_node']
        link_data_nodes(source, node)


class AggregatorForm(ComponentForm):
    source_nodes = DataNodeModelMultipleChoiceField(
        queryset=DataNode.objects.all(),
        to_field_name='id',
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
            }
        ))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        nodes = get_data_nodes_by_dest(node.id)
        fields.update({'source_nodes': nodes})
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.save()

        source_nodes = self.cleaned_data['source_nodes']
        set_data_node_sources(source_nodes, node)

    def clean_source_nodes(self):
        source_nodes = self.cleaned_data['source_nodes']
        if len(source_nodes) < 2:
            raise ValidationError('Must select at least 2 source nodes')
        return source_nodes


class WriterForm(CalculatorForm):
    pass
