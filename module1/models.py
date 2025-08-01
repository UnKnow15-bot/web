from django.db import models
from django.utils.text import slugify

class User(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(null=False, unique=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()


class Task(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Category(models.Model):
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    is_avail = models.BooleanField(default=True)
    image = models.ImageField(upload_to ='images/')
    file = models.FileField(upload_to='files/')

    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    user = models.ManyToManyField(User, related_name='courses', blank=True, null=True)

    def __str__(self):
        return self.name
    

 
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name



class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

 

# IntegerField
# CharField
# FloatField
# DateField
# DateTimeField
# EmailField
# BooleanField
# FileField
# ImageField
 
# Assuming these already exist
# class User(models.Model): ...
# class Course(models.Model): ...

from django.db import models

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    grandtotal = models.FloatField(default=0)

    def __str__(self):
        return f"Cart of {self.user.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.course.name} x {self.quantity}"
