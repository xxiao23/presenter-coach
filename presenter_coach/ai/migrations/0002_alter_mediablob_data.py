# Generated by Django 3.2.4 on 2021-07-14 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediablob',
            name='data',
            field=models.CharField(max_length=1048576),
        ),
    ]
