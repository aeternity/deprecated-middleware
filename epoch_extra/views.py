
# Create your views here.
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.exceptions import ParseError, APIException, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet, ModelViewSet

from epoch_extra.models import AeName
from epoch_extra.serializer import AensSerializer


class BalanceView(ViewSet):

    permission_classes = (AllowAny, )

    def retrieve(self, request, pk=None):
        if pk is None:
            raise ParseError('Account key is not set')
        url = f'http://{settings.EPOCH_HOST}:3113/v2/account/balance/{pk}'
        response = requests.get(url)
        if response.status_code >= 500:
            raise APIException(
                detail=f'Response {response.status_code} {response.text}',
                code=response.status_code)
        elif response.status_code == 404:
            raise NotFound(f'{response.json()["reason"]}')
        json = response.json()

        return JsonResponse(json)


class AensViewSet(ModelViewSet):

    serializer_class = AensSerializer
    queryset = AeName.objects.all()

    def retrieve(self, request, pk=None):
        name = self.get_object()
        serializer = self.get_serializer(name)
        return JsonResponse(data=serializer.data)
