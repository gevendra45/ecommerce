# Generated by Django 2.2 on 2022-05-01 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('pid', models.CharField(default='P8CA9D', editable=False, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Product_Detail',
                'verbose_name_plural': 'Product_Details',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('oid', models.CharField(default='O5AFE15F', editable=False, max_length=8, primary_key=True, serialize=False)),
                ('detail', models.CharField(blank=True, max_length=2000, null=True)),
                ('ordered_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('total', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='self', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order_Detail',
                'verbose_name_plural': 'Order_Details',
            },
        ),
    ]