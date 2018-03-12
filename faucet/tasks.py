from aeternity.aens import NameStatus, AEName
from celery import shared_task
from epoch_extra import client, key_pair

from epoch_extra.models import AeName


@shared_task
def claim_unclaimed_names():

    # ae_name_obj = AEName(name, client=client)

    for name in AeName.objects.filter(status=NameStatus.PRECLAIMED):

        if name.preclaim_tx:
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
        else:
            aen = AEName(name, client=client)
            aen.update_status()
            if aen.status == NameStatus.AVAILABLE:
                name.preclaim()

    for name in AeName.objects.filter(status=NameStatus.CLAIMED):
        response = client.get_transaction_by_transaction_hash(name.claim_tx)

        if response.status_code == 200:
            response_data = response.json()
            block_height = response_data['block_height']
            if block_height == -1:
                ae_name = AEName(name, client=client)
                ae_name.update_status()
                next(pointer
                     for pointer in ae_name.pointers
                     if pointer[1] == name.pub_key)
