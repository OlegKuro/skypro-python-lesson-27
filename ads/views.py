import json

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ads.models import Advertisement, Category
from lesson27 import settings
from users.models import User
from rest_framework import status

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def index(_):
    return JsonResponse({'status': status.HTTP_200_OK})


class CategoriesListCreate(ListView, CreateView):
    model = Category

    def get(self, *args, **kwargs):
        return JsonResponse([{
            'id': cat.pk,
            'name': cat.name,
        } for cat in self.get_queryset().order_by('name')], safe=False)

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        try:
            category = Category.objects.create(**category_data)
        except TypeError:
            return JsonResponse({'error': 'validation error ¯\_(ツ)_/¯'}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return JsonResponse({'error': 'probably it\'s constraint violation (｡•̀ᴗ-)✧'},
                                status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({
            'id': category.pk,
            'name': category.name,
        }, status=status.HTTP_201_CREATED)


class CategoryRetrieveUpdateView(DetailView, UpdateView, DeleteView):
    model = Category
    success_url = '/'

    def get(self, *args, **kwargs):
        category: Category = self.get_object()
        return JsonResponse({
            'id': category.pk,
            'name': category.name,
        })

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        })

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)


class AdsListCreate(ListView, CreateView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset().select_related('author').order_by('-price')
        paginator = Paginator(qs, settings.PAGINATOR_DEFAULT_ITEMS)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'num_pages': page_obj.paginator.num_pages,
            'total': page_obj.paginator.count,
            'items': [{
                'id': ad.id,
                'name': ad.name,
                'author_id': ad.author_id,
                'author': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'category_id': ad.category_id,
                'image': ad.image.url if ad.image else None,
            } for ad in page_obj]
        })

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, ad_data['author_id'])
        category = get_object_or_404(Category, ad_data['category_id'])

        try:
            ad = Advertisement.objects.create({
                **ad_data,
                **{
                    'author': author,
                    'category': category,
                }
            })
        except TypeError:
            return JsonResponse({'error': 'validation error ¯\_(ツ)_/¯'}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return JsonResponse({'error': 'probably it\'s constraint violation (｡•̀ᴗ-)✧'},
                                status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author_id,
            'author': ad.author.first_name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category_id,
            'image': ad.image.url if ad.image else None,
        }, status=status.HTTP_201_CREATED)


class AdUpdateRetrieveView(DetailView, UpdateView, DeleteView):
    model = Advertisement
    success_url = '/'

    def get(self, *args, **kwargs):
        ad: Advertisement = self.get_object()
        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author_id,
            'author': ad.author.first_name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category_id,
            'image': ad.image.url if ad.image else None,
        })

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]

        self.object.author = get_object_or_404(User, ad_data["author_id"])
        self.object.category = get_object_or_404(Category, ad_data["category_id"])

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id,
            'author': self.object.author.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None,
        })

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)


class UploadAdImageView(UpdateView):
    model = Advertisement
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id,
            'author': self.object.author.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None,
        }, status=status.HTTP_200_OK)
