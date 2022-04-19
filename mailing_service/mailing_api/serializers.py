import re

from rest_framework import serializers

from mailing_api.models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def validate_phone_number(self, value):
        """Валидация номера телефона"""
        if not re.fullmatch(r'^7\d{10}$', str(value)):
            raise serializers.ValidationError('Номер телефона должен иметь вид: 7ХХХХХХХХХХ, где Х - число от 0 до 9')
        return value


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
