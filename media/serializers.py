from rest_framework.serializers import ModelSerializer, StringRelatedField
from museum.models import Picture, PictureFile, Size

class PictureFilesSerializer(ModelSerializer):
    class Meta:
        model = PictureFile
        fields = ('filename','extension','size_name', 'width')


class PictureSerializer(ModelSerializer):
    picturefiles = PictureFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Picture
        fields = ('filename','extension','picturefiles')
