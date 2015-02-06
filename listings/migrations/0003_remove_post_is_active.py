# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_picture_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_active',
        ),
    ]
