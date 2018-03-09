from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from epoch_extra.views import BalanceView

# router = DefaultRouter()

urlpatterns = [
    url(r'^balance/(?P<pk>.+)', csrf_exempt(BalanceView.as_view({'get': 'retrieve'})))
]
