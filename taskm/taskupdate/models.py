from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class Products(models.Model):
    pid = models.CharField(primary_key=True, default="P"+uuid.uuid4().hex[:5].upper(), max_length=6, editable=False)
    name = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Product_Detail'
        verbose_name_plural = 'Product_Details'

class Order(models.Model):
    oid = models.CharField(primary_key=True, default="O"+uuid.uuid4().hex[:7].upper(), max_length=8, editable=False)
    detail = models.CharField(max_length=2000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='self')
    ordered_date = models.DateTimeField(default=timezone.now, editable=False)
    total = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Order_Detail'
        verbose_name_plural = 'Order_Details'