
from django.contrib import admin
from .models import *


# Register your models here.
class Post_LU_Category(admin.ModelAdmin):
    list_display=['Category','Descriptions','date']
    list_filter =['Category','date']
    search_fields=['Category','Descriptions']
admin.site.register(LU_Category,Post_LU_Category)
# Register your models here.
class Post_LU_Item(admin.ModelAdmin):
    list_display=['Item','Descriptions','date']
    list_filter =['Item','date']
    search_fields=['Item','Descriptions']
admin.site.register(LU_Item,Post_LU_Item)
# Register your models here.
class Post_Product(admin.ModelAdmin):
    list_display=['Product','Descriptions','date']
    list_filter =['Product','date']
    search_fields=['Product','Descriptions']
admin.site.register(Product,Post_Product)
# Register your models here.
class Post_LU_Value(admin.ModelAdmin):
    list_display=['id','Category','Item','Value','Comments','date']
    list_filter =['Category','Item','Value','date']
    search_fields=['id','Category__Category','Item__Item','Value','Comments']
admin.site.register(LU_Value,Post_LU_Value)
# Register your models here.
class Post_ASO_Configuration(admin.ModelAdmin):
    list_display=['Project','Customer','Product','Value','Comments','date']
    list_filter =['Project','Customer','Product','Value__Category__Category','Value__Item__Item','date']#,'Value'
    search_fields=['Project','Customer','Product__Product','Value__Value','Value__Category__Category','Value__Item__Item','Comments','date']
admin.site.register(ASO_Configuration,Post_ASO_Configuration)

admin.site.site_title = "Admin SMST Portal"
admin.site.index_title = "Welcome to Admin SMST "
admin.site.site_header= "SMST"