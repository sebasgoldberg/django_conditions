from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta
from django_conditions.models import AbstractCondition

class ModelForTesting(models.Model):
    pass

class ConditionForTesting(AbstractCondition):
    instance = models.ForeignKey(ModelForTesting)
