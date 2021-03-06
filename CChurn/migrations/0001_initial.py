# Generated by Django 2.2.5 on 2021-06-27 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormDataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.FileField(blank=True, null=True, upload_to='')),
                ('DateImputed', models.DateTimeField(blank=True, null=True)),
                ('UserID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.UserTable')),
            ],
        ),
    ]
