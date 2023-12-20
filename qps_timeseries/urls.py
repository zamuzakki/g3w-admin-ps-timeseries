# coding=utf-8
"""" Urls module for qps_timeseries
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-04'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.urls import path
from base.urls import G3W_SITETREE_I18N_ALIAS
from django.contrib.auth.decorators import login_required
from .views import (
    QpsTimeseriesProjectListView,
    QpsTimeseriesProjectAddView,
    QpsTimeseriesProjectUpdateView,
    QpsTimeseriesProjectDeleteView,
    QpsTimeseriesLayersListView,
    QpsTimeseriesLayerAddView,
    QpsTimeseriesLayerUpdateView,
    QpsTimeseriesLayerDeleteView
)

# For sitree bar translation
G3W_SITETREE_I18N_ALIAS.append('qps_timeseries')


urlpatterns = [

     #########################################################
     # Projects
     #########################################################
     path(
         'projects/',
         login_required(QpsTimeseriesProjectListView.as_view()),
         name='qpstimeseries-project-list'
     ),

     path(
         'projects/add/',
         login_required(QpsTimeseriesProjectAddView.as_view()),
         name='qpstimeseries-project-add'
     ),

     # path(
     #     'projects/update/<int:pk>/',
     #     login_required(SimpleRepoProjectUpdateView.as_view())
     #     name='qpstimeseries-project-update'
     # ),

     path(
         'projects/delete/<int:pk>/',
         login_required(QpsTimeseriesProjectDeleteView.as_view()),
         name='qpstimeseries-project-delete'
     ),

     #########################################################
     # Layers
     #########################################################
     path(
        'projects/<int:qps_prj_pk>/layers/',
        login_required(QpsTimeseriesLayersListView.as_view()),
        name='qpstimeseries-project-layer-list'
     ),

     path(
         'projects/<int:qps_prj_pk>/layers/add/',
         login_required(QpsTimeseriesLayerAddView.as_view()),
         name='qpstimeseries-project-layer-add'
     ),

     path(
        'projects/<int:qps_prj_pk>/layers/update/<int:pk>/',
        login_required(QpsTimeseriesLayerUpdateView.as_view()),
        name='qpstimeseries-project-layer-update'
     ),

     path(
         'projects/<int:qps_prj_pk>/layers/delete/<int:pk>/',
         login_required(QpsTimeseriesLayerDeleteView.as_view()),
         name='qpstimeseries-project-layer-delete'
     ),

]