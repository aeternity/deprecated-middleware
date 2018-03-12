# Create your views here.
import sys

from django.http import JsonResponse
from django.utils import cache
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from aeternity import AEName
from aeternity.exceptions import AException
from epoch_extra import get_client, get_key_pair
from epoch_extra.models import AeName
from faucet.models import FaucetTransaction

sys.path.append('/code/src/aeternity')
sys.path.append('/code/src/')

redis = cache.caches['default']


class FaucetView(GenericViewSet):

    permission_classes = (IsAuthenticated, )

    def create(self, request, **kwargs):
        pub_key = request.data.get('key')
        amount = request.data.get('amount', 100)

        with redis.lock(f'get_faucet_{pub_key}', timeout=5):

            free_coins = FaucetTransaction.receivable_tokens(pub_key)
            actual_coins = min(amount, free_coins)

            response_data = {}

            if actual_coins > 0:
                client = get_client()
                try:
                    # check balance
                    balance = client.get_balance()
                    if balance < actual_coins:
                        raise ParseError('Faucet is out of cash')
                except AException:
                    raise ParseError('Faucet has no account')

                key_pair = get_key_pair()
                try:
                    tx_hash = client.spend(pub_key, int(actual_coins), key_pair)
                    response_data['tx_hash'] = tx_hash
                except AException:
                    raise ParseError(f'Spend TX failed')

                response_data['spent'] = actual_coins

                user = request.user
                aet_name = f'{user.username}.aet'
                try:
                    ae_name = AeName.objects.get(user=user, name=aet_name)
                except AeName.DoesNotExist:
                    ae_name = AeName.objects.create(
                        user=user,
                        pub_key=pub_key,
                        name=aet_name
                    )

                if AEName(aet_name, client=client).is_available():
                    # Another task will pick up from here later
                    # see tasks.claim_unclaimed_names()
                    ae_name.preclaim()

                FaucetTransaction.objects.create(
                    public_key=pub_key,
                    amount=actual_coins
                )
            elif amount > 0:
                raise ParseError('Your hourly/daily rate has been reached')

        if not response_data:
            response_data['error'] = 'No token available'

        return JsonResponse(response_data)
