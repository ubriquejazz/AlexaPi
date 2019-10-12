from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
# from django.core.urlresolvers import reverse
from . import models
from django.views.generic import View, ListView


# Create your views here.

def home(request):
    """
    View for rendering home for both: authorized and unauthorised users.
    """
    return render(request, 'home.html', {})
