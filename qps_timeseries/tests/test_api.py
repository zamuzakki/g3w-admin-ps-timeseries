# coding=utf-8
""""
    API testing for qps_timeseries module
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-28'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.urls import reverse
from .base import TestQpsTimeseriesBase
import datetime
import json

class TestQpsTimeseriesApi(TestQpsTimeseriesBase):


    def test_init_plugin_start(self):
        """
        Test init_plugin_start signal
        """

        self.client.login(username=self.test_user1.username, password=self.test_user1.username)

        # Get initconfig project without plugin
        url = reverse('group-map-config', args=[
            self.project.instance.group.slug, 'qdjango',
            self.project.instance.pk
        ])
        response = self.client.get(url)

        jcontent = json.loads(response.content)

        self.assertFalse('qps_timeseries' in jcontent['group']['plugins'])

        # Create a QpsTimeseriesProject and QpsTimeseriesLayer instance
        self.create_instance_qpstimseriesproject()

        response = self.client.get(url)

        jcontent = json.loads(response.content)

        # check qps_timeseries into plugins section
        self.assertTrue('qps_timeseries' in jcontent['group']['plugins'])

        plugin = jcontent['group']['plugins']['qps_timeseries']

        self.assertEqual(plugin['gid'], 'qdjango:{}'.format(
            self.project.instance.pk))

        self.assertEqual(len(plugin['layers']), 1)

        self.client.logout()

    def test_info_layer(self):
        """
        Testing `qpstimeseries-api-layerinfo`
        """

        # Test permission:
        # As anonymoususer

        layer = self.project.instance.layer_set.all()[0]
        url = reverse('qpstimeseries-api-layerinfo', kwargs={'pk': layer.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

        # Test as admin
        self.client.login(username=self.test_user1.username, password=self.test_user1.username)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        jres = json.loads(response.content)

        self.assertTrue(jres['result'])
        self.assertEqual(len(jres['x']), 357)
        self.assertEqual(len(jres['y']), 357)
        self.assertEqual(jres['fields'], ['pid', 'cluster_la', 'mp_type', 'latitude', 'longitude', 'easting', 'northing', 'height', 'height_wgs', 'line', 'pixel', 'rmse', 'temporal_c', 'amplitude_', 'incidence_', 'track_angl', 'los_east', 'los_north', 'los_up', 'mean_veloc', 'mean_vel_1', 'accelerati', 'accelera_1', 'seasonalit', 'seasonal_1'])

        self.client.logout()

    def test_plot_data(self):
        """ Test qps-timeseries-api-plot-data api """

        # Test permission:
        # As anonymoususer

        layer = self.project.instance.layer_set.all()[0]

        url = reverse('qpstimeseries-api-plot-data', kwargs={
            'project_pk': self.project.instance.pk,
            'layer_id': layer.qgs_layer_id,
            'feature_id': 1
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

        # As admin level 1
        # NO QpsTimeseriesProject instance active

        self.client.login(username=self.test_user1.username, password=self.test_user1.username)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        
        # QpsTimeseriesProject instance active
        qpsts = self.create_instance_qpstimseriesproject()
        qpsts_layer = qpsts.layers.all()[0]

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        jres = json.loads(response.content)

        self.assertTrue(jres['result'])

        self.assertEqual(len(jres['data'][0]['x']), 357)
        self.assertEqual(len(jres['data'][0]['y']), 357)
        self.assertEqual(len(jres['data'][1]['y']), 0)
        self.assertEqual(len(jres['data'][2]['y']), 0)
        self.assertFalse('error_y' in jres['data'][0])

        self.assertEqual(jres['config'], {'displayModeBar': True, 'editable': False, 'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'], 'responsive': True, 'scrollZoom': True, 'toImageButtonOptions': {'filename': 'qps-timeseries'}})

        # Change data range
        # -----------------
        qpsts_layer.min_date = datetime.date(2015, 2, 8)
        qpsts_layer.max_date = datetime.date(2015, 5, 27)

        qpsts_layer.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        jres = json.loads(response.content)

        self.assertEqual(len(jres['data'][0]['x']), 10)
        self.assertEqual(len(jres['data'][0]['y']), 10)
        self.assertEqual(len(jres['data'][1]['y']), 0)
        self.assertEqual(len(jres['data'][2]['y']), 0)


        # Add replica up and down
        # -----------------------

        qpsts_layer.replica_up = True
        qpsts_layer.replica_down = True
        qpsts_layer.replica_dist = 10

        qpsts_layer.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        jres = json.loads(response.content)

        self.assertEqual(len(jres['data'][0]['x']), 10)
        self.assertEqual(len(jres['data'][0]['y']), 10)
        self.assertEqual(len(jres['data'][1]['y']), 10)
        self.assertEqual(len(jres['data'][2]['y']), 10)

        # Check y replica's values
        for y in jres['data'][0]['y']:
            index = jres['data'][0]['y'].index(y)
            self.assertEqual(jres['data'][1]['y'][index], y + 10)

        # Add line trend poly trend and std
        # ---------------------------------
        qpsts_layer.lin_trend = True
        qpsts_layer.poly_trend = True
        qpsts_layer.std = True

        qpsts_layer.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        jres = json.loads(response.content)

        self.assertEqual(len(jres['data'][0]['x']), 10)
        self.assertEqual(len(jres['data'][0]['y']), 10)
        self.assertEqual(len(jres['data'][1]['y']), 10)
        self.assertEqual(len(jres['data'][2]['y']), 10)
        self.assertEqual(len(jres['data'][3]['x']), 10)
        self.assertEqual(len(jres['data'][3]['y']), 10)
        self.assertEqual(len(jres['data'][4]['x']), 10)
        self.assertEqual(len(jres['data'][4]['y']), 10)


        self.assertEqual(jres['data'][0]['error_y']['type'], 'data')
        self.assertEqual(jres['data'][0]['error_y']['symmetric'], True)
        self.assertEqual(len(jres['data'][0]['error_y']['array']), 10)
        # Test config i.e. for layout
        # ---------------------------

        qpsts_layer.h_grid = True
        qpsts_layer.v_grid = True
        qpsts_layer.lines = True
        qpsts_layer.labels = True
        qpsts_layer.x_axis_label = 'Label x'
        qpsts_layer.y_axis_label = 'Label y'
        qpsts_layer.title_part_1_field = 'pid'
        qpsts_layer.title_part_2_field = 'pid'
        qpsts_layer.title_part_3_field = 'pid'

        qpsts_layer.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        jres = json.loads(response.content)

        self.assertEqual(jres['layout']['xaxis']['title'], 'Label x')
        self.assertTrue(jres['layout']['xaxis']['showgrid'])
        self.assertEqual(jres['layout']['yaxis']['title'], 'Label y')
        self.assertTrue(jres['layout']['yaxis']['showgrid'])

        self.assertEqual(jres['layout']['title']['text'], 'coher.: 1ODQB00afP vel.: 1ODQB00afP v_stdev.: 1ODQB00afP ')

        self.client.logout()







