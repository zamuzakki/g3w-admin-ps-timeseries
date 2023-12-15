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



