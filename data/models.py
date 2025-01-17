import decimal

from django.db import models


class SupplyPoint(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs) -> "SupplyPoint":
        return cls.objects.create(**kwargs)


class Meter(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs) -> "Meter":
        return cls.objects.create(**kwargs)


class Reading(models.Model):
    value = models.DecimalField(decimal_places=4, max_digits=16)

    class Meta:
        abstract = True

    @classmethod
    def new(cls, *, value: decimal.Decimal, **kwargs) -> "Reading":
        return cls.objects.create(
            value=value,
            **kwargs,
        )
