import pytz
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mailing(models.Model):
    """Модель Рассылка"""
    start_time = models.DateTimeField(verbose_name='дата и время старта рассылки')
    message = models.TextField(verbose_name='Текст сообщения')
    filter_params = models.CharField(max_length=64, verbose_name='фильтр свойств клиентов')
    end_time = models.DateTimeField(verbose_name='дата и время окончания рассылки')

    class Meta:
        ordering = ('start_time',)
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def get_messages(self):
        """Получает все сообщения по рассылке"""
        return self.mailingmessage.select_related()


class Client(models.Model):
    """Модель Клиент"""
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.IntegerField(unique=True, verbose_name='Номер телефона')
    operator_code = models.IntegerField(db_index=True, verbose_name='Код оператора')
    tag = models.CharField(max_length=64, db_index=True, verbose_name='Тег(метка)')
    timezone = models.CharField(max_length=64, choices=TIMEZONES, default='Europe/Moscow', verbose_name='Часовой пояс')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Модель Сообщение"""
    STATUS_FORMING = 'FM'
    STATUS_PROCESSED = 'PD'
    STATUS_DELAYED = 'DL'
    STATUS_COMPLETED = 'CP'
    STATUS_REPEATED = 'RP'
    STATUS_ERROR = 'ERR'

    STATUSES = (
        (STATUS_FORMING, 'Сформировано'),
        (STATUS_PROCESSED, 'Отправляется'),
        (STATUS_DELAYED, 'Отложено'),
        (STATUS_COMPLETED, 'Отправлено'),
        (STATUS_REPEATED, 'Повтор отправки'),
        (STATUS_ERROR, 'Ошибка отправки')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    sending_status = models.CharField(verbose_name='статус', max_length=3, choices=STATUSES, default=STATUS_FORMING)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailingmessage')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


@receiver(post_save, sender=Mailing)
def create_message(sender, instance, created, **kwargs):
    if created:
        filter_client = instance.filter_params
        clients = Client.objects.filter(Q(operator_code=filter_client) | Q(tag=filter_client))
        objs = []
        for client in clients:
            msg = Message(mailing_id=instance, client_id=client)
            objs.append(msg)
        Message.objects.bulk_create(objs)
