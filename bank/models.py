from django.db import models
from django.core.exceptions import ValidationError
import random
import string
from django.contrib.auth.models import User
from hashlib import sha256


class Bank(models.Model):
    fullname = models.CharField(max_length=100)
    account_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=256)
    amount = models.FloatField(default=0.0)
    nagrita_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def generate_unique_account_no(self):
        while True:
            # Generate a random 8-digit account number
            account_number = ''.join(random.choices(string.digits, k=8))
            if not Bank.objects.filter(account_number=account_number).exists():
                return account_number



    def save(self, *args, **kwargs):


        # Name to lowercase
        self.fullname = self.fullname.lower()

        # Generate account number if not provided
        if not self.account_number:
            self.account_number = self.generate_unique_account_no()

        # Phone number validation
        if not self.phone.isdigit():
            raise ValidationError('Phone number must be a number')
        

        # Amount validation
        try:
            float(self.amount)
        except ValueError:
            raise ValidationError('Amount must be a number')

        return super(Bank, self).save(*args, **kwargs)

    def __str__(self):
        return self.fullname + ' - ' + self.phone + ' - ' + str(self.amount) + ' - ' + self.account_number



