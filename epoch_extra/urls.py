from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from epoch_extra.views import BalanceView, AensViewSet

router = DefaultRouter()

router.register(r'^name', AensViewSet, base_name='name')


urlpatterns = [
    url(r'^balance/(?P<pk>.+)', csrf_exempt(BalanceView.as_view({'get': 'retrieve'}))),
    url(r'<')
] + router.urls
