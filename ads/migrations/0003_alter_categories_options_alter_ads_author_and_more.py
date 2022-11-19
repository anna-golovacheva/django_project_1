# Generated by Django 4.1.3 on 2022-11-17 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_locations_alter_ads_options_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='ads',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ads.users'),
        ),
        migrations.AlterField(
            model_name='ads',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ads.categories'),
        ),
        migrations.AlterField(
            model_name='users',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='locations',
            field=models.ManyToManyField(blank=True, null=True, to='ads.locations'),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
