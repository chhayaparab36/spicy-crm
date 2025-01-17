from django.contrib import admin
from django.urls import path

from interfaces import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("readings/<int:supply_point_identifier>/", views.ReadingsView.as_view(), name="readings"),
]
