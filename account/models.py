from django.db import models
from django.contrib.auth.models import User
from . constant import ACCCOUNT_TYPE,GENDER
# Create your models here.



class UserAccount(models.Model):
    user=models.OneToOneField(User,related_name='useraccount', on_delete=models.CASCADE)
    blance=models.DecimalField( max_digits=12, decimal_places=2,default=0.00)
    account_type=models.CharField(max_length=50,choices=ACCCOUNT_TYPE)
    gender=models.CharField(max_length=50,choices=GENDER)
    create_date=models.DateField( auto_now=True,)
    birth_date=models.DateField()
    
    def __str__(self) -> str:
        return self.user.username

class UserAddress(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    postal_code=models.IntegerField()
    streat=models.CharField( max_length=50)
    city=models.CharField( max_length=50)
    country=models.CharField( max_length=50,blank=True ,null=True)


    def __str__(self) -> str:
        return self.user.username