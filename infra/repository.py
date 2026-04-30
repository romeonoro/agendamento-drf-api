from core.agendamento import Agendamento
from core.exceptions import AgendamentoNaoEncontradoError


class AgendamentoRepositorio:
    def __init__(self) -> None:
        self._agendamentos: list[Agendamento] = []

    def adicionar(self, agendamento: Agendamento) -> None:
        self._agendamentos.append(agendamento)

    def buscar_todos(self) -> list[Agendamento]:
        return list(self._agendamentos)

    def remover(self, paciente_id: int) -> None:
        for consulta in self._agendamentos:
            if consulta.paciente_id == paciente_id:
                self._agendamentos.remove(consulta)
                return

        raise AgendamentoNaoEncontradoError(paciente_id)

    def buscar_por_id(self, agendamento_id: int) -> Agendamento | None:
        """Busca um agendamento no banco pelo ID. Retorna None se não encontrar."""

    def atualizar(self, agendamento: Agendamento) -> None:
        """Atualiza os dados de um agendamento existente no banco."""
