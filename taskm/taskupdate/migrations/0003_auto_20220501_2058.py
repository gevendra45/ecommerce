# Generated by Django 2.2 on 2022-05-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskupdate', '0002_auto_20220501_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.CharField(default='OC7DBE62', editable=False, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='pid',
            field=models.CharField(default='PAFF9E', editable=False, max_length=6, primary_key=True, serialize=False),
        ),
    ]
