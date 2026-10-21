from django.db import models
from accounts.models import Account

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
    ("DEPOSIT", "Deposit"),
    ("WITHDRAW", "Withdraw"),
    ("TRANSFER_SENT", "Transfer Sent"),
    ("TRANSFER_RECEIVED", "Transfer Received"),
    ]
    account = models.ForeignKey(Account,on_delete=models.CASCADE ,  related_name="transactions")
    transaction_type = models.CharField( max_length=50 , choices= TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12 , decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12,decimal_places=2)
    description = models.CharField(max_length=255 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_no} - {self.transaction_type} - ₹{self.amount}"