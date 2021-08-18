from django.contrib import admin

from main.models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 10
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Like)

