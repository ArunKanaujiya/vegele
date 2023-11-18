from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
class Receipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    receipe_name=models.CharField(max_length=100)
    receipe_description=models.TextField(max_length=1000)
    receipe_image=models.FileField()
    receipe_slug=AutoSlugField(populate_from='receipe_name',unique=True,null=True,default=None)
    receipe_amount=models.IntegerField(default=200)

    def __str__(self):
        return self.receipe_name

class amount(models.Model):
    receipe_amount=models.IntegerField()