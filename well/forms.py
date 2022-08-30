from django.forms import ModelForm, TextInput, Select, Textarea
from django import forms
from . import models


class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'
            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Field
        fields = ('name',)


class WellForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['class'] = 'form-control'
            self.fields[k].widget.attrs['style'] = 'width:250px;'

    class Meta:
        model = models.Well
        fields = ('field', 'name', 'lat', 'long')
