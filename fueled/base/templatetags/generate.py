from django import template

register = template.Library()

def generate_rating_stars(value):
    value = int(value)
    html = ""
    for i in range(value):
        html += '<i class="icon-star star-yellow"></i>'
    for i in range(value, 5):
        html += '<i class="icon-star-empty star-black"></i>'
    return html

register.filter('generate_rating_stars', generate_rating_stars)
    

