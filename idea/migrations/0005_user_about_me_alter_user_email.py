# Generated by Django 4.2 on 2024-08-28 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0004_remove_idea_slug_comment_time_update_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
