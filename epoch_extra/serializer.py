from rest_framework import serializers

from epoch_extra.models import AeName


class AensSerializer(serializers.ModelSerializer):

    pointers = serializers.SerializerMethodField()

    class Meta:
        model = AeName
        fields = (
            'pub_key',
            'name',
            'status',
            'preclaim_tx',
            'claim_tx',
            'pointers'
        )

    def get_pointers(self):
        return [pointer[1] for pointer in self.pointers]
