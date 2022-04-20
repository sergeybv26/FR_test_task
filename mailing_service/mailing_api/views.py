from django.db.models import Count
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing_api.models import Client, Mailing, Message
from mailing_api.serializers import ClientSerializer, MailingSerializer, MessageSerializer, MailingStatSerializer, \
    MessageStatSerializer


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
        messages = mailing.get_messages()
        serializer = MessageStatSerializer(messages, many=True)
        return Response({'messages': serializer.data})


class MessageAndMailingStat(ListCreateAPIView):
    queryset = Mailing.objects.all()
    print(queryset)
    serializer_class = MailingStatSerializer


class SingleMessageView(RetrieveUpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
