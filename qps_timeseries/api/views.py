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
from core.utils.qgisapi import get_qgis_layer
from qdjango.models import Layer
from qgis.core import QgsFeature
from qgis.PyQt.QtCore import QDate, QRegExp, Qt
from .permissions import GetLayerInfoPermission


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
        attrs = qfeature.attributes()

        x, y = [], []  # lists containg x,y values
        infoFields = []  # list of the fields containing info to be displayed

        ps_source = qlayer.source()
        ps_fields = qlayer.dataProvider().fields()

        providerType = qlayer.providerType()
        uri = ps_source
        subset = ""

        #if providerType == 'ogr' and ps_source.lower().endswith(".shp"):
        # Shapefile
        for idx, fld in enumerate(ps_fields):
            if QRegExp("D\\d{8}", Qt.CaseInsensitive).indexIn(fld.name()) < 0:
                # info fields are all except those containing dates
                infoFields.append(fld.name())
            else:
                x.append(QDate.fromString(fld.name()[1:], "yyyyMMdd").toPyDate())
                y.append(float(attrs[idx]))

        self.results.update({
            'x': x,
            'y': y,
            'fields': infoFields
        })

        return Response(self.results.results)


class QpsTimeseriesPlotDataApiView(G3WAPIView):
    """
    API view for get data plot
    """

    def get(self, request, *args, **kwargs):

        DELTA_1 = 5
        DELTA_2 = 0

        TITLE = 'PS Time Series Viewer<br><sub>coher.: <pid> vel.: <pid> v_stdev.: <pid></sub>'
        X = ['2013-08-04 22:23:00', '2013-09-04 22:23:00', '2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00']
        Y = [4, 1, 7, 1, 4]

        XGRID = True
        YGRID = True

        ## WebGL optimization
        ## https://plotly.com/javascript/webgl-vs-svg/
        TYPE = 'scattergl'

        ## Fake Data
        ## https://plotly.com/javascript/
        self.results.results.update({
            'data':  [
              ## TRACE0 = scatter
              {
                'x': X,
                'y': Y,
                'mode': 'markers',
                'type': TYPE,
                'name': 'Scatter',
                'marker': {
                  'size': 8,
                  'color': 'black',
                  'symbol': 'square',
                },
              },
              ## TRACE1 = replica + delta
              {
                'visible': False if 0 == DELTA_1 else True,
                # 'x': [] if 0 == DELTA_1 else X,
                'y': [] if 0 == DELTA_1 else [y + DELTA_1 for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica +' + str(DELTA_1),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TRACE2 = replica - delta
              {
                'visible': False if 0 == DELTA_2 else True,
                # 'x': [] if 0 == DELTA_2 else X,
                'y': [] if 0 == DELTA_2 else [y - DELTA_2 for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica -' + str(DELTA_2),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TRACE3 = trend line
              {
                'x': [
                  '2013-08-04 22:23:00',
                  '2013-09-04 22:23:00',
                  '2013-10-04 22:23:00',
                  '2013-11-04 22:23:00',
                  '2013-12-04 22:23:00',
                ],
                'y': [3, 2, 1.5, 2, 4],
                'mode': 'lines',
                'type': TYPE,
                'name': 'Lin Trend',
                'line': {
                  'color': 'red',
                },
              },
              ## TRACE5 = trend poly
              {
                'visible': 'legendonly',
                'x': [
                  '2013-08-04 22:23:00',
                  '2013-09-04 22:23:00',
                  '2013-10-04 22:23:00',
                  '2013-11-04 22:23:00',
                  '2013-12-04 22:23:00',
                ],
                'y': [3, 2, 1.5, 2, 4],
                'mode': 'lines',
                'type': 'scatter',
                'name': 'Poly Trend',
                # https://plotly.com/javascript/reference/scatter/#scatter-line-shape
                # https://plotly.com/javascript/reference/scattergl/#scattergl-line-shape
                'line': {
                  'shape': 'spline',
                  'smoothing': 1.3,
                  'color': 'green'
                },
              },
            ],
            'layout': {
              'xaxis': {
                'showgrid': XGRID,
                'title': '[Date]',
                'autorange': True,
                'linecolor': 'rgb(238, 238, 238)',
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
                'title': '[mm]',
                'autorange': True,
                # 'range': [0 - DELTA, 8 + DELTA],
                'linecolor': 'rgb(238, 238, 238)',
                'mirror': True,
                'ticks': 'outside',
                'tickcolor': '#000',
                'zeroline': False,
                'rangeslider': { },
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
              'editable': True,
              'responsive': True,
              'scrollZoom': True,
              'toImageButtonOptions': { 'filename': 'qps-timeseries' },
            },
        })

        return Response(self.results.results)
