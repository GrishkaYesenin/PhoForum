from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def comments_filter(tree):
    res = """
        <ul>
            {}
        </ul>
        """
    i = ''

    for comment in tree:
        i += f"""
        <li>
            {comment.get('text')}
            {comment.get('timestamp_create')}
        </li>
        """
        if comment.get('children'):
            i += comments_filter(comment['children'])

    return mark_safe(res.format(i))