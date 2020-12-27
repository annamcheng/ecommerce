from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Inherit models from Model for Customer class
# User can only have one Customer
# Customer can only have one User
class Customer(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)

  # String Constructor passing in self as an argument
  def __str__(self):
    return self.name