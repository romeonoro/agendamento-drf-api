from datetime import date
from typing import List, Optional

from core.agendamento import Agendamento
from infra.repository import AgendamentoRepositorio  # Importando a interface
from rest_api.models import AgendamentoModel


class DjangoAgendamentoRepository(AgendamentoRepositorio):  # Herança explícita

    def salvar(self, agendamento: Agendamento, medico_nome: str) -> None:
        AgendamentoModel.objects.create(
            paciente_id=agendamento.paciente_id,
            medico_nome=medico_nome,
            inicio=agendamento.inicio,
            duracao_minutos=agendamento.duracao_minutos,
            ativo=agendamento.ativo,
        )

    def buscar_por_medico_e_data(
        self, medico_nome: str, data: date
    ) -> List[Agendamento]:
        modelos = AgendamentoModel.objects.filter(
            medico_nome=medico_nome, inicio__date=data
        )

        return [
            Agendamento(
                paciente_id=model.paciente_id,
                inicio=model.inicio,
                duracao_minutos=model.duracao_minutos,
            )
            for model in modelos
        ]

    def listar_todos(self) -> List[Agendamento]:
        # Refatorado: Agora retorna Entidades em vez de dicionários
        modelos = AgendamentoModel.objects.all()

        return [
            Agendamento(
                paciente_id=model.paciente_id,
                inicio=model.inicio,
                duracao_minutos=model.duracao_minutos,
            )
            for model in modelos
        ]

    def buscar_por_id(self, agendamento_id: int) -> Optional[Agendamento]:
        modelo = AgendamentoModel.objects.filter(id=agendamento_id).first()
        if not modelo:
            return None

        agendamento = Agendamento(
            paciente_id=modelo.paciente_id,
            inicio=modelo.inicio,
            duracao_minutos=modelo.duracao_minutos,
        )

        if not modelo.ativo:
            agendamento.cancelar()

        return agendamento

    def atualizar(self, agendamento: Agendamento) -> None:
        # Nota: Filtramos por campos únicos para garantir a atualização correta
        AgendamentoModel.objects.filter(
            paciente_id=agendamento.paciente_id, inicio=agendamento.inicio
        ).update(ativo=agendamento.ativo)
