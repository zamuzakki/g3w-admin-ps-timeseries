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
import json

class TestQpsTimeseriesApi(TestQpsTimeseriesBase):

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



