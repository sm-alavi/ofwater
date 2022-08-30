from cProfile import label
from dataclasses import fields
from django import forms
from . import models
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class SamplePointForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'

    class Meta:
        model = models.SamplePoint
        fields = ('name', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AnalysisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'

    class Meta:
        model = models.Analysis
        fields = ('name', 'abbreviation', 'charge',
                  'molecular_weight', 'equivalent_weight')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'charge': forms.NumberInput(attrs={'class': 'form-control'}),
            'molecular_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'equivalent_weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['lab_number'].label = 'Lab. No.'
        self.fields['well'].label = 'Well No.'
        self.fields['samplepoint'].label = 'Sample Point'
        self.fields['sampling_date'].label = 'Sampling Date'

    class Meta:
        model = models.Test
        fields = ('lab_number', 'well', 'samplepoint',
                  'sampling_date', 'report_date', 'comment')

        widgets = {
            'lab_number': forms.TextInput(),
            'well': forms.Select(),
            'samplepoint': forms.Select(),
            'sampling_date': DateTimePickerInput(),
            'report_date': DateTimePickerInput(),
            'comment': forms.Textarea()

        }


class TestAnalysis(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        analysis = models.Analysis.objects.all()

        for item in analysis:
            self.fields[item.name] = forms.CharField(
                label=f'{item.name}({item.abbreviation})', max_length=10, required=False)
            self.fields[item.name].help_text = 'mg/lit'
            self.fields[item.name].widget.attrs['class'] = 'form-control form-control-sm '


class MetadataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = models.MetaData
        fields = ('name', 'unit',)

        widgets = {
            'name': forms.TextInput(),
            'unit': forms.TextInput(),
        }


class TestMetadata(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        metadata = models.MetaData.objects.all()

        for item in metadata:
            self.fields[item.name] = forms.CharField(
                label=item.name, max_length=10, required=False)
            self.fields[item.name].help_text = item.unit
            self.fields[item.name].widget.attrs['class'] = 'form-control form-control-sm'
