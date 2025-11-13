from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def subtotal(self):
        return self.product.price*self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField(null=True)
    order_id=models.CharField(max_length=50,null=True)
    ordered_date=models.DateTimeField(null=True,auto_now_add=True)
    phone=models.IntegerField(null=True)
    address=models.TextField(null=True)
    is_ordered=models.BooleanField(default=False)
    payment_method=models.CharField(max_length=30,null=True)
    delivery_status=models.CharField(default="Pending")

    def __str__(self):
        return self.user.username

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.product.name