# Create your views here.
import sys

from django.conf import settings
from django.http import JsonResponse
from django.utils import cache
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.viewsets import GenericViewSet
from aeternity import Config, EpochClient
from aeternity.exceptions import AException
from faucet.models import FaucetTransaction
from aeternity.signing import KeyPair

sys.path.append('/code/src/aeternity')
sys.path.append('/code/src/')

redis = cache.caches['default']


class FaucetView(GenericViewSet):

    def create(self, request, **kwargs):
        pub_key = request.data.get('key')
        amount = request.data.get('amount', 100)

        with redis.lock(f'get_faucet_{pub_key}', timeout=5):

            free_coins = FaucetTransaction.receivable_tokens(pub_key)
            actual_coins = min(amount, free_coins)

            if actual_coins > 0:
                epoch_host = settings.EPOCH_HOST
                config = Config(
                    external_host=f'{epoch_host}:3013',
                    internal_host=f'{epoch_host}:3113',
                    websocket_host=f'{epoch_host}:3114'
                )

                # connect with the Epoch node
                client = EpochClient(configs=config)

                key_pair = KeyPair.read_from_dir(
                    settings.EPOCH_KEYS,
                    settings.EPOCH_PASSWORD
                )
                try:
                    # check balance
                    balance = client.get_balance()
                    if balance < actual_coins:
                        raise ParseError('Faucet is out of cash')
                except AException:
                    raise ParseError('Faucet has no account')

                try:
                    client.spend(pub_key, int(actual_coins), key_pair)
                except AException:
                    raise ParseError(f'Spend TX failed Amount {actual_coins}')

                FaucetTransaction.objects.create(
                    public_key=pub_key,
                    amount=actual_coins
                )
            elif amount > 0:
                raise ParseError('Your hourly/daily rate has been reached')

        return JsonResponse({'spent': actual_coins})