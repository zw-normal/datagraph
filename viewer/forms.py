from django.contrib.auth.forms import AuthenticationForm
from django import forms

from engine.forms import DataNodeModelChoiceField
from engine.queries import get_vega_spec_writers


class DataGraphAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter User Name...'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class VegaSpecNodesForm(forms.Form):
    vega_spec_nodes = DataNodeModelChoiceField(
        queryset=get_vega_spec_writers(),
        required=False,
        to_field_name='id',
        widget=forms.Select(
            attrs={
                'id': 'vega-spec-picker',
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
            }
        ))
