# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JanrainUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=512)),
                ('provider', models.CharField(max_length=64)),
                ('identifier', models.URLField(max_length=512)),
                ('avatar', models.URLField(max_length=512, blank=True)),
                ('url', models.URLField(max_length=512, blank=True)),
                ('user', models.ForeignKey(related_name='janrain_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
