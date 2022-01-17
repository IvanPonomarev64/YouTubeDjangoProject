from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # список отображения
    list_display_links = ('id', 'title')  # поля для редактирования
    search_fields = ('title', 'content')  # по каким полям производить поиск
    list_editable = ('is_published', )  # поля для редоктирования в админке
    list_filter = ('is_published', 'time_create')  # поля для фильтрации экземпляров в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'time_create')


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
