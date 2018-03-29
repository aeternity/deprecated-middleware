from django.conf import settings

from aeternity import Config, EpochClient
from aeternity.signing import KeyPair


def get_client():
    epoch_host = settings.EPOCH_HOST
    config = Config(
        external_host=f'{epoch_host}:3013',
        internal_host=f'{epoch_host}:3113',
        websocket_host=f'{epoch_host}:3114'
    )
    # connect with the Epoch node
    return EpochClient(configs=config)


def get_key_pair():
    return KeyPair.read_from_dir(
        settings.EPOCH_KEYS,
        settings.EPOCH_PASSWORD
    )
