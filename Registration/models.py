from django.db import models
from django.contrib.auth.models import User

class register(models.Model):
    address=models.CharField(max_length=100)
    contact=models.CharField(max_length=100,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class department(models.Model):
    department=models.CharField(max_length=100)   

    
class foods(models.Model):
    fooditem=models.CharField(max_length=100)
    image=models.ImageField(upload_to='foodimage')
    dept=models.ForeignKey(department,on_delete=models.CASCADE)