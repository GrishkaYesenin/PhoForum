from django.template import Library
from ..models import ParentCategory, Category
register = Library()


@register.inclusion_tag('forum/sidebar.html')
def show_sidebar():
    return {'p_categories': ParentCategory.objects.all(), 'categories': Category.objects.all()}