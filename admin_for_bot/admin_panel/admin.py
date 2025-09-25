from django.contrib import admin
from .models import Users, Categories, Products


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram', 'phone')
    search_fields = ('name', 'phone')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name', )

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category')
    search_fields = ('product_name', 'price')
    list_filter = ('category', )