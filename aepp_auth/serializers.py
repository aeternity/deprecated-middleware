from rest_framework import serializers


class OAuthSerializer(serializers.Serializer):

    state = serializers.CharField()
    redirect_uri = serializers.CharField()
    code = serializers.CharField()