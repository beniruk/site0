# Generated by Django 3.0.4 on 2020-03-28 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20200328_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='destination',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='flights',
            name='origin',
            field=models.CharField(max_length=64),
        ),
        migrations.DeleteModel(
            name='airport',
        ),
    ]
