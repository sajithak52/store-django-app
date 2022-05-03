from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product_images')
    selling_price = models.IntegerField()
    mrp = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=True, null=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.name
