from django.db import models

# Create your models here.
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class LedState(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  is_on = models.BooleanField(default=False)


  def __str__(self):
    return self.name