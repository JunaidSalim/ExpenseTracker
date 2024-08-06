from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name
    
    class Meta:
        ordering : ['-date']


