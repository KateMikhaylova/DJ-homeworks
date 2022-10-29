from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist

from advertisements.filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.permissions import IsOwnerOrAdmin, IsOwnerOrNotDraft

from advertisements.models import Advertisement, Favourite
from advertisements.serializers import AdvertisementSerializer

from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        if self.action == 'retrieve':
            return [IsOwnerOrNotDraft()]
        return []

    def list(self, request, *args, **kwargs):
        try:
            queryset = Advertisement.objects.all().exclude(~Q(creator=request.user), status='DRAFT')
            queryset = self.filter_queryset(queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)
        except TypeError:
            queryset = Advertisement.objects.all().exclude(status='DRAFT')
            queryset = self.filter_queryset(queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_favourite(self, request, pk=None):
        advertisement = self.get_object()
        if request.user == advertisement.creator:
            return Response({'error': 'You cannot add your advertisement to favourites'})
        try:
            Favourite.objects.get(advertisement=advertisement, user=request.user)
            return Response({'error': 'You have already added this advertisement to favourites'})
        except ObjectDoesNotExist:
            Favourite(advertisement=advertisement, user=request.user).save()
            return Response({'success': 'Advertisement is added to favourites'})
        except TypeError:
            return Response({'error': 'Only registered users can add advertisements to favourites'})

    @action(detail=True, methods=['delete'])
    def delete_from_favourite(self, request, pk=None):
        advertisement = self.get_object()
        try:
            favourite = Favourite.objects.get(advertisement=advertisement, user=request.user)
            favourite.delete()
            return Response({'success': 'You have deleted this advertisement from favourites'})
        except ObjectDoesNotExist:
            return Response({'error': 'This advertisement is not in your favourites'})
        except TypeError:
            return Response({'error': 'Only registered users can delete advertisements from favourites'})

    @action(detail=False, methods=['get'])
    def favourite(self, request):
        try:
            advertisements = Advertisement.objects.filter(favourites__user=request.user)
            serializer = AdvertisementSerializer(advertisements, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'error': 'Only registered users can see their favourites'})
