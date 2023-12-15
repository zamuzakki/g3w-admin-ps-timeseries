from django.contrib import admin
from .models import (
    QpsTimeseriesProject,
    QpsTimeseriesLayer
)


class QpsTimeseriesLayerAdmin(admin.TabularInline):
    model = QpsTimeseriesLayer

@admin.register(QpsTimeseriesProject)
class QpsTimeseriesProjectAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'project',
    )

    inlines = [
        QpsTimeseriesLayerAdmin
    ]