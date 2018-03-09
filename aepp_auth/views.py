import urllib.parse as urlparse

import requests
from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet

from aepp_auth.backends import get_or_create_github_user_from_token
from aepp_auth.serializers import OAuthSerializer


class GithubAuth(GenericViewSet):

    serializer_class = OAuthSerializer

    def create(self, request, **kwargs):
        state = self.request.data.get('state')
        redirect_uri = self.request.data.get('redirect_uri')
        code = self.request.data.get('code')
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            json=dict(
                client_id=settings.GITHUB_OAUTH_CLIENT_ID,
                client_secret=settings.GITHUB_OAUTH_CLIENT_SECRET,
                code=code,
                redirect_uri=redirect_uri,
                state=state,
                grant_type='authorization_code'
            ),
            headers={'content-type': 'application/json'}
        )
        parsed_params = urlparse.parse_qs(response.text)
        response_json = {k: v[0] for k, v in parsed_params.items()}

        token = response_json['access_token']
        get_or_create_github_user_from_token(token)

        return JsonResponse(response_json)
