from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    SomeProtectedView
)

urlpatterns = [

    path(
        'api/some-protected-view/<int:feature_id>',
        login_required(SomeProtectedView.as_view()),
        name='some-protected-view'
    ),

]