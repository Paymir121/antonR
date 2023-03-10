from django.core.paginator import Paginator
from django.conf import settings


def page(request, posts):
    paginator = Paginator(posts, settings.PAGINATION_SIZE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
