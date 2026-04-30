from datetime import datetime, time, timedelta

from core.exceptions import (
    CancelamentoInvalidoError,
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
        self._ativo = True

    @property
    def paciente_id(self) -> int:
        return self._paciente_id

    @property
    def inicio(self) -> datetime:
        return self._inicio

    @property
    def fim(self) -> datetime:
        return self._inicio + timedelta(minutes=self._duracao_minutos)

    @property
    def duracao_minutos(self) -> int:
        return self._duracao_minutos

    @property
    def ativo(self) -> bool:
        return self._ativo

    def cancelar(self) -> None:
        self._ativo = False


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

    def cancelar(
        self,
        paciente_id: int,
        data_hora: datetime,
        agendamentos_existentes: list[Agendamento],
        data_hora_atual: datetime | None = None,
    ) -> None:
        """
        Tenta cancelar um agendamento aplicando as regras de negócio:
        1. O agendamento deve pertencer ao paciente solicitante.
        2. O cancelamento deve ocorrer com pelo menos 24h de antecedência.
        """

        if data_hora_atual is None:
            data_hora_atual = datetime.now()

        agendamento_alvo = None

        # 1. Busca o agendamento na lista pelo horário
        for agendamento in agendamentos_existentes:
            if agendamento.inicio == data_hora and agendamento.ativo:
                agendamento_alvo = agendamento
                break

        if not agendamento_alvo:
            raise CancelamentoInvalidoError(
                "Nenhum agendamento ativo encontrado neste horário."
            )

        # 2. Valida se o paciente que está cancelando é o dono da consulta
        if agendamento_alvo.paciente_id != paciente_id:
            # Esta é a mensagem exata que o seu primeiro teste espera!
            raise CancelamentoInvalidoError("Não é possível cancelar este agendamento.")

        # 3. Valida a regra de 24 horas de antecedência
        diferenca_de_tempo = agendamento_alvo.inicio - data_hora_atual

        # 86400 é a quantidade de segundos em 24 horas
        if diferenca_de_tempo.total_seconds() < 86400:
            raise CancelamentoInvalidoError(
                "Cancelamentos só são permitidos com 24 horas de antecedência."
            )

        # 4. Se passou por todas as barreiras de segurança, efetua o cancelamento
        agendamento_alvo.cancelar()
