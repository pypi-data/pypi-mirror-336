from rest_framework.serializers import ModelSerializer

from ..models import File


class FileWrite(
    ModelSerializer["File"],
):
    class Meta:
        model = File

        fields = ("file",)
