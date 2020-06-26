"""
Views for whole project
"""
from django.shortcuts import render


def home(request):
    """
    Project home page, shown any unauthorized user
    """
    return render(request, 'home.html')


def goodbye(request):
    """
    Page, shown after logout
    """
    return render(request, 'goodbye.html')


def about(request):
    """
    About page
    """
    return render(request, 'about.html')


def terms(request):
    """
    Terms page
    """
    return render(request, 'terms.html')
