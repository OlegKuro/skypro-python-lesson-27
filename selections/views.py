from rest_framework import generics, permissions
from selections.models import Selection
from selections import serializers as selection_serializers
from selections.permissions import IsSelectionAuthor


class RetrieveSelectionView(generics.RetrieveAPIView):
    queryset = Selection.objects.prefetch_related('items')
    serializer_class = selection_serializers.SelectionRetrieveView


class SelectionsListView(generics.ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = selection_serializers.SelectionBaseSerializer


class SelectionCreateView(generics.CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = selection_serializers.SelectionCreateUpdateView
    permission_classes = (permissions.IsAuthenticated,)


class SelectionUpdateDeleteView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = selection_serializers.SelectionCreateUpdateView
    permission_classes = (IsSelectionAuthor,)
