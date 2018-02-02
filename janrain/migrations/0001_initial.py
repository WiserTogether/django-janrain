from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL)
    ]

    operations = [
        migrations.CreateModel(
            name='JanrainUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=512)),
                ('provider', models.CharField(max_length=64)),
                ('identifier', models.URLField(max_length=512)),
                ('avatar', models.URLField(blank=True, max_length=512)),
                ('url', models.URLField(blank=True, max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='janrain_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
    
