from rest_framework import serializers

from epoch_extra.models import AeName


class AensSerializer(serializers.ModelSerializer):

    class Meta:
        model = AeName
        fields = (
            'pub_key'
            'name'
            'status',
        )
