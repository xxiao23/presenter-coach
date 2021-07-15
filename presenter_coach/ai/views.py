from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, MediaBlobSerializer
from .models import MediaBlob

import logging


logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, "ai/index.html", context={})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MediaBlobList(APIView):
    def get(self, request, format=None):
        mediaBlobs = MediaBlob.objects.all()
        serializer = MediaBlobSerializer(mediaBlobs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # logger.info(f'request data: {request.data}')
        serializer = MediaBlobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info(f'serializer error: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaBlobDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = MediaBlob.objects.all()
    serializer_class = MediaBlobSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)