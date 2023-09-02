from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class ProductCategory(models.Model):
    category_name = models.CharField("Category Name",max_length=255)
    added_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_name = models.CharField("Product Name",max_length=255)
    product_description = models.TextField("Product Description")
    product_price = models.FloatField("Product Price")
    product_image = models.ImageField(upload_to = "images/",null=True)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_product(id):
        return Product.objects.get(id=id)

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    address = models.CharField(max_length=255,default='')
    phone = models.CharField(max_length=12,default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user__id=user_id).order_by('-date')

    def __str__(self):
        return f"{str(self.quantity)} {self.product.product_name} By {self.user.username}"