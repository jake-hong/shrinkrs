# Generated by Django 3.2 on 2021-12-02 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='url_count',
            field=models.IntegerField(default=0),
        ),
    ]
