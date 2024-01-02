# coding=utf-8
""""
    Base testing module
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

__author__ = 'lorenzetti@gis3w.it'
__date__ = '2023-12-28'
__copyright__ = 'Copyright 2015 - 2023, Gis3w'
__license__ = 'MPL 2.0'

from django.test import TestCase, override_settings
from django.core.files import File
from core.models import G3WSpatialRefSys, Group as CoreGroup
from usersmanage.tests.utils import setup_testing_user
from qdjango.utils.data import QgisProject
from qps_timeseries.models import (
    QpsTimeseriesProject,
    QpsTimeseriesLayer
)
import os
import datetime

CURRENT_PATH = os.path.dirname(__file__)
TEST_BASE_PATH = 'data/'
DATASOURCE_PATH = '{}/{}project_data'.format(CURRENT_PATH, TEST_BASE_PATH)

QGS_PROJECT_FILE = 'projects/qps_timeseries.qgs'



@override_settings(
    CACHES={
        'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'some',
        }
    },
    DATASOURCE_PATH=DATASOURCE_PATH,
    LANGUAGE_CODE='en',
    LANGUAGES = (
        ('en', 'English'),
    ),
)
class TestQpsTimeseriesBase(TestCase):

    fixtures = ['BaseLayer.json',
                'G3WMapControls.json',
                'G3WSpatialRefSys.json',
                'G3WGeneralDataSuite.json'
                ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        setup_testing_user(cls)

        cls.qgis_file = os.path.join(CURRENT_PATH, TEST_BASE_PATH, QGS_PROJECT_FILE)

    @classmethod
    def setUp(cls):
        # main project group
        cls.project_group = CoreGroup(name='QProcessing', title='QProcessing', header_logo_img='',
                                      srid=G3WSpatialRefSys.objects.get(auth_srid=4326))
        cls.project_group.save()

        # Add projects to DB
        qgis_file = File(open(cls.qgis_file, 'r'))
        cls.project = QgisProject(qgis_file)
        cls.project.title = 'Qps Timeseries Test Project'
        cls.project.group = cls.project_group
        cls.project.save()

    def create_instance_qpstimseriesproject(self):
        """ Create a QpsTimeseriesProject and QpsTimeseriesLayer instance """

        qpsts_project = QpsTimeseriesProject(project=self.project.instance)
        qpsts_project.save()
        QpsTimeseriesLayer(
            qps_timeseries_project=qpsts_project,
            layer=self.project.instance.layer_set.all()[0],
            min_date=datetime.date(2015, 2, 8),
            max_date=datetime.date(2021, 12, 21)
        ).save()

        return qpsts_project