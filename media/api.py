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
import imghdr


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

        hash = hashlib.md5(file_obj.read()).hexdigest()
        file_obj.seek(0)

        if Picture.objects.filter(pk=hash).exists():
            response = 200
            picture = Picture.objects.get(pk=hash)
        else:
            response = 201
            picture = Picture()
            picture.owner = request.user
            picture.original_file = file_obj
            picture.save()
            try:
                picture.resize_image()
            except:
                picture.delete()
                return Response({'error': 'The uploaded file is not an image'}, status=404)
            
        filename, file_extension = os.path.splitext(os.path.basename(picture.original_file.path))
        return Response(PictureSerializer(picture).data, status=response)


    def retrieve(self, request, pk=None):
        if Picture.objects.filter(pk=pk).exists():
            picture = Picture.objects.get(pk=pk)
            filename, file_extension = os.path.splitext(os.path.basename(picture.original_file.path))
            return Response({'id': picture.pk, 'name': filename, 'extension': file_extension}, status=200)
        return Response({'not_found': pk}, status=404)
