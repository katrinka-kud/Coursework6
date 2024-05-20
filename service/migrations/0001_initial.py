# Generated by Django 5.0.4 on 2024-05-05 13:50

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100, verbose_name='фамилия')),
                ('first_name', models.CharField(max_length=100, verbose_name='имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='комментарий')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='MailingSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_begin', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата начала рассылки')),
                ('data_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата конца рассылки')),
                ('period', models.CharField(max_length=10, verbose_name='периодичность')),
                ('status', models.CharField(max_length=10, verbose_name='статус рассылки')),
                ('is_active', models.BooleanField(default=False, verbose_name='активна')),
                ('clients', models.ManyToManyField(to='service.client', verbose_name='клиенты')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'настройка рассылки',
                'verbose_name_plural': 'настройки рассылки',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_send', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата')),
                ('is_done', models.BooleanField(default=True, verbose_name='статус')),
                ('error_massage', models.CharField(blank=True, max_length=150, null=True, verbose_name='ошибка')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.client', verbose_name='клиент')),
                ('send_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.mailingsetup', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'журнал рассылки',
                'verbose_name_plural': 'журналы рассылок',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('mailing_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.mailingsetup', verbose_name='рассылка')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
    ]
