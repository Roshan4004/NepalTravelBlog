# Generated by Django 4.0.3 on 2023-02-19 10:07

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_quill.fields.QuillField(),
        ),
    ]