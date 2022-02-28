from django.shortcuts import render

# Create your views here.

def IndexView(requests):
    return render(requests, 'recipes/index.html', {})
