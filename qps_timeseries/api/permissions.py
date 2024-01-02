# coding=utf-8
""""
API REST permission classes for Qps Timeseries
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-15'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from rest_framework.permissions import BasePermission
from qdjango.models import (
    Layer,
    Project
)

from qps_timeseries.models import QpsTimeseriesProject

import logging

logger = logging.getLogger('qps_timeseries')


class GetLayerInfoPermission(BasePermission):
    """
    Allows access only to users have permission run_model
    """

    def has_permission(self, request, view):

        # get
        try:
            layer = Layer.objects.get(pk=view.kwargs['pk'])

            # Check permission on QProcessingProject and on Porject

            return request.user.has_perm('qdjango.view_project', layer.project)
        except Exception as e:
            logger.debug(f'[QPS_TIMESERIES] - GetLayerInfoPermission: {e}')
            return False


class PlotDataPermission(BasePermission):
    """ Check permission for plot data """

    def has_permission(self, request, view):

        try:

            # In this way is checked ifa qps_tmiserise project is active
            qpsts = QpsTimeseriesProject.objects.get(project_id=view.kwargs['project_pk'])

            return request.user.has_perm('qdjango.view_project', qpsts.project)

        except Exception as e:
            logger.debug(f'[QPS_TIMESERIES] - PlotDataPermission: {e}')
            return False