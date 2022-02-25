import json

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Location
from lesson27 import settings
from users.models import User
from rest_framework import status


class UserListCreateView(CreateView, ListView):
    model = User

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
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
                'location': str(user.location)
            } for user in page_obj]
        }, safe=False)

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        location = get_object_or_404(User, user_data['location_id'])

        try:
            user = User.objects.create({
                **user_data,
                **{
                    'location': location,
                }
            })
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
            'location': str(user.location),
        }, safe=False)


class UserRUDView(DetailView, UpdateView, DeleteView):
    model = User
    success_url = '/'

    def get(self, *args, **kwargs):
        user: User = self.get_object()
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location': str(user.location),
        }, safe=False)

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.location = get_object_or_404(Location, user_data['location_id'])
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'location': str(self.object.location),
        })

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)
