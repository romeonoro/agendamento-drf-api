# rest_api/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AgendamentoViewSet

# O Router automatiza a criação das URLs para as ViewSets
router = DefaultRouter()

# Como a sua ViewSet não usa o banco de dados direto (não tem a propriedade 'queryset'),
# precisamos passar o 'basename' para o Django não se perder.
router.register(r"agendamentos", AgendamentoViewSet, basename="agendamento")

urlpatterns = [
    path("", include(router.urls)),
]
