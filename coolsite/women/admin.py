from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Women, Category


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # список отображения
    list_display_links = ('id', 'title')  # поля для редактирования
    search_fields = ('title', 'content')  # по каким полям производить поиск
    list_editable = ('is_published', )  # поля для редоктирования в админке
    list_filter = ('is_published', 'time_create')  # поля для фильтрации экземпляров в админке
    prepopulated_fields = {'slug': ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published')  # редактируемые поля
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # нередактируемые поля
    save_on_top = True  # панель удалить-сохранить вверху

    def get_html_photo(self, object_):
        if object_.photo:
            return mark_safe(f"<img src='{object_.photo.url}' width=50")  # mark_save чтобы строка читалась как команда,
            # а не как строка

    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'time_create')
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
