# Generated by Django 4.0.1 on 2022-03-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_initial'),
        ('users', '0003_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='locations',
            field=models.ManyToManyField(blank=True, null=True, to='ads.Location'),
        ),
    ]