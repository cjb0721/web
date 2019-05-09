# Generated by Django 2.2 on 2019-05-02 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=40)),
                ('url', models.CharField(max_length=100)),
                ('idc', models.CharField(max_length=3)),
                ('alarm_type', models.CharField(max_length=8)),
                ('alarm_info', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Monitor_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns_lookup_time', models.FloatField()),
                ('connect_time', models.FloatField()),
                ('pre_transfer_time', models.FloatField()),
                ('start_transfer_time', models.FloatField()),
                ('total_time', models.FloatField()),
                ('http_status', models.CharField(max_length=100)),
                ('size_download', models.FloatField()),
                ('size_header', models.SmallIntegerField()),
                ('size_request', models.SmallIntegerField()),
                ('download_length', models.FloatField()),
                ('download_speed', models.FloatField()),
                ('datetime', models.DateTimeField(auto_now_add=True, max_length=12)),
                ('mark', models.CharField(max_length=1)),
                ('fid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Host_info')),
            ],
        ),
    ]
