from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()


router.register(
    prefix=r"videos",
    viewset=views.Video,
    basename="videos",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
