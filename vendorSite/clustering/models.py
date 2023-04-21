from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomerBill(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=14, blank=False)
    spendingScore = models.IntegerField()
    annualIncome = models.IntegerField()

    def __str__(self):
        return self.phoneNumber
