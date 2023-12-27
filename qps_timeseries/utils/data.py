# coding=utf-8
"""" Utility functions and classes for data management

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-27'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from qgis.PyQt.QtCore import (
    QDate,
    QRegExp,
    Qt
)


def get_base_plot_data(qgs_feature, qgs_layer, qps_timeseries_layer=None):
    """
    Get base plot data

    :param qgs_feature: QgsFeature
    :param qps_timeseries_layer: QgsVectorLayer
    :return type: dict
    :return: Dict of base plot data
    """

    attrs = qgs_feature.attributes()

    x, y = [], []  # lists containg x,y values
    infoFields = []  # list of the fields containing info to be displayed

    ps_source = qgs_layer.source()
    ps_fields = qgs_layer.dataProvider().fields()

    providerType = qgs_layer.providerType()
    uri = ps_source
    subset = ""

    # if providerType == 'ogr' and ps_source.lower().endswith(".shp"):
    # Shapefile
    for idx, fld in enumerate(ps_fields):
        if QRegExp("D\\d{8}", Qt.CaseInsensitive).indexIn(fld.name()) < 0:
            # info fields are all except those containing dates
            infoFields.append(fld.name())
        else:

            x_date = QDate.fromString(fld.name()[1:], "yyyyMMdd").toPyDate()

            # Only for date >= qps_timeseries_layer.min_date and <= qps_timeseries_layer.max_date
            if qps_timeseries_layer:
                if x_date >= qps_timeseries_layer.min_date and x_date <= qps_timeseries_layer.max_date:
                    x.append(x_date)
                    y.append(float(attrs[idx]))
            else:
                x.append(x_date)
                y.append(float(attrs[idx]))


    return {
        'x': x,
        'y': y,
        'fields': infoFields
    }
