from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'choicapp/index.html', context=context)
 