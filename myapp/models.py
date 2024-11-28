from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class register(models.Model):
    username=models.CharField(max_length=50)
    emailaddress = models.EmailField(null=True)
    password=models.CharField(max_length=50)
    Mobileno=models.CharField(max_length=10)

    def __str__(self):
        return self.username


class Product(models.Model):
    name=models.CharField(max_length=60)
    Description = models.CharField(max_length=1000,null=True)
    price=models.IntegerField()
    packaging_date=models.DateField(null=True)
    Expiry_date = models.DateField(null=True)
    Product_weight=models.IntegerField()
    product_image = models.ImageField(upload_to="photos", null=True)


    def __str__(self):
        return self.name

class ProductImage(models.Model):
    p_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    p_image = models.ImageField(upload_to="photos", null=False)

class CartItem(models.Model):
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)  # Make sure this line exists
    tprice = models.IntegerField()
    quantity = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s cart item"


  

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"

# class OrderItems(models.Model):
#     user = models.ForeignKey(register, on_delete=models.CASCADE)
#     product = models.ManyToManyField(Product,related_name='purchased')
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return self.product.name

class OrderedItems(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    cart = models.ManyToManyField(CartItem)
    totalPrice = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ordered Item'
        verbose_name_plural = 'Ordered Items'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
