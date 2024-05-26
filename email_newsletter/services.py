from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Если статьи есть, то берем из в кеш,
    если нет в кеш - то из БД
    """
    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = "blogs_list"
    blogs = cache.get(key)
    if blogs is not None:
        return blogs
    blogs = Blog.objects.all()
    cache.get(key)
    return blogs
