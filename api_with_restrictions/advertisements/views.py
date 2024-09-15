from rest_framework import viewsets, permissions
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def perform_create(self, serializer):
        user_ads = Advertisement.objects.filter(author=self.request.user, status='OPEN').count()
        if user_ads >= 10:
            return Response({'Ошибка': 'У вас не может быть более 10 открытых объявлений.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response({'Ошибка': 'У вас нет разрешения на удаление этого объявления.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()