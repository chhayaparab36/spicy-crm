from data import models as base_models
from django.db import models


class SupplyPoint(base_models.SupplyPoint):
    identifier = models.CharField(max_length=12, unique=True)


class Reading(base_models.Reading):
    supply_point = models.ForeignKey(
        SupplyPoint,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    read_at = models.DateTimeField()
