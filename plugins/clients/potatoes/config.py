import datetime
import decimal
import json

from domain.readings import config

from . import models


class ReadingsConfig(config.ReadingsConfig):
    def create_supply_point(self, **kwargs) -> models.SupplyPoint:
        return models.SupplyPoint.new(
            identifier=kwargs["identifier"],
        )

    def create_reading(
        self,
        *,
        value: decimal.Decimal,
        **kwargs,
    ) -> models.Reading:
        return models.Reading.new(
            value=value,
            read_at=kwargs["read_at"],
            supply_point=kwargs["supply_point"],
        )

    def ingest_file(self, file_path: str, **kwargs) -> None:
        with open(file_path) as f:
            data = json.load(f)

        for supply_point_dict in data:
            try:
                supply_point = models.SupplyPoint.objects.get(
                    identifier=supply_point_dict["identifier"]
                )
            except models.SupplyPoint.DoesNotExist:
                supply_point = self.create_supply_point(
                    identifier=supply_point_dict["identifier"],
                )

            for reading_dict in supply_point_dict["readings"]:
                self.create_reading(
                    supply_point=supply_point,
                    value=decimal.Decimal(str(reading_dict["value"])),
                    read_at=reading_dict["read_at"],
                )

    def get_supply_point(self, identifier: str) -> models.SupplyPoint:
        return models.SupplyPoint.objects.get(identifier=identifier)

    def get_readings(
        self,
        supply_point: models.SupplyPoint,
        from_dt: datetime.datetime | None = None,
        to_dt: datetime.datetime | None = None,
    ) -> list[dict]:
        readings = supply_point.readings.all()
        if from_dt:
            readings = readings.filter(read_at__gte=from_dt)
        if to_dt:
            readings = readings.filter(read_at__lt=to_dt)
        return [
            {
                "value": str(reading.value),
                "read_at": reading.read_at.isoformat(),
            }
            for reading in readings
        ]
