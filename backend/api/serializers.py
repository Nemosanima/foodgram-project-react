from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from recipes.models import Tag
from users.models import Follow
from django.contrib.auth import get_user_model


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')



