# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-19 08:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20191130_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='Department',
            field=models.CharField(choices=[('CSE', 'CSE'), ('MECH', 'MECH'), ('Civil', 'Civil'), ('ENC', 'ENC'), ('ISE', 'ISE')], default='CSE', max_length=10),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='Designation',
            field=models.CharField(blank=True, choices=[('Principal', 'Principal'), ('Prof.', 'Professor'), ('HOD', 'HOD'), ('Asst.Prof.', 'Asst.Professor'), ('Asst.Prof.', 'Asso.Professor')], max_length=20),
        ),
        migrations.AlterField(
            model_name='reqdetails',
            name='dateof_request',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='students',
            name='Department',
            field=models.CharField(blank=True, choices=[('CSE', 'CSE'), ('MECH', 'MECH'), ('Civil', 'Civil'), ('ENC', 'ENC'), ('ISE', 'ISE')], max_length=10),
        ),
    ]
