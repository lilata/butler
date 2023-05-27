import math
import os
import random
import string
import uuid

from django.conf import settings
from django.db import models

from . import utils

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


class Comment(models.Model):
    key = models.CharField(max_length=255)
    poster = models.CharField(max_length=100)
    text = models.TextField()
    inserted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-inserted_at",)

    @classmethod
    def add_comment(cls, key, poster, text):
        return cls.objects.create(key=key, poster=poster, text=text)

    @classmethod
    def comments(cls, key, page=1, page_size=10) -> dict:
        from . import serializers

        comments = cls.objects.filter(key=key).all()[
            (page - 1) * page_size : page * page_size
        ]
        return serializers.CommentSerializer(comments, many=True).data

    @classmethod
    def page_count(cls, key, page_size=10) -> int:
        return math.ceil(cls.objects.filter(key=key).count() / page_size)


def protected_file_upload_to(instance, filename):
    dir_name = settings.PROTECTED_FILE_UPLOAD_DIR
    os.makedirs(dir_name, exist_ok=True)
    return f"{dir_name}/{filename}"


class ProtectedFile(models.Model):
    code = models.TextField()
    file = models.FileField(upload_to=protected_file_upload_to)

    @classmethod
    def get_file(cls, filename, code):
        path = f"{settings.PROTECTED_FILE_UPLOAD_DIR}/{filename}"
        f = cls.objects.filter(file=path).first()
        if f is not None and f.code == code:
            return f
        return None
