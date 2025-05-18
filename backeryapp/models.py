from django.db import models
from django.contrib.auth.models import User
# Create your models here.


from django.db import models

class Prebooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    requests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


class MyCustomUser(User):
    phone_number = models.CharField(max_length=15)  
    address = models.CharField(max_length = 300, null = True)
    postcode = models.CharField(max_length = 100, null = True)
    near_by = models.CharField(max_length = 100, null = True)
    user_type =  models.CharField(max_length=20)  
    number_pare = models.IntegerField()
    def __str__(self):
        return self.username
    

class Bakery_category(models.Model):
    img =  models.FileField(upload_to='category')
    category = models.CharField(max_length = 100)

class Bakery_recipe(models.Model):
    category = models.CharField(max_length=100)
    img1 = models.FileField(upload_to='product_images')
    name = models.CharField(max_length=60)
    price = models.CharField(max_length=20)
    price_in_market = models.CharField(max_length=20,null = True,default=True)
    weight = models.CharField(max_length=100)
    inches = models.CharField(max_length=100)


class add_cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=15)  
    number = models.IntegerField() 
    order_status = models.CharField(max_length=35)  
    qyt = models.CharField(max_length=35)  
    

class user_comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comp = models.CharField(max_length=300)

class review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_of_stars = models.IntegerField()
    comments = models.CharField(max_length=300)

class offer(models.Model):
    of = models.CharField(max_length=200)

class our_signature_banner(models.Model):
    img =  models.FileField(upload_to='our_signature_creations')
    

class our_products_data(models.Model):
    img =  models.FileField(upload_to='our_products_data')
    name = models.CharField(max_length=60)