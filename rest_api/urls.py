# rest_api/urls.py
from django.urls import include, path  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore

from .views import AgendamentoViewSet

router = DefaultRouter()
router.register(r"agendamentos", AgendamentoViewSet, basename="agendamentos")

urlpatterns = [
    path("", include(router.urls)),
]
