import requests
from rest_framework import authentication, exceptions

from aepp_auth.models import GithubUser


def get_or_create_github_user_from_token(token):
    user_data_response = requests.get(
        f'https://api.github.com/user?access_token={token}'
    )
    user_data = user_data_response.json()
    user_id = user_data['id']

    user = None
    try:
        user = GithubUser.objects.get(user_id=user_id)
        user.token = token
        user.username = user_data['login']
        user.email = user_data['email']
        user.save(update_fields=['token', 'username', 'email'])
    except GithubUser.DoesNotExist:
        if user_data_response.status_code == 200:
            user = GithubUser.objects.create(
                user_id=user_id,
                token=token,
                username=user_data['login'],
                email=user_data['email']
            )
    return user


class GithubBackend(authentication.BaseAuthentication):

    def authenticate(self, request):
        github_token = request.META.get('HTTP_X_GH_TOKEN')
        if not github_token:
            return None

        user = None
        if github_token:
            try:
                user = GithubUser.objects.get(token=github_token)
            except GithubUser.DoesNotExist:
                user = get_or_create_github_user_from_token(github_token)

        if user is None:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
