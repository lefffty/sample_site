from django.contrib import admin

from .models import BillBoard


class BillBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published_at',)
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


admin.site.register(BillBoard, BillBoardAdmin)
