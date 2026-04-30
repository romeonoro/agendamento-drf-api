from datetime import date

from core.agendamento import Agendamento
from rest_api.models import AgendamentoModel


class DjangoAgendamentoRepository:

    def salvar(self, agendamento_entity: Agendamento, medico_nome: str) -> None:
        AgendamentoModel.objects.create(
            paciente_id=agendamento_entity.paciente_id,
            medico_nome=medico_nome,
            inicio=agendamento_entity.inicio,
            duracao_minutos=agendamento_entity.duracao_minutos,
        )

    def buscar_por_medico_e_data(
        self, medico_nome: str, data_alvo: date
    ) -> list[Agendamento]:
        # Busca apenas os agendamentos daquele médico naquele dia específico
        modelos = AgendamentoModel.objects.filter(
            medico_nome=medico_nome, inicio__date=data_alvo
        )

        # Converte os dados do banco de volta para a sua classe Pura
        return [
            Agendamento(
                paciente_id=model.paciente_id,
                inicio=model.inicio,
                duracao_minutos=model.duracao_minutos,
            )
            for model in modelos
        ]

    def listar_todos(self) -> list[dict]:
        modelos = AgendamentoModel.objects.all()

        resultado = []
        for model in modelos:
            resultado.append(
                {
                    "paciente_id": model.paciente_id,
                    "medico_nome": model.medico_nome,
                    "inicio": model.inicio,
                    "duracao_minutos": model.duracao_minutos,
                }
            )

        return resultado

    def buscar_por_id(self, agendamento_id: int) -> Agendamento | None:

        modelo = AgendamentoModel.objects.filter(id=agendamento_id).first()
        if not modelo:
            return None

        # Monta a entidade pura do Core
        agendamento = Agendamento(
            paciente_id=modelo.paciente_id,
            inicio=modelo.inicio,
            duracao_minutos=modelo.duracao_minutos,
        )

        # Garante que o status do banco reflita na entidade
        if not modelo.ativo:
            agendamento.cancelar()

        return agendamento

    def atualizar(self, agendamento: Agendamento) -> None:
        AgendamentoModel.objects.filter(
            paciente_id=agendamento.paciente_id, inicio=agendamento.inicio
        ).update(ativo=agendamento.ativo)
