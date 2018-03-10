from aeternity.aens import NameStatus, AEName
from celery import shared_task
from django.conf import settings

from aeternity import EpochClient, Config
from epoch_extra.models import AeName

epoch_host = settings.EPOCH_HOST
config = Config(
    external_host=f'{epoch_host}:3013',
    internal_host=f'{epoch_host}:3113',
    websocket_host=f'{epoch_host}:3114'
)

# connect with the Epoch node
client = EpochClient(configs=config)


@shared_task
def claim_unclaimed_names():

    # ae_name_obj = AEName(name, client=client)

    for name in AeName.objects.filter(status=NameStatus.PRECLAIMED):

        response = client.get_transaction_by_transaction_hash(name.preclaim_tx)
        if response.status_code == 200:
            response_data = response.json()
            block_height = response_data['block_height']
            if block_height == -1:
                ae_name = AEName(name, client=client)
                ae_name.preclaim_salt = name.claim_salt
                claim_tx = ae_name.claim()
                name.claim_tx = claim_tx
                name.status = NameStatus.CLAIMED
                name.save(update_fields=['status, claim_tx'])
