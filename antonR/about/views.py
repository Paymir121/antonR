from django.views.generic.base import TemplateView


class PageAboutAuthor(TemplateView):
    template_name = 'about/author.html'


class PageTech(TemplateView):
    template_name = 'about/tech.html'
