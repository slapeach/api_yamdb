# Generated by Django 2.2.16 on 2022-04-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220418_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.TextField(),
        ),
    ]
