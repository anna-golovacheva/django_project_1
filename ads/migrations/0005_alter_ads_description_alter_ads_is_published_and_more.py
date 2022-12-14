# Generated by Django 4.1.3 on 2022-11-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_ads_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ads',
            name='is_published',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ads',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ads',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
