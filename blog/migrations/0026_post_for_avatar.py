# Generated by Django 4.2.2 on 2025-01-04 08:57

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='for_avatar',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
