from django.contrib import admin
from .models import Category, Subcategory, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'slug', 'description')
    search_fields = ('cat_name', 'description')
    prepopulated_fields = {'slug': ('cat_name',)}

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('subcat_name', 'slug', 'category', 'description')
    search_fields = ('subcat_name', 'description')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('subcat_name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'category', 'subcategory', 'price', 'stock', 'is_available')
    search_fields = ('product_name', 'description', 'categorycat_name', 'subcategorysubcat_name')
    list_filter = ('category', 'subcategory', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
