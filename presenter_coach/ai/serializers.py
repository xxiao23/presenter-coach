from django.contrib.auth import models
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MediaBlob

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
    

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MediaBlobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    data = serializers.ModelField(model_field=MediaBlob()._meta.get_field('data'))

    def create(self, validated_data):
        return MediaBlob.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance