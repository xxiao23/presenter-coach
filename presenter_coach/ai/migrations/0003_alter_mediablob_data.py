# Generated by Django 3.2.4 on 2021-07-14 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0002_alter_mediablob_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediablob',
            name='data',
            field=models.BinaryField(max_length=1048576),
        ),
    ]
