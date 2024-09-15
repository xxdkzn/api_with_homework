from django.contrib.auth.models import User
from rest_framework import serializers

from api_with_restrictions.advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # Проверяем статус объявления
        if data.get('status') not in dict(Advertisement.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Статус должен быть 'OPEN' или 'CLOSED'.")

        # Проверяем количество открытых объявлений у автора
        if self.instance is None:  # Создание нового объявления
            user_ads = Advertisement.objects.filter(author=self.context['request'].user, status='OPEN').count()
            if user_ads >= 10:
                raise serializers.ValidationError("У вас не может быть более 10 открытых объявлений.")

        return data