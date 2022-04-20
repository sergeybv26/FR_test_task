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


class MessageStatSerializer(serializers.ModelSerializer):
    sending_status = serializers.CharField(read_only=True)
    msq_quantity = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['sending_status', 'msq_quantity']


class MailingStatSerializer(serializers.ModelSerializer):
    msg_stat = serializers.SerializerMethodField()
    message = serializers.CharField(read_only=True)

    class Meta:
        model = Mailing
        fields = ['id', 'message', 'msg_stat']

    def get_msg_stat(self, obj):
        return obj.get_messages()


class MessageSerializer(serializers.ModelSerializer):
    client_phone = serializers.ReadOnlyField(source='client_id.phone_number')
    client_tz = serializers.ReadOnlyField(source='client_id.timezone')
    mail_start = serializers.ReadOnlyField(source='mailing_id.start_time')
    mail_end = serializers.ReadOnlyField(source='mailing_id.end_time')
    message = serializers.ReadOnlyField(source='mailing_id.message')

    class Meta:
        model = Message
        fields = ['id', 'sending_status', 'client_phone', 'client_tz', 'mail_start', 'mail_end', 'message']
