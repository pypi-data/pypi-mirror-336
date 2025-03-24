from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()


router.register(
    prefix=r"files",
    viewset=views.File,
    basename="files",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
