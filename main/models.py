from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="targetslist", null=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
        
class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    pid = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.text