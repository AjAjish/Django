# Generated by Django 5.2.4 on 2025-07-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_formdata_address_alter_formdata_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdata',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='formdata',
            name='role',
            field=models.CharField(default='user', max_length=50),
        ),
    ]
