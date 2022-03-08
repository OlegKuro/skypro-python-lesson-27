from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions

from ads.models import Advertisement, Category, Location
from ads.permissions import AdOwnerOrHasRoles
from ads.serializers import LocationSerializer, AdvertisementSerializer, CategorySerializer
from users.models import User
from rest_framework import status

from django.views.generic import UpdateView


def index(_):
    return JsonResponse({'status': status.HTTP_200_OK})


class CategoriesListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdsListCreate(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        qs = self.queryset
        param_getter = lambda param_name: self.request.query_params.get(param_name)
        categories = self.request.query_params.getlist('category_id')
        text = param_getter('text')
        location = param_getter('location')
        price_range = param_getter('price_from'), param_getter('price_to')

        if len(categories):
            qs = qs.filter(category__pk__in=categories)
        if text:
            qs = qs.filter(name__icontains=text)
        if location:
            qs = qs.filter(author__locations__name__icontains=location)
        if price_range[0] is not None and price_range[1] is not None:
            qs = qs.filter(price__range=price_range)
        return qs


class AdRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # как и написано в домашке, закрывыаю тока для чтения
            # иначе влепил бы permission_class = [permissions.IsAuthenticated]
            return [permissions.IsAuthenticated()]
        return AdOwnerOrHasRoles(User.ROLE_ADMIN, User.ROLE_MODERATOR)


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


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer