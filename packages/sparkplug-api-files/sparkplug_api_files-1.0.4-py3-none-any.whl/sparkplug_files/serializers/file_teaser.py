from decouple import config
from django.conf import settings
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from sparkplug_core.fields import UserUuidField

from .. import models


class FileTeaser(
    ModelSerializer["models.File"],
):
    creator_uuid = UserUuidField(source="creator")

    file = SerializerMethodField()

    class Meta:
        model = models.File

        fields = (
            "uuid",
            "created",
            "creator_uuid",
            "file",
        )

        read_only_fields = ("__all__",)

    def get_file(self, obj: models.File) -> str:
        if not obj.file:
            return ""

        environment = config("API_ENV")
        file_url = obj.file.url
        if environment == "dev":
            file_url = f"{settings.API_URL}{obj.file.url}"

        return file_url
