from django import template
from django.urls import reverse
from monapp.urls import urlpatterns

register = template.Library()

@register.simple_tag
def get_urlpatterns():
    links = []
    for pattern in urlpatterns:
        try:
            # Attempt to reverse the URL pattern to get the URL
            url = reverse(pattern.name)
            links.append((url, pattern.name))
        except:
            pass
    return links