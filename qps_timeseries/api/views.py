# coding=utf-8
""""
Qps Timeseries REST API views
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-13'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from core.api.base.views import G3WAPIView, Response
from core.utils.qgisapi import (
    get_qgis_layer,
    get_layer_fids_from_server_fids
)
from qdjango.models import Layer
from qps_timeseries.utils import (
    get_base_plot_data,
    get_line_trend_plot_data
)
from qps_timeseries.models import QpsTimeseriesProject
from qgis.core import QgsFeature
from qgis.PyQt.QtCore import (
    QDate,
    QRegExp,
    Qt
)
from .permissions import (
    GetLayerInfoPermission,
    PlotDataPermission
)


class QpsTimeseriesLayerinfoApiView(G3WAPIView):
    """
    API for get information about PS Timeseries layer
    """

    # Todo: add permisisons classes
    permission_classes = (
        GetLayerInfoPermission,
    )

    def get(self, request, *args, **kwargs):

        try:
            layer = Layer.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist as e:
            raise APIException('Layer object not found into DB')

        # Get a feature for layer
        qlayer = get_qgis_layer(layer)


        # Following code from QGIS desktop plugin PS Tme series
        # https://gitlab.com/faunalia/ps-speed/-/blob/master/pstimeseries_plugin.py?ref_type=heads#L112
        # ---------------------------------------------------------------------------------------------
        qfeature = QgsFeature()
        qfeatures = qlayer.getFeatures()
        qfeatures.nextFeature(qfeature)

        self.results.update(get_base_plot_data(qfeature, qlayer))

        return Response(self.results.results)


class QpsTimeseriesPlotDataApiView(G3WAPIView):
    """
    API view for get data plot
    """

    permission_classes = (
        PlotDataPermission,
    )

    def get(self, request, *args, **kwargs):

        # Get QGIS layer instance
        layer = Layer.objects.get(project_id=kwargs['project_pk'], qgs_layer_id=kwargs['layer_id'])
        qlayer = get_qgis_layer(layer)
        qfeature = qlayer.getFeature(get_layer_fids_from_server_fids([str(kwargs['feature_id'])], qlayer)[0])

        # Get QPS Timeseries layer property
        qpst_project = QpsTimeseriesProject.objects.get(project_id=kwargs['project_pk'])
        qpst_layer = qpst_project.layers.get(layer=layer)

        # Get base data
        base_data_plot = get_base_plot_data(qfeature, qlayer, qpst_layer)

        ## WebGL optimization
        ## https://plotly.com/javascript/webgl-vs-svg/
        TYPE = 'scattergl'

        X = base_data_plot['x']
        Y = base_data_plot['y']

        TITLE = (f'{qpst_layer.title_part_1} {qfeature[qpst_layer.title_part_1_field]} '
                 f'{qpst_layer.title_part_2} {qfeature[qpst_layer.title_part_2_field]} '
                 f'{qpst_layer.title_part_3} {qfeature[qpst_layer.title_part_3_field]} ')

        XGRID = qpst_layer.h_grid
        YGRID = qpst_layer.v_grid

        DELTA_UP = qpst_layer.replica_dist if qpst_layer.replica_up else 0
        DELTA_DOWN = qpst_layer.replica_dist if qpst_layer.replica_down else 0

        data = [
                ## TRACE0 = scatter
                {
                    'x': X,
                    'y': Y,
                    'type': TYPE,
                    'name': 'Scatter',
                    'marker': {
                        'size': 8,
                        'color': 'black',
                        'symbol': 'square',
                    }
                },
                ## TRACE1 = replica + delta up
                {
                    'visible': False if 0 == DELTA_UP else True,
                    # 'x': [] if 0 == DELTA_1 else X,
                    'y': [] if 0 == DELTA_UP else [y + DELTA_UP for y in Y],
                    'mode': 'scatter',
                    'type': TYPE,
                    'name': 'Replica +' + str(DELTA_UP),
                    'marker': {
                        'size': 8,
                        'color': 'blue',
                        'symbol': 'square',
                    },
                },
                ## TRACE2 = replica - delta down
                {
                    'visible': False if 0 == DELTA_DOWN else True,
                    'y': [] if 0 == DELTA_DOWN else [y - DELTA_DOWN for y in Y],
                    'mode': 'scatter',
                    'type': TYPE,
                    'name': 'Replica -' + str(DELTA_DOWN),
                    'marker': {
                        'size': 8,
                        'color': 'blue',
                        'symbol': 'square',
                    },
                },
            ]

        # Add TRACE3 if Lin trend option is enabled
        if qpst_layer.lin_trend:
            lin_trend = get_line_trend_plot_data(X,Y)
            data.append({
                'x': lin_trend[0],
                'y': lin_trend[1],
                'mode': 'lines',
                'type': TYPE,
                'name': 'Lin Trend',
                'line': {
                  'color': 'red',
                },
            })

        # Add TRACE4 if Poly trend option is enabled
        if qpst_layer.poly_trend:
            lin_trend = get_line_trend_plot_data(X, Y, 3)
            data.append({
                'visible': True,
                'x': lin_trend[0],
                'y': lin_trend[1],
                'mode': 'lines',
                'type': 'scatter',
                'name': 'Poly Trend',
                'line': {
                    'shape': 'spline',
                    'smoothing': 1.3,
                    'color': 'green'
                },
            })


        self.results.results.update({
            'data': data,
            'layout': {
                'xaxis': {
                    'showgrid': XGRID,
                    'title': qpst_layer.x_axis_label if qpst_layer.labels else None,
                    'autorange': True,
                    'linecolor': 'black',
                    'mirror': True,
                    'ticks': 'outside',
                    'tickcolor': '#000',
                    'zeroline': False,
                    'rangeslider': {
                        # 'range': [ '2013-07-04 22:23:00', '2014-01-04 22:23:00' ],
                        # 'range': [ '2013', '2014' ],
                        # 'range': [ ],
                        'thickness': 0.1,
                    },
                    'type': 'date'
                },
                'yaxis': {
                    'showgrid': YGRID,
                    'title': qpst_layer.y_axis_label if qpst_layer.labels else None,
                    'autorange': True,
                    # 'range': [0 - DELTA, 8 + DELTA],
                    'linecolor': 'black',
                    'mirror': True,
                    'ticks': 'outside',
                    'tickcolor': '#000',
                    'zeroline': False,
                    'rangeslider': {},
                    'type': 'linear',
                },
                'title': {
                    "font": {
                        "size": 20,
                        "color": "blue",
                        "family": "monospace",
                    },
                    'text': TITLE,
                },
                'hovermode': 'closest',
            },
            'config': {
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'],
                'editable': False,
                'responsive': True,
                'scrollZoom': True,
                'toImageButtonOptions': {'filename': 'qps-timeseries'},
            },
        })

        return Response(self.results.results)
