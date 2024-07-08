from django.shortcuts import render


def error_500(request, *args, **kwargs):
    return render(request, 'courses/errors/500.html')