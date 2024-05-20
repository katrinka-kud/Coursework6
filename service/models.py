from datetime import datetime

from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='почта')
    comment = models.CharField(max_length=200, verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f'Клиент: {self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingSetup(models.Model):
    EVERY_DAY = 'раз в день'
    EVERY_WEEK = 'раз в неделю'
    EVERY_MONTH = 'раз в месяц'

    PERIODICITY = (
        (EVERY_DAY, 'раз в день'),
        (EVERY_WEEK, 'раз в неделю'),
        (EVERY_MONTH, 'раз в месяц'),
    )

    STATUS_CREATE = 'создана'
    STATUS_START = 'запущена'
    STATUS_DONE = 'завершена'

    STATUSES = (
        (STATUS_CREATE, 'создана'),
        (STATUS_START, 'запущена'),
        (STATUS_DONE, 'завершена')
    )

    data_begin = models.DateTimeField(default=datetime.now, verbose_name='дата начала рассылки')
    data_end = models.DateTimeField(default=datetime.now, verbose_name='дата конца рассылки')
    period = models.CharField(max_length=20, default='EVERY_DAY', choices=PERIODICITY, verbose_name='периодичность')
    status = models.CharField(max_length=20, default='STATUS_CREATE', choices=STATUSES, verbose_name='статус рассылки')

    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    is_active = models.BooleanField(default=False, verbose_name='активна')

    def __str__(self):
        return f'''Владелец: {self.owner}\n
                   \rДата: {self.data_begin}-{self.data_end}\n
                   \rПериодичность: {self.period}\n
                   \rСтатус: {self.status}
                '''

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылки'
        permissions = [('can_disable_mailing', 'Может отключать рассылку'),]


class Messages(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    mailing_list = models.ForeignKey(MailingSetup, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f'{self.owner} {self.subject}'


class Logs(models.Model):
    data_send = models.DateTimeField(default=datetime.now, verbose_name='дата')
    is_done = models.BooleanField(default=True, verbose_name='статус')
    error_massage = models.CharField(max_length=150, verbose_name='ошибка', **NULLABLE)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    send_list = models.ForeignKey(MailingSetup, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'журнал рассылки'
        verbose_name_plural = 'журналы рассылок'

    def __str__(self):
        return f'{self.is_done} {self.client} {self.data_send}'
