# Generated by Django 4.2.10 on 2024-02-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
