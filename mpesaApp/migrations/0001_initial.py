# Generated by Django 3.2 on 2021-04-15 20:08

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
            name='MpesaPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('MerchantRequestID', models.CharField(blank=True, max_length=100, null=True)),
                ('CheckoutRequestID', models.CharField(blank=True, max_length=100, null=True)),
                ('Amount', models.CharField(blank=True, max_length=100, null=True)),
                ('MpesaReceiptNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('TransactionDate', models.CharField(blank=True, max_length=100, null=True)),
                ('PhoneNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('Status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
