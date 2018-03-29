import requests
from django.db import transaction
from rest_framework import authentication, exceptions

from aepp_auth.models import GithubUser, AeternityUser


def get_or_create_github_user_from_token(token):
    user_data_response = requests.get(
        f'https://api.github.com/user?access_token={token}'
    )
    user_data = user_data_response.json()
    user_id = user_data['id']

    github_user = None
    with transaction.atomic():
        try:
            github_user = GithubUser.objects.get(user_id=user_id)
            github_user.token = token
            github_user.username = user_data['login']
            github_user.email = user_data['email']
            github_user.save(update_fields=['token', 'username', 'email'])
        except GithubUser.DoesNotExist:
            if user_data_response.status_code == 200:
                user, _ = AeternityUser.objects.get_or_create(
                    username=user_data['login'],
                    email=user_data['email']
                )

                github_user = GithubUser.objects.create(
                    user=user,
                    github_user_id=user_id,
                    token=token,
                )

    return github_user


class GithubBackend(authentication.BaseAuthentication):

    def authenticate(self, request):
        github_token = request.META.get('HTTP_X_GH_TOKEN')
        if not github_token:
            return None

        github_user = None
        if github_token:
            try:
                github_user = GithubUser.objects.get(token=github_token)
            except GithubUser.DoesNotExist:
                github_user = get_or_create_github_user_from_token(github_token)

        if github_user is None:
            raise exceptions.AuthenticationFailed('No such user')

        return github_user.user, None
