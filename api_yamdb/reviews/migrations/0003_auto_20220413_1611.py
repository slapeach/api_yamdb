# Generated by Django 2.2.16 on 2022-04-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220412_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, through='reviews.TitleGenre', to='reviews.Genre'),
        ),
    ]
