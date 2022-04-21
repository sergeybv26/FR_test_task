from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing_api.models import Client, Mailing, Message
from mailing_api.serializers import ClientSerializer, MailingSerializer, MessageSerializer, MailingStatSerializer, \
    MessageStatSerializer


class ClientView(ListCreateAPIView):
    """Получения всех клиентов и создание нового клиента"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class SingleClientView(RetrieveUpdateDestroyAPIView):
    """Получение клиента, изменение данных, удаление клиента"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingView(ListCreateAPIView):
    """Получение всех рассылок и создание новой рассылки"""
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class SingleMailingView(RetrieveUpdateDestroyAPIView):
    """Редактирование и удаление рассылки"""
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MessageFromMailingStat(APIView):
    """Получение статистики по рассылке"""
    def get(self, request, pk=None):
        mailing = get_object_or_404(Mailing, pk=pk)
        messages = mailing.get_messages()
        serializer = MessageStatSerializer(messages, many=True)
        return Response({'messages': serializer.data})


class MessageAndMailingStat(ListCreateAPIView):
    """Получение статистики по всем рассылкам"""
    queryset = Mailing.objects.all()
    serializer_class = MailingStatSerializer


class SingleMessageView(RetrieveUpdateAPIView):
    """Получение и изменение сообщения со всеми параметрами"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageView(ListAPIView):
    """Получение всех сообщений"""
    queryset = Message.objects.filter(~Q(sending_status='CP') & ~Q(sending_status='ERR'))
    serializer_class = MessageSerializer
