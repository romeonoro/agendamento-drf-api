import unittest
from datetime import datetime

from core.agendamento import Agendamento
from core.exceptions import AgendamentoNaoEncontradoError
from infra.repository import AgendamentoRepositorio


class TestAgendamentoRepositorio(unittest.TestCase):

    def test_deve_remover_agendamento_com_sucesso(self) -> None:
        repo = AgendamentoRepositorio()
        horario = datetime(2026, 4, 25, 9, 0)
        consulta = Agendamento(paciente_id=101, inicio=horario, duracao_minutos=30)

        repo.adicionar(consulta)
        self.assertEqual(len(repo.buscar_todos()), 1)

        repo.remover(paciente_id=101)

        self.assertEqual(len(repo.buscar_todos()), 0)

    def test_erro_ao_remover_agendamento_inexistente(self) -> None:
        repo = AgendamentoRepositorio()

        with self.assertRaisesRegex(
            AgendamentoNaoEncontradoError, "Nenhuma consulta encontrada"
        ):
            repo.remover(paciente_id=999)
