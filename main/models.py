from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

# Create your models here.
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    vendor = models.CharField(max_length=200) 
    description= models.CharField(max_length=300, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payback = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    due = models.DateTimeField()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paybacks')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    