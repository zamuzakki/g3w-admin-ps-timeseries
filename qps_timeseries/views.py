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

    def get_form_kwargs(self):
        fkwargs = super().get_form_kwargs()

        # Add QpsTimeseriesProject instance
        fkwargs['qps_timeseries_project'] = QpsTimeseriesProject.objects.get(pk=self.kwargs['qps_prj_pk'])

        return fkwargs


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

