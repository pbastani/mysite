# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('post_id', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('file', sorl.thumbnail.fields.ImageField(upload_to='listing_images/%Y/%m/%d', default='')),
                ('title', models.CharField(max_length=50, default='')),
                ('upload_date', models.DateField(verbose_name='Uploaded On')),
                ('position', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200, default='')),
                ('content', models.CharField(max_length=10000, default='')),
                ('create_date', models.DateTimeField(default=datetime.date(2000, 1, 1))),
                ('expiry_date', models.DateTimeField(default=datetime.date(2000, 1, 1))),
                ('is_active', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=50, default='')),
                ('price', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[(None, 'Select a category'), ('general', 'General'), ('forsale', 'For Sale'), ('services', 'Services'), ('housing', 'Housing')], max_length=2, default='general')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('last_online', models.DateTimeField(default=datetime.date(2000, 1, 1))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(max_length=50, verbose_name='Tag', default='')),
                ('posts', models.ManyToManyField(to='listings.Post', related_name='tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='picture',
            name='post',
            field=models.ForeignKey(to='listings.Post', related_name='pictures'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorite',
            name='profile',
            field=models.ForeignKey(to='listings.Profile', related_name='favorites'),
            preserve_default=True,
        ),
    ]
