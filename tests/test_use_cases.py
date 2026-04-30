from datetime import timedelta

from django.test import TestCase  # type: ignore
from django.utils import timezone  # type: ignore

from application.use_cases import CancelarAgendamentoUseCase, CriarAgendamentoUseCase
from core.exceptions import CancelamentoInvalidoError, ConflitoHorarioError
from infra.django_repository import DjangoAgendamentoRepository
from rest_api.models import AgendamentoModel


class TestCriarAgendamentoUseCase(TestCase):
    def setUp(self) -> None:
        self.repositorio = DjangoAgendamentoRepository()
        self.use_case = CriarAgendamentoUseCase(self.repositorio)

    def test_deve_criar_agendamento_com_sucesso(self) -> None:
        # Arrange: Prepara um horário válido para amanhã às 09:00
        amanha = timezone.now() + timedelta(days=1)
        horario_valido = amanha.replace(hour=9, minute=0, second=0, microsecond=0)

        # Act: Executa o caso de uso
        agendamento = self.use_case.execute(paciente_id=10, inicio=horario_valido)

        # Assert: Garante que o objeto foi retornado e salvo no banco
        self.assertIsNotNone(agendamento)
        self.assertEqual(agendamento.paciente_id, 10)
        self.assertEqual(AgendamentoModel.objects.count(), 1)

    def test_deve_lancar_erro_ao_criar_com_conflito_de_horario(self) -> None:
        # Arrange
        amanha = timezone.now() + timedelta(days=1)
        horario = amanha.replace(hour=10, minute=0, second=0, microsecond=0)

        # Cria o primeiro agendamento com sucesso
        self.use_case.execute(paciente_id=1, inicio=horario)

        # Act & Assert: Tenta criar o segundo no MESMO horário e espera o erro
        with self.assertRaises(ConflitoHorarioError):
            self.use_case.execute(paciente_id=2, inicio=horario)


class TestCancelarAgendamentoUseCase(TestCase):
    def setUp(self) -> None:
        self.repositorio = DjangoAgendamentoRepository()
        self.use_case = CancelarAgendamentoUseCase(self.repositorio)

    def test_deve_cancelar_agendamento_com_sucesso(self) -> None:
        # Arrange: Cria direto no banco com antecedência de 2 dias
        inicio = timezone.now() + timedelta(days=2)
        modelo = AgendamentoModel.objects.create(
            paciente_id=1, inicio=inicio, duracao_minutos=30, ativo=True
        )

        # Act
        self.use_case.execute(agendamento_id=modelo.id, paciente_id=1)

        # Assert: O banco deve ter sido atualizado pelo Use Case
        modelo.refresh_from_db()
        self.assertFalse(modelo.ativo)

    def test_deve_lancar_erro_se_agendamento_nao_existir(self) -> None:
        # Act & Assert: Tenta cancelar um ID que não existe no banco vazio
        with self.assertRaisesRegex(ValueError, "Agendamento não encontrado."):
            self.use_case.execute(agendamento_id=999, paciente_id=1)

    def test_deve_lancar_erro_se_antecedencia_menor_que_24h(self) -> None:
        # Arrange: Cria um agendamento para daqui a apenas 2 horas
        inicio = timezone.now() + timedelta(hours=2)
        modelo = AgendamentoModel.objects.create(
            paciente_id=1, inicio=inicio, duracao_minutos=30, ativo=True
        )

        # Act & Assert: O Use Case deve deixar a exceção do Core "vazar" para cima
        with self.assertRaises(CancelamentoInvalidoError):
            self.use_case.execute(agendamento_id=modelo.id, paciente_id=1)
