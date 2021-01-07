from django.db import models

class VaccineType(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=30,)
    name = models.CharField(max_length=30,)
    type = models.CharField(max_length=30,)
    def __str__(self):
        return self.group


class VolunteersModel(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=30)
    dose = models.FloatField()
    positive = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
