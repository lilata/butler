import random
import string

from django.conf import settings
from django.db import models

from . import utils

# Create your models here.
alias_chars = string.ascii_letters + string.digits + "-_~"
alias_chars_len = len(alias_chars)


def generate_url_alias(min_length=settings.SHORTENER_MIN_LENGTH):
    surl_len = ShortenedURL.objects.count()
    length = min_length
    while (alias_chars_len**length) * 0.4 < surl_len:
        length += 1
    is_alias_used = True
    alias = None
    while is_alias_used:
        alias = "".join(random.choices(alias_chars, k=length))
        is_alias_used = ShortenedURL.objects.filter(alias=alias).exists()
    return alias


class ShortenedURL(models.Model):
    url = models.TextField(unique=True)
    alias = models.TextField()

    @classmethod
    def add_url(cls, url):
        if utils.is_url_valid(url) is False:
            raise ValueError("bad url")
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            return cls.objects.create(url=url, alias=generate_url_alias())
