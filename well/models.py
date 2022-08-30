from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, related_name="created_%(app_label)s_%(class)s_related")
    updated_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, related_name="updated_%(app_label)s_%(class)s_related")
    updated_date = models.DateTimeField(auto_now=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class Field(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Well(BaseModel):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_json(self):
        return {
            'field': self.field.name,
            'field_id': self.field.id,
            'name': self.name,
            'lat': self.lat,
            'long': self.long,
        }
