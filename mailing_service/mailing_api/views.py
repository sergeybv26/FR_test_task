from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing_api.models import Client, Mailing
from mailing_api.serializers import ClientSerializer, MailingSerializer, MessageSerializer


class ClientView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class SingleClientView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingView(ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class SingleMailingView(RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MessageFromMailingStat(APIView):
    def get(self, request, pk=None):
        mailing = get_object_or_404(Mailing, pk=pk)
        serializer = MessageSerializer(mailing.get_messages(), many=True)
        return Response({'messages': serializer.data})
