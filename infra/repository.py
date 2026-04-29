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
