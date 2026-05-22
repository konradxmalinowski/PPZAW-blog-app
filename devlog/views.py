from django.shortcuts import render


def handler429(request, exception=None):
    return render(request, '429.html', status=429)
