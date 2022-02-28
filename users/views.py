import json

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Location
from lesson27 import settings
from users.models import User
from rest_framework import status


class UserListCreateView(CreateView, ListView):
    model = User

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()\
            .prefetch_related('locations')\
            .annotate(total_ads=Count('advertisements', filter=Q(advertisements__is_published=True)))
        paginator = Paginator(qs, settings.PAGINATOR_DEFAULT_ITEMS)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'num_pages': page_obj.paginator.num_pages,
            'total': page_obj.paginator.count,
            'items': [{
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'total_ads': user.total_ads,
                'locations': list(map(str, user.locations.all()))
            } for user in page_obj]
        }, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        try:
            with transaction.atomic():
                user = User.objects.create(**user_data)
                for location_name in user_data['locations']:
                    location, _ = Location.objects.get_or_create(name=location_name)
                    user.locations.add(location)
        except TypeError:
            return JsonResponse({'error': 'validation error ¯\_(ツ)_/¯'}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return JsonResponse({'error': 'probably it\'s constraint violation (｡•̀ᴗ-)✧'},
                                status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all())),
        }, status=status.HTTP_201_CREATED)


class UserRUDView(DetailView, UpdateView, DeleteView):
    model = User
    success_url = '/'

    def get(self, *args, **kwargs):
        user: User = self.get_queryset().prefetch_related('locations').get(pk=self.kwargs.get(self.pk_url_kwarg))
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all())),
        })

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]

        for location_name in user_data['locations']:
            location, _ = Location.objects.get_or_create(name=location_name)
            self.object.locations.add(location)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'locations': list(map(str, self.object.locations.all())),
        })

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)
