from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    QPSTimeseriesPlot
)

urlpatterns = [

    path(
        'api/plot/<str:layer_id>/<int:feature_id>',
        login_required(QPSTimeseriesPlot.as_view()), # TODO: check if "login_required" is really needed 
        name='qps-timeseries-plot'
    ),

]