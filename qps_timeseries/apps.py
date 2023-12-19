from django.apps import AppConfig


class QpsTimeseriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qps_timeseries'

    def ready(self):

        # import signal handlers
        from . import receivers
