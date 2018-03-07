from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from faucet.views import FaucetView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', csrf_exempt(FaucetView.as_view({'post': 'create'})))
]
