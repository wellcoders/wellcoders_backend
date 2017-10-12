import base64
import os
import copy
from PIL import Image
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from museum.models import Picture
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from media.serializers import PictureSerializer
from django.core.files import File
import hashlib


class MediaUploadViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    allowed_content_types = ('image/png', 'image/jpeg', )
    serializer_class = PictureSerializer

    def create(self, request):
        file_obj = request.data.get('file') or None

        if not file_obj:
            return Response({'error': _('Missing \'file\' parameter in request')}, status=400)

        if file_obj.content_type not in self.allowed_content_types:
            return Response({'error': _(u'File content type {0} not allowed'.format(file_obj.content_type)),
                             'file': file_obj.name}, status=400)

        #file_path = os.path.join(settings.BASE_DIR, 'temp', file_obj.name)


        hash = hashlib.md5(file_obj.read()).hexdigest()
        file_obj.seek(0)

        if Picture.objects.filter(pk=hash).exists():
            response = 200
            picture = Picture.objects.get(pk=hash)
        else:
        #hash = hashlib.md5(file_obj.open().read()).hexdigest()
        #gallery_tasks.museum_create_picture_by_image.delay(file_path, request.user.pk)
            response = 201
            picture = Picture()
            picture.owner = request.user
            picture.original_file = file_obj
            picture.save()

        filename, file_extension = os.path.splitext(os.path.basename(picture.name))
        return Response({'id': picture.pk, 'name': filename, 'extension': file_extension}, status=response)


    def retrieve(self, request, pk=None):
        print(pk)
        if Picture.objects.filter(pk=pk).exists():
            picture = Picture.objects.get(pk=pk)
            filename, file_extension = os.path.splitext(os.path.basename(picture.name))
            return Response({'id': picture.pk, 'name': filename, 'extension': file_extension}, status=200)
        return Response({'not_found': pk}, status=404)