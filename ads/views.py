import json

from django.db import IntegrityError
from django.http import JsonResponse
from ads.models import Advertisement, Category
from rest_framework import status

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView


def index(_):
    return JsonResponse({'status': status.HTTP_200_OK}, safe=False)


class CategoriesListCreate(ListView, CreateView):
    model = Category

    def get(self, *args, **kwargs):
        return JsonResponse([{
            'id': cat.pk,
            'name': cat.name,
        } for cat in self.get_queryset()], safe=False)

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        try:
            category = Category.objects.create(**category_data)
        except TypeError:
            return JsonResponse({'error': 'validation error ¯\_(ツ)_/¯'}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return JsonResponse({'error': 'probably it\'s constraint violation (｡•̀ᴗ-)✧'}, status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({
            'id': category.pk,
            'name': category.name,
        }, safe=False, status=status.HTTP_201_CREATED)


class AdsListCreate(ListView, CreateView):
    model = Advertisement

    def get(self, *args, **kwargs):
        return JsonResponse([{
            'id': ad.pk,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
        } for ad in self.get_queryset()], safe=False)

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        try:
            ad = Advertisement.objects.create(**ad_data)
        except TypeError:
            return JsonResponse({'error': 'validation error ¯\_(ツ)_/¯'}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return JsonResponse({'error': 'probably it\'s constraint violation (｡•̀ᴗ-)✧'}, status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
        }, safe=False)


class DetailAd(DetailView):
    model = Advertisement

    def get(self, *args, **kwargs):
        ad: Advertisement = self.get_object()
        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
        }, safe=False)


class DetailCategory(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        category: Category = self.get_object()
        return JsonResponse({
            'id': category.pk,
            'name': category.name,
        }, safe=False)
