from django.contrib import admin

# Register your models here.
from smms.models import Product, Sale, TotalProduct, Profile


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category']
    list_display = ['name', 'category', 'quantity', 'date']
    # filter_by = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale)
admin.site.register(TotalProduct)
admin.site.register(Profile)
