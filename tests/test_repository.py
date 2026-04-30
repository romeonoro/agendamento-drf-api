from datetime import timedelta

from django.test import TestCase  # type: ignore
from django.utils import timezone  # type: ignore

from infra.django_repository import DjangoAgendamentoRepository


class TestAgendamentoRepositorio(TestCase):

    def setUp(self) -> None:
        self.repositorio = DjangoAgendamentoRepository()

    def test_deve_buscar_agendamento_por_id(self) -> None:
        from rest_api.models import AgendamentoModel

        horario = timezone.now() + timedelta(days=1)
        modelo = AgendamentoModel.objects.create(
            paciente_id=1, inicio=horario, duracao_minutos=30, ativo=True
        )

        agendamento_encontrado = self.repositorio.buscar_por_id(modelo.id)

        # assertIsNotNone avisa o Mypy que a partir daqui a variável não é None
        self.assertIsNotNone(agendamento_encontrado)
        if agendamento_encontrado:
            self.assertEqual(agendamento_encontrado.paciente_id, 1)
            self.assertTrue(agendamento_encontrado.ativo)

    def test_deve_retornar_none_ao_buscar_id_inexistente(self) -> None:
        resultado = self.repositorio.buscar_por_id(9999)
        self.assertIsNone(resultado)

    def test_deve_atualizar_status_do_agendamento(self) -> None:
        from rest_api.models import AgendamentoModel

        horario = timezone.now() + timedelta(days=1)
        modelo = AgendamentoModel.objects.create(
            paciente_id=2, inicio=horario, duracao_minutos=45, ativo=True
        )

        agendamento_core = self.repositorio.buscar_por_id(modelo.id)

        # O assert avisando o Mypy que o objeto existe
        self.assertIsNotNone(agendamento_core)
        if agendamento_core:
            agendamento_core.cancelar()
            self.repositorio.atualizar(agendamento_core)

        modelo_atualizado = AgendamentoModel.objects.get(id=modelo.id)
        self.assertFalse(modelo_atualizado.ativo)
