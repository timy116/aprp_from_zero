from django.conf.urls import url

from apps.accounts.views import (
    login_view,
)

urlpatterns = [
    url(r'^login/', login_view, name='login'),
]
