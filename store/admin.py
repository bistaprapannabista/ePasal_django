from django.contrib import admin
from store.models import ProductCategory, Product, Order
# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.get_fields() if field.name != 'id']

admin.site.site_header = "ePasal Admin"
admin.site.site_title = "ePasal Admin Portal"
admin.site.index_title = "Welcome to ePasal Portal"