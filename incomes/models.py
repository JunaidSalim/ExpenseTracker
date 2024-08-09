from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey(to=Source,on_delete=models.CASCADE)

    def __str__(self):
        return self.source.name
    
    class Meta:
        ordering : ['-date']


