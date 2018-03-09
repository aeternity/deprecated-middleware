from aeternity.aens import NameStatus, AEName
from celery import shared_task
from epoch_extra import get_client, get_key_pair

from epoch_extra.models import AeName


@shared_task
def claim_unclaimed_names():
    client = get_client()
    for ae_name_obj in AeName.objects.filter(status=NameStatus.PRECLAIMED):

        if ae_name_obj.preclaim_tx:
            response = client.get_transaction_by_transaction_hash(ae_name_obj.preclaim_tx)

            if response.status_code == 200:
                response_data = response.json()
                block_height = response_data['block_height']
                if block_height == -1:
                    ae_name = AEName(ae_name_obj, client=client)
                    ae_name.preclaim_salt = ae_name_obj.claim_salt
                    claim_tx = ae_name_obj.claim()
                    ae_name_obj.claim_tx = claim_tx
                    ae_name_obj.status = NameStatus.CLAIMED
                    ae_name_obj.save(update_fields=['status, claim_tx'])
        else:
            aen = AEName(ae_name_obj.name, client=client)
            aen.update_status()
            if aen.status == NameStatus.AVAILABLE:
                ae_name_obj.preclaim()

    for ae_name_obj in AeName.objects.filter(status=NameStatus.CLAIMED):
        response = client.get_transaction_by_transaction_hash(ae_name_obj.claim_tx)

        if response.status_code == 200:
            response_data = response.json()
            block_height = response_data['block_height']
            if block_height == -1:
                ae_name_obj = AEName(ae_name_obj, client=client)
                ae_name_obj.update_status()
                next(pointer
                     for pointer in ae_name_obj.pointers
                     if pointer[1] == ae_name_obj.pub_key)
