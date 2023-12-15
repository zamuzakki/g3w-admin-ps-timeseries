# coding=utf-8
""""
API REST urls
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-13'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.urls import path
from .api.views import QpsTimeseriesLayerinfoApiView
from .config import QPS_TIMESERIES_API_LAYERINFO

urlpatterns = [
    path(f'{QPS_TIMESERIES_API_LAYERINFO}/<int:pk>/', QpsTimeseriesLayerinfoApiView.as_view(),
         name='qpstimeseries-api-layerinfo'),
]