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

            free_tokens = FaucetTransaction.receivable_tokens(pub_key)
            actual_tokens = min(amount, free_tokens)

            if actual_tokens > 0:
                config = Config(
                    external_host='epoch:3013',
                    internal_host='epoch:3113',
                    websocket_host='epoch:3114'
                )
                client = EpochClient(configs=config)  # connect with the Epoch node

                key_pair = KeyPair.read_from_dir(settings.EPOCH_KEYS, 'secret')
                try:
                    # check balance
                    balance = client.get_balance()
                    if balance < actual_tokens:
                        raise ParseError('Faucet is out of cash')
                except AException:
                    raise ParseError('Faucet has no account')

                try:

                    tx = client.create_transaction(pub_key, int(actual_tokens))
                    signed_tx = key_pair.sign_transaction(tx)
                    client.send_signed_transaction(signed_tx)
                except AException:
                    raise ParseError(f'Spend TX failed Amount {actual_tokens}')

                FaucetTransaction.objects.create(
                    public_key=pub_key,
                    amount=actual_tokens
                )
            elif amount > 0:
                raise ParseError('Your hourly/daily rate has been reached')

        return JsonResponse({'spent': actual_tokens})