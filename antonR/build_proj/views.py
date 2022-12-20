from django.shortcuts import render


def index(request):
    template = 'ice_cream/index.html'
    return render(request, template)