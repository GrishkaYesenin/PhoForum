from django.template import Library


register = Library()

def sum(*values):
    return