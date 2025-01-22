from typing import Any
from django.db import models
from account.models import UserAccount
from .constant import TRANSACTIONS_TYPE
# Create your models here.


class UserTransactions(models.Model):
    account=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    after_transaction=models.DecimalField(decimal_places=2,max_digits=12)
    transaction_type=models.IntegerField(choices=TRANSACTIONS_TYPE)
    transactions_date=models.DateField(auto_now=True)
    loan_status=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.transaction_type)
    
        
