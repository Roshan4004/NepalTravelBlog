# Generated by Django 4.0.3 on 2023-02-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_likes_alter_post_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='exact_place',
            new_name='local_body',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='place',
            new_name='local_name',
        ),
        migrations.AlterField(
            model_name='post',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]