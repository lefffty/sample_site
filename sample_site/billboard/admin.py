from django.contrib import admin

from .models import BillBoard, Category


class BillBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', 'price', 'published_at',)
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(BillBoard, BillBoardAdmin)
admin.site.register(Category, CategoryAdmin)
