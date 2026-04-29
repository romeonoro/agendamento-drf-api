from datetime import datetime, time, timedelta

from core.exceptions import (
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
)


class Agendamento:
    def __init__(
        self, paciente_id: int, inicio: datetime, duracao_minutos: int
    ) -> None:
        self._paciente_id = paciente_id
        self._inicio = inicio
        self._duracao_minutos = duracao_minutos

    @property
    def paciente_id(self) -> int:
        return self._paciente_id

    @property
    def inicio(self) -> datetime:
        return self._inicio

    @property
    def fim(self) -> datetime:
        return self._inicio + timedelta(minutes=self._duracao_minutos)


class Medico:
    def __init__(
        self,
        nome: str,
        inicio_turno: time,
        fim_turno: time,
        intervalo_atendimento: int = 30,
    ) -> None:
        self._nome = nome
        self._inicio_turno = inicio_turno
        self._fim_turno = fim_turno
        self._intervalo_atendimento = intervalo_atendimento

    @property
    def nome(self) -> str:
        return self._nome

    def _esta_no_horario_de_trabalho(self, agendamento: Agendamento) -> bool:
        return (
            self._inicio_turno <= agendamento.inicio.time()
            and agendamento.fim.time() <= self._fim_turno
        )

    def _existe_conflito(
        self, novo: Agendamento, existentes: list[Agendamento]
    ) -> bool:
        for existente in existentes:
            if novo.inicio < existente.fim and novo.fim > existente.inicio:
                return True
        return False

    def _respeita_grade_de_intervalo(self, data_hora: datetime) -> bool:
        return data_hora.minute % self._intervalo_atendimento == 0

    def agendar(
        self,
        paciente_id: int,
        data_hora: datetime,
        agendamentos_existentes: list[Agendamento],
    ) -> Agendamento:

        if not self._respeita_grade_de_intervalo(data_hora):
            raise IntervaloInvalidoError()

        novo_agendamento = Agendamento(
            paciente_id, data_hora, self._intervalo_atendimento
        )

        if not self._esta_no_horario_de_trabalho(novo_agendamento):
            raise ForaDoHorarioError()

        if self._existe_conflito(novo_agendamento, agendamentos_existentes):
            raise ConflitoHorarioError()

        return novo_agendamento
