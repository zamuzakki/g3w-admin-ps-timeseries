# coding=utf-8
""""
    Qps_timeseries models
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-04'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from qdjango.models import Project, Layer


class QpsTimeseriesProject(models.Model):
    """ Main configuration model """

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="%(app_label)s_projects", unique=True)
    note = models.TextField('Note', null=True, blank=True)

    class Meta:
        verbose_name = 'Qps Timeseries Project'

    def __str__(self):
        return str(self.project)

    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)
    #
    #     # check for unique project for simple reporting system only for new
    #     try:
    #         srproject = SimpleRepoProject.objects.filter(project=self.project)[0]
    #     except:
    #         srproject = None
    #
    #     if srproject and (self.pk and self.pk != srproject.pk):
    #         raise ValidationError({'project': _("This project is just set for a simple reporting")})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        update = bool(self.pk)

        with transaction.atomic():
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

            # For new only, relation layers
            # if not update:
            #     layer = QpsTimeseriesLayer(simplerepo_project=self)
            #     layer.save()

    @property
    def layers(self):
        """Return children layers"""
        return self.qpstimeserieslayer_set.all()


GEO_TYPE_VECTOR_LAYER_ALLOWED = [
    'Point',
    'MultiPoint',
    'Point25D',
    'MultiPointZ',
    'PointZ',
    'Polygon',
    'MultiPolygon',
    'Polygon25D',
    'PolygonZ',
    'MultiPolygonZ',
    'LineString',
    'MultiLineString'
    'LineString25D',
    'LineStringZ',
    'MultiLineStringZ',
]


class QpsTimeseriesLayer(models.Model):
    """ Layer where to apply qps_timeseries """

    qps_timeseries_project = models.ForeignKey(QpsTimeseriesProject, on_delete=models.CASCADE, unique=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE,
                                  help_text=_('Select vector project layers to use for PS Timeseries: '
                                              'only follow geometry types are allowed: ' +
                                              ', '.join(GEO_TYPE_VECTOR_LAYER_ALLOWED))
                              )

    # Plot data
    # ---------
    # Scale options
    min_date = models.DateField('Min date', null=False, blank=False)
    max_date = models.DateField('Max date', null=False, blank=False)
    min_y = models.FloatField('Min Y', null=True, blank=True)
    max_y = models.FloatField('Max Y', null=True, blank=True)

    # Replica
    replica_up = models.BooleanField('Up', null=False, blank=False, default=False)
    replica_down = models.BooleanField('Down', null=False, blank=False, default=False)
    replica_dist = models.FloatField('Distance [mm]', null=False, blank=False, default=0.0)

    # Chart options
    h_grid = models.BooleanField('Horizontal grid', null=False, blank=False, default=False)
    v_grid = models.BooleanField('Vertical grid', null=False, blank=False, default=False)
    lines = models.BooleanField('Lines', null=False, blank=False, default=False)
    labels = models.BooleanField('Labels', null=False, blank=False, default=True)
    lin_trend = models.BooleanField('Lin trend', null=False, blank=False, default=False)
    poly_trend = models.BooleanField('Poly trend', null=False, blank=False, default=False)
    detrending = models.BooleanField('Detrending', null=False, blank=False, default=False)

    # Chart axis label
    x_axis_label = models.CharField('X axis label', null=False, blank=False, max_length=255, default='[Date]')
    y_axis_label = models.CharField('Y axis label', null=False, blank=False, max_length=255, default='[mm]')

    # Chart title
    title_part_1 = models.CharField('Title part 1', null=False, blank=False, max_length=255, default='coher.:')
    title_part_1_field = models.CharField('Title part 1 field', null=False, blank=False, max_length=255)
    title_part_2 = models.CharField('Title part 2', null=False, blank=False, max_length=255, default='vel.:')
    title_part_2_field = models.CharField('Title part 2 field', null=False, blank=False, max_length=255)
    title_part_3 = models.CharField('Title part 3', null=False, blank=False, max_length=255, default='v_stdev.:')
    title_part_3_field = models.CharField('Title part 3 field', null=False, blank=False, max_length=255)

    note = models.TextField('Note', null=True, blank=True)

    class Meta:
        verbose_name = 'Qps Timeseries Layer'

    def clean_fields(self, exclude=None):

        super().clean_fields(exclude=exclude)

        # check for vector layer  only
        if self.layer.geometrytype not in GEO_TYPE_VECTOR_LAYER_ALLOWED:
            raise ValidationError({'layer': _("Layer geometry type is not in allowed type: " +
                                              ", ".join(GEO_TYPE_VECTOR_LAYER_ALLOWED))})

        # Check for layer inside the project
        if not self.pk and len(QpsTimeseriesLayer.objects.filter(qps_timeseries_project=self.qps_timeseries_project,
                                                 layer=self.layer)) > 0:
            raise ValidationError({'layer': _("Layer already set for this project")})

        # Check date
        if self.min_date > self.max_date:
            raise ValidationError({'min_date': _("Min date must be lower than max date")})


    def __str__(self):
        return f"{self.qps_timeseries_project} - {self.layer}"
