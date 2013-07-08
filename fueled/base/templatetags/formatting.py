from django import template

register = template.Library()

def format_phone(value, arg):
    return arg.join([value[0:3],value[3:6],value[6:10]])

register.filter('format_phone', format_phone)
    
