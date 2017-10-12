from rest_framework.serializers import ModelSerializer
from museum.models import Picture

class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
