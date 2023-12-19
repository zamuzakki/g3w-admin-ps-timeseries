from django.dispatch import receiver
from django.templatetags.static import static

from core.signals import initconfig_plugin_start

@receiver(initconfig_plugin_start)
def set_initconfig_value(sender, **kwargs):
    """
    Set base qps_timeseries data for initconfig
    """
    return {
        'qps_timeseries': {
            'gid': "{}:{}".format(kwargs['projectType'], kwargs['project']),
            'jsscripts': [
                static('qplotly/polyfill.min.js'),     # Tested with: g3w-admin@v3.7
                static('qplotly/plotly-1.52.2.min.js') # Tested with: g3w-admin@v3.7
            ],
        },
    }