# Create your views here.
import sys
from django.utils import cache
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.viewsets import GenericViewSet
from aeternity import Config, EpochClient
from aeternity.exceptions import AException
from faucet.models import FaucetTransaction

sys.path.append('/code/src/aeternity')
sys.path.append('/code/src/')

redis = cache.caches['default']


class FaucetView(GenericViewSet):

    def create(self, request, **kwargs):
        pub_key = kwargs.get('key')
        amount = kwargs.get('amount', 100)

        with redis.lock(f'get_faucet_{pub_key}', expire=120):

            free_tokens = FaucetTransaction.receivable_tokens(pub_key)
            actual_tokens = min(amount, free_tokens)

            config = Config(
                external_host='epoch:3013',
                internal_host='epoch:3113',
                websocket_host='epoch:3114'
            )
            client = EpochClient(configs=config)  # connect with the Epoch node
            try:
                # check balance
                balance = client.get_balance()
                if balance < actual_tokens:
                    raise ParseError('Faucet is out of cash')

                client.spend(pub_key, actual_tokens)
            except AException:
                raise ParseError('Faucet has no account')

            FaucetTransaction.objects.create(
                public_key=pub_key,
                amount=actual_tokens
            )
