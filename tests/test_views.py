from datetime import timedelta

from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.test import APIClient  # type: ignore

from rest_api.models import AgendamentoModel


class TestAgendamentoViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_deve_cancelar_agendamento_com_sucesso_via_api(self) -> None:
        # Arrange: Cria a consulta no banco (com antecedência maior que 24h)
        horario = timezone.now() + timedelta(days=2)
        agendamento = AgendamentoModel.objects.create(
            paciente_id=1, inicio=horario, duracao_minutos=30, ativo=True
        )

        # A URL padrão que vamos criar no ViewSet com a action 'cancelar'
        url = reverse("agendamentos-cancelar", args=[agendamento.id])

        # Act: Simula uma requisição HTTP PATCH passando o paciente_id no corpo
        response = self.client.patch(url, {"paciente_id": 1}, format="json")

        # Assert: A API deve retornar sucesso (200 OK) e o banco deve atualizar
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agendamento.refresh_from_db()
        self.assertFalse(agendamento.ativo)

    def test_deve_retornar_erro_400_se_regra_de_negocio_falhar(self) -> None:
        # Arrange: Cria a consulta para daqui a 1 hora (vai quebrar a regra das 24h)
        horario = timezone.now() + timedelta(hours=1)
        agendamento = AgendamentoModel.objects.create(
            paciente_id=1, inicio=horario, duracao_minutos=30, ativo=True
        )
        url = reverse("agendamentos-cancelar", args=[agendamento.id])

        # Act
        response = self.client.patch(url, {"paciente_id": 1}, format="json")

        # Assert: A API deve capturar a exceção do domínio e retornar 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("24 horas", response.data["erro"])  # type: ignore

        # Garante que o banco NÃO foi alterado, protegendo os dados
        agendamento.refresh_from_db()
        self.assertTrue(agendamento.ativo)
