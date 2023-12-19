# coding=utf-8
""""
Views module for Qps_timeseries
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-04'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.views.generic import \
    ListView, \
    CreateView, \
    UpdateView, \
    View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required
from core.mixins.views import G3WRequestViewMixin, G3WAjaxDeleteViewMixin
from .models import (
    QpsTimeseriesProject,
    QpsTimeseriesLayer
)
from .forms import (
    QpsTimeseriesProjectForm,
    QpsTimeseriesLayerForm
)
from .config import QPS_TIMESERIES_API_LAYERINFO

import json

class QpsTimeseriesProjectListView(ListView):
    """List qps_timeseries projects view."""
    template_name = 'qps_timeseries/projects_list.html'
    model = QpsTimeseriesProject

    @method_decorator(permission_required('qps_timeseries.add_qpstimeseriesproject', return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QpsTimeseriesProjectAddView(G3WRequestViewMixin, CreateView):
    """
    Create view for qps_timeseries project
    """
    form_class = QpsTimeseriesProjectForm
    template_name = 'qps_timeseries/project_form.html'
    success_url = reverse_lazy('qpstimeseries-project-list')

    @method_decorator(permission_required('qps_timeseries.add_qpstimeseriesproject', return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QpsTimeseriesProjectUpdateView(G3WRequestViewMixin, UpdateView):
    """
    Update view for qps_timeseries project
    """
    model = QpsTimeseriesProject
    form_class = QpsTimeseriesProjectForm
    template_name = 'qps_timeseries/project_form.html'
    success_url = reverse_lazy('qpstimeseries-project-list')

    @method_decorator(
        permission_required('qps_timeseries.change_qpstimeseriesproject',
                            (QpsTimeseriesProject, 'pk', 'pk'), return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QpsTimeseriesProjectDeleteView(G3WAjaxDeleteViewMixin, SingleObjectMixin, View):
    """
    Delete qps_timeseries project Ajax view
    """
    model = QpsTimeseriesProject

    @method_decorator(
        permission_required('qps_timeseries.delete_qpstimeseriesproject',
                            (QpsTimeseriesProject, 'pk', 'pk'), return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QpsTimeseriesLayersListView(ListView):
    """List qps_timeseries projects layers view."""

    template_name = 'qps_timeseries/layers_list.html'
    model = QpsTimeseriesLayer

    def get_queryset(self):
        return QpsTimeseriesLayer.objects.filter(qps_timeseries_project_id=self.kwargs['qps_prj_pk'])

    @method_decorator(permission_required('qps_timeseries.add_qpstimeserieslayer', return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Add QpsProject instance pk
        ctx['qps_timeseries_project_id'] = self.kwargs['qps_prj_pk']

        return ctx


class QpsTimeseriesLayerMixinView(object):

    def get_context_data(self, **kwargs):
        ctx = ctx = super().get_context_data(**kwargs)

        ctx['layerinfo_api_url_base'] = f'qps_timeseries/{QPS_TIMESERIES_API_LAYERINFO}/'

        ctx['update'] = False

        return ctx

    def get_form_kwargs(self):
        fkwargs = super().get_form_kwargs()

        # Add QpsTimeseriesProject instance
        fkwargs['qps_timeseries_project'] = QpsTimeseriesProject.objects.get(pk=self.kwargs['qps_prj_pk'])

        return fkwargs

    def get_success_url(self):

        return reverse_lazy('qpstimeseries-project-layer-list', args=[self.kwargs['qps_prj_pk']])


class QpsTimeseriesLayerAddView(QpsTimeseriesLayerMixinView, G3WRequestViewMixin, CreateView):
    """
    Create view for qps_timeseries project layer
    """
    form_class = QpsTimeseriesLayerForm
    template_name = 'qps_timeseries/layer_form.html'

    @method_decorator(permission_required('qps_timeseries.add_qpstimeserieslayer', return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QpsTimeseriesLayerUpdateView(QpsTimeseriesLayerMixinView, G3WRequestViewMixin, UpdateView):
    """
    Update view for qps_timeseries project layer
    """
    model = QpsTimeseriesLayer
    form_class = QpsTimeseriesLayerForm
    template_name = 'qps_timeseries/layer_form.html'

    @method_decorator(
        permission_required('qps_timeseries.change_qpstimeserieslayer',
                            (QpsTimeseriesLayer, 'pk', 'pk'), return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Add update status
        ctx['update'] = True

        # Add initial value
        ctx['initial'] = json.dumps({
            'id_min_date': str(self.object.min_date),
            'id_max_date': str(self.object.min_date),
            'id_title_part_1_field': self.object.title_part_1_field,
            'id_title_part_2_field': self.object.title_part_2_field,
            'id_title_part_3_field': self.object.title_part_3_field,
        })

        return ctx


class QpsTimeseriesLayerDeleteView(QpsTimeseriesLayerMixinView, G3WAjaxDeleteViewMixin, SingleObjectMixin, View):
    """
    Delete qps_timeseries project layer Ajax view
    """
    model = QpsTimeseriesLayer

    @method_decorator(
        permission_required('qps_timeseries.delete_qpstimeserieslayer',
                            (QpsTimeseriesLayer, 'pk', 'pk'), return_403=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

from django.views.generic import View
from django.http.response import JsonResponse

class QPSTimeseriesPlot(View):

    def get(self, *args, **kwargs):

        DELTA_U = 5
        DELTA_D = 0

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
        return JsonResponse({
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
                'visible': False if 0 == DELTA_U else True,
                'x': [] if 0 == DELTA_U else X,
                'y': [] if 0 == DELTA_U else [y + DELTA_U for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica +' + str(DELTA_U),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TRACE2 = replica - delta
              {
                'visible': False if 0 == DELTA_D else True,
                'x': [] if 0 == DELTA_D else X,
                'y': [] if 0 == DELTA_D else [y - DELTA_D for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica -' + str(DELTA_D),
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
                'title': '[mm]',
                'autorange': True,
                # 'range': [0 - DELTA, 8 + DELTA],
                'linecolor': 'black',
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