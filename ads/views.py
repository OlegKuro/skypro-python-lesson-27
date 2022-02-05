from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView


class BaseView(ListView):
    model = None

    def get(self, *args, **kwargs):
        return JsonResponse({'status': 200}, safe=False)
