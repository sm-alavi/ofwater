
from django.db import models
from django.db.models import OuterRef, Subquery
from well.models import BaseModel, Well
from typing import Optional, Iterable, Any


# Create your models here.


class SamplePoint(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Analysis(BaseModel):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=50, null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    molecular_weight = models.FloatField(null=True, blank=True)
    equivalent_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name + (self.abbreviation)


try:
    from stiff.models import StiffTemplateLevel
except ImportError:
    import sys
    StiffTemplateLevel = sys.modules[__package__ + '.StiffTemplateLevel']


class Test(BaseModel):
    lab_number = models.CharField(max_length=200)
    samplepoint = models.ForeignKey(SamplePoint, on_delete=models.DO_NOTHING)
    well = models.ForeignKey(Well, on_delete=models.CASCADE)
    sampling_date = models.DateTimeField()
    report_date = models.DateTimeField(blank=True)
    tds_error = models.FloatField(null=True, editable=False)
    charge_balance_error = models.FloatField(null=True, editable=False)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.lab_number

    def save(self, *args, **kwargs) -> None:
        self.charge_balance_error = self.cbe
        return super().save(*args, **kwargs)

    @property
    def tds_error_calc(self):
        testanalysis = TestAnalysis.objects.filter(
            test_id=self.id)
        sum_value = sum([ion.value for ion in testanalysis])
        return None

    @property
    def cbe(self):
        testanalysis = TestAnalysis.objects.filter(
            test_id=self.id)
        sum_meqv_cations = sum(
            [ion.meqv for ion in testanalysis if ion.meqv is not None and ion.meqv > 0])
        sum_meqv_anions = sum(
            [ion.meqv for ion in testanalysis if ion.meqv is not None and ion.meqv < 0])
        if sum_meqv_cations == abs(sum_meqv_anions):
            cbe = 0.0
        else:
            cbe = (sum_meqv_cations - abs(sum_meqv_anions)) * \
                100 / (sum_meqv_cations + abs(sum_meqv_anions))
        return round(cbe, 2)

    def get_radar_chart_data(self):
        return {
            'id': self.id,
            'lab_number': self.lab_number,
            'sampling_date': self.sampling_date,
            'report_date': self.report_date,
            'created': self.created_date,
            'updated': self.updated_date,
            'well': [
                {
                    'id': self.well.id,
                    'name': self.well.name,
                    'field': self.well.field.name
                }
            ],
            'analysis': [
                {
                    'id': item.id,
                    'name': item.analysis.name,
                    'analysis_id': item.analysis.id,
                    'abbreviation': item.analysis.abbreviation,
                    'value': item.value,
                    'meqv': item.meqv_abs,
                }

                for item in self.testanalysis_set.all()
            ],
        }

    def get_stiff_chart_data(self, stiff_template_id):
        ion_level = StiffTemplateLevel.objects.filter(
            stifftemplatelevelions__analysis__id=OuterRef('analysis')).values('name')

        testanalysis = TestAnalysis.objects.filter(
            test_id=self.id).annotate(level_no=Subquery(ion_level)).order_by('level_no')

        template_level = StiffTemplateLevel.objects.filter(
            stiff_template_id=int(stiff_template_id))

        data = []
        for i, v in enumerate(template_level):

            y = -int(v.name)
            x_cation = sum([ion.meqv for ion in testanalysis if ion.level_no ==
                           v.name and ion.meqv is not None and ion.meqv > 0])
            if x_cation != 0:
                point = {
                    'x': x_cation * (-1),
                    'y': y
                }
                data.append(point)

        for i, v in enumerate(reversed(template_level)):

            y = -int(v.name)
            x_anion = sum([ion.meqv for ion in testanalysis if ion.level_no ==
                          v.name and ion.meqv is not None and ion.meqv < 0])

            if x_anion != 0:
                point = {
                    'x': x_anion * (-1),
                    'y': y
                }
                data.append(point)

        data.append(data[0])

        return {
            'id': self.id,
            'lab_number': self.lab_number,
            'sampling_date': self.sampling_date,
            'report_date': self.report_date,
            'created': self.created_date,
            'updated': self.updated_date,
            'well': [
                {
                    'id': self.well.id,
                    'name': self.well.name,
                    'field': self.well.field.name
                }
            ],
            'data': data
        }


class TestAnalysis(BaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)

    @ property
    def meqv(self):
        if self.analysis.molecular_weight and self.analysis.charge and self.value:
            return self.value/(self.analysis.molecular_weight/self.analysis.charge)

    @ property
    def meqv_abs(self):
        if self.analysis.molecular_weight and self.analysis.charge and self.value:
            return self.value/(self.analysis.molecular_weight/abs(self.analysis.charge))


class MetaData(BaseModel):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TestMetadata(BaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    metadata = models.ForeignKey(MetaData, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)
