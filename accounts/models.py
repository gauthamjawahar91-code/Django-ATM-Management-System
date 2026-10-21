from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField()
    account_no = models.BigIntegerField(unique=True)
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    pin = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name