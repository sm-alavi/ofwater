from django.db import models
from well.models import BaseModel

try:
    from analysis.models import Analysis
except ImportError:
    import sys
    Analysis = sys.modules[__package__ + '.Analysis']

# Create your models here.


class StiffTemplate(BaseModel):
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StiffTemplateLevel(BaseModel):
    stiff_template = models.ForeignKey(StiffTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StiffTemplateLevelIon(BaseModel):
    stiff_template_level = models.ForeignKey(
        StiffTemplateLevel, on_delete=models.CASCADE, related_name='stifftemplatelevelions')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
