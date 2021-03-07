from django import template
from django_consent import models

register = template.Library()


@register.simple_tag
def consent_sources():
    return models.ConsentSource.objects.all()
