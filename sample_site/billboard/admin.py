from django.contrib import admin

from .models import BillBoard, Category, Comment


class BillBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', 'price', 'published_at', 'kind')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title', 'slug')
    search_fields = ('title', 'slug')


admin.site.register(Comment)
admin.site.register(BillBoard, BillBoardAdmin)
admin.site.register(Category, CategoryAdmin)
