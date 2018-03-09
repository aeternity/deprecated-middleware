from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from aepp_auth.views import GithubAuth

urlpatterns = [
    url(r'^github/', csrf_exempt(GithubAuth.as_view({'post': 'create'})))
]
