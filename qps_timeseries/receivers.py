# coding=utf-8
"""Ps Time series signals receiver module.

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-13'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'


from django.dispatch import receiver
from django.templatetags.static import static
from .models import QpsTimeseriesProject

from core.signals import initconfig_plugin_start

@receiver(initconfig_plugin_start)
def set_initconfig_value(sender, **kwargs):
    """
    Set base qps_timeseries data for initconfig
    """

    # Check for activation  plugin
    try:
        qpstp = QpsTimeseriesProject.objects.get(project_id=kwargs['project'])
    except:
        return None

    return {
        'qps_timeseries': {
            'gid': "{}:{}".format(kwargs['projectType'], kwargs['project']),
            'layers': [l.layer.qgs_layer_id for l in qpstp.layers.all()],
            'jsscripts': [
                static('qplotly/polyfill.min.js'),     # Tested with: g3w-admin@v3.7
                static('qplotly/plotly-1.52.2.min.js') # Tested with: g3w-admin@v3.7
            ],
        },
    }