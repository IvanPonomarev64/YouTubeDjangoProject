from django import template
from women.models import *
#  Создаем пользовательские теги, чтобы избежать повторения кода
register = template.Library()


#  Простой тег
@register.simple_tag()
def get_categories(filter_=None):
    if not filter_:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter_)


#  Включающий тег
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}
