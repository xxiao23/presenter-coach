# Generated by Django 3.2.4 on 2021-07-15 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0006_alter_mediablob_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediablob',
            name='data',
            field=models.BinaryField(default=None, max_length=1038336),
        ),
    ]
