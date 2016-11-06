# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-03 19:35
from __future__ import unicode_literals

from django.db import migrations
from Instanssi.common.misc import parse_youtube_video_id


def forwards(apps, schema_editor):
    OtherVideo = apps.get_model("arkisto", "OtherVideo")
    for video in OtherVideo.objects.all():
        video_id = parse_youtube_video_id(video.youtube_url)
        if video_id:
            video.youtube_url = u'https://www.youtube.com/v/{}'.format(video_id)
            video.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('arkisto', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
