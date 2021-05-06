from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class LU_Category(models.Model):
    Category=models.CharField(max_length=100,primary_key=True)
    Descriptions=models.TextField(null=True, blank=True,)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Category

class LU_Item(models.Model):
    Item=models.CharField(max_length=100,primary_key=True)
    Descriptions=models.TextField(null=True, blank=True,)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Item

class Product(models.Model):
    Product=models.CharField(max_length=100,primary_key=True)
    Descriptions=models.TextField(null=True, blank=True,)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Product

class LU_Value(models.Model):
    Category=models.ForeignKey(LU_Category,on_delete=models.DO_NOTHING,blank=True, null=False,)
    Item=models.ForeignKey(LU_Item,on_delete=models.DO_NOTHING,blank=True, null=False,)
    Value=models.CharField(max_length=100,)
    Comments=models.TextField(null=True, blank=True,)
    date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return  (str(self.Category) + '---' + str(self.Item) + ':' + ' ' + ' '+str(self.Value))

    class Meta:
        managed = True
        unique_together = (("Category", "Item", "Value"),)
        ordering = ("Category","Item", "Value",)

class ASO_Configuration(models.Model):
    Project = models.IntegerField(default=1,validators=[MaxValueValidator(9999999), MinValueValidator(1000000)],)
    Customer=models.CharField(max_length=100, null=True, blank=True)
    Product=models.ForeignKey(Product,max_length=100,on_delete=models.DO_NOTHING,blank=True, null=False,)
    Value=models.ForeignKey(LU_Value,max_length=100,on_delete=models.DO_NOTHING,blank=True, null=True,)
    date=models.DateTimeField(auto_now=True)
    Comments=models.TextField(null=True, blank=True,)

    def __str__(self):
        return str(self.Project)
        
    class Meta:
        managed = True
        unique_together = (("Project", "Product","Value"),)
        #ordering = ("Project","Customer",)