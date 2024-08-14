"""Module"""

from django.shortcuts import render

# ======================================================================
#                                               LOAD PAGE
# ======================================================================


# def error_404(request, exception=None):
#   return render(request,'landingpage/error_404.html')

def home(request):
    """docstring"""
    return render(request, 'landingpage/index.html')
