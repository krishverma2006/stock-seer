from django.db import models

# Create your models here.
class  StockData(models.Model):
    company_name=models.CharField(max_length=90)
    Open_Year=models.IntegerField()
    Last_Year=models.IntegerField()
    High_Profit=models.IntegerField()
    Low_Profit=models.IntegerField()
    Trade_Amt=models.IntegerField()