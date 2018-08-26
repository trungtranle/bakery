from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to = 'img')

    def __str__(self):
        return self.name

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 100)
    

    picture = models.ImageField(upload_to = 'img')

    def __str__(self):
        return self.user.username