# Generated by Django 4.1.2 on 2022-10-30 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_keyword', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RegionInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=100)),
                ('region_interest', models.IntegerField()),
                ('region_geo_code', models.CharField(default=None, max_length=10)),
                ('search_keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.searchkey')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_interest', models.IntegerField()),
                ('time_stamp', models.DateTimeField()),
                ('search_keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.searchkey')),
            ],
        ),
    ]
