from datetime import datetime, time

from django.utils import timezone  # type: ignore

from core.agendamento import Agendamento, Medico
from infra.repository import AgendamentoRepositorio


class CriarAgendamentoUseCase:
    def __init__(self, repositorio: AgendamentoRepositorio):
        self.repositorio = repositorio

    def execute(self, paciente_id: int, inicio: datetime) -> Agendamento:
        medico = Medico(
            nome="Dr. Sistema",
            inicio_turno=time(8, 0),
            fim_turno=time(18, 0),
            intervalo_atendimento=30,
        )

        # Busca o contexto
        data_do_agendamento = inicio.date()
        existentes = self.repositorio.buscar_por_medico_e_data(
            medico.nome, data_do_agendamento
        )

        # Executa a regra do Core
        novo_agendamento = medico.agendar(
            paciente_id=paciente_id,
            data_hora=inicio,
            agendamentos_existentes=existentes,
        )

        # Salva na Infra
        self.repositorio.salvar(novo_agendamento, medico.nome)

        return novo_agendamento


class CancelarAgendamentoUseCase:
    # Injeção de Dependência: O caso de uso pede "um repositório qualquer"
    def __init__(self, repositorio: AgendamentoRepositorio):
        self.repositorio = repositorio

    def execute(self, agendamento_id: int, paciente_id: int) -> None:
        # 1. Busca a entidade
        agendamento_core = self.repositorio.buscar_por_id(agendamento_id)
        if not agendamento_core:
            raise ValueError("Agendamento não encontrado.")

        # 2. Instancia o Domínio
        medico = Medico(
            nome="Dr. Sistema",
            inicio_turno=time(8, 0),
            fim_turno=time(18, 0),
            intervalo_atendimento=30,
        )

        agendamentos_do_medico = [agendamento_core]

        # 3. Executa a Regra de Negócio
        medico.cancelar(
            paciente_id=paciente_id,
            data_hora=agendamento_core.inicio,
            agendamentos_existentes=agendamentos_do_medico,
            data_hora_atual=timezone.now(),
        )

        # 4. Persiste a mudança
        self.repositorio.atualizar(agendamento_core)
