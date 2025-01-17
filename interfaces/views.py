from django import http
from django.conf import settings
from django.utils import dateparse
from django.views import generic

from data import models
from domain.readings import config


class ReadingsView(generic.View):
    readings_config: config.ReadingsConfig
    supply_point: models.SupplyPoint

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.readings_config = config.get_config(settings.CLIENT_NAME)
        self.supply_point = self.readings_config.get_supply_point(
            kwargs["supply_point_identifier"]
        )

    def get(self, request, *args, **kwargs) -> http.HttpResponse:
        if from_dt := request.GET.get("from_dt"):
            from_dt = dateparse.parse_datetime(from_dt)
        else:
            from_dt = None
        if to_dt := request.GET.get("to_dt"):
            to_dt = dateparse.parse_datetime(to_dt)
        else:
            to_dt = None

        readings = self.readings_config.get_readings(
            supply_point=self.supply_point,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        return http.JsonResponse(readings, safe=False)
