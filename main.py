from datetime import datetime, time

from api.agendamento import Medico
from api.exceptions import (
    AgendamentoNaoEncontradoError,
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
)
from infra.repository import AgendamentoRepositorio


def simular_dia_na_clinica() -> None:
    print("=== INICIANDO SISTEMA DE AGENDAMENTOS ===\n")

    repo = AgendamentoRepositorio()
    dr_house = Medico(
        nome="Dr. House",
        inicio_turno=time(8, 0),
        fim_turno=time(12, 0),
        intervalo_atendimento=30,
    )

    print(f"👨‍⚕️ Médico cadastrado: {dr_house.nome}")
    print("⏰ Turno: 08:00 às 12:00 (Consultas de 30 min)\n")

    def tentar_agendar(paciente_id: int, data_hora: datetime) -> None:
        hora_str = data_hora.strftime("%H:%M")
        print(f"Tentando agendar Paciente ID {paciente_id} para {hora_str}...")

        try:
            agenda_atual = repo.buscar_todos()
            nova_consulta = dr_house.agendar(paciente_id, data_hora, agenda_atual)
            repo.adicionar(nova_consulta)
            print("✅ Sucesso: Consulta agendada!\n")

        except ForaDoHorarioError as e:
            print(f"❌ Bloqueado (Fora do Horário): {e}\n")
        except IntervaloInvalidoError as e:
            print(f"❌ Bloqueado (Grade Inválida): {e}\n")
        except ConflitoHorarioError as e:
            print(f"❌ Bloqueado (Conflito): {e}\n")
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"❌ Erro Inesperado: {e}\n")

    def tentar_cancelar(paciente_id: int) -> None:
        print(f"Tentando cancelar a consulta do Paciente ID {paciente_id}...")
        try:
            repo.remover(paciente_id)
            print("✅ Sucesso: Consulta cancelada com sucesso!\n")
        except AgendamentoNaoEncontradoError as e:
            print(f"❌ Erro ao cancelar: {e}\n")

    # --- Executando os Cenários da Simulação ---

    # 1. Agendando com sucesso
    tentar_agendar(paciente_id=101, data_hora=datetime(2026, 4, 25, 9, 0))
    tentar_agendar(paciente_id=103, data_hora=datetime(2026, 4, 25, 9, 30))

    # 2. Conflito proposital
    tentar_agendar(paciente_id=104, data_hora=datetime(2026, 4, 25, 9, 0))

    # 3. Cancelando uma consulta existente
    tentar_cancelar(paciente_id=101)

    # 4. Agendando no horário que acabou de vagar
    tentar_agendar(paciente_id=999, data_hora=datetime(2026, 4, 25, 9, 0))

    # 5. Tentando cancelar alguém que não existe
    tentar_cancelar(paciente_id=888)

    print("=== AGENDA FINAL ===")
    consultas_salvas = repo.buscar_todos()

    if not consultas_salvas:
        print("Nenhuma consulta agendada.")
    else:
        for consulta in consultas_salvas:
            inicio = consulta.inicio.strftime("%H:%M")
            fim = consulta.fim.strftime("%H:%M")

            print(
                f"📅 Início: {inicio} | Fim: {fim} "
                f"| Paciente: {consulta.paciente_id}"
            )


if __name__ == "__main__":
    simular_dia_na_clinica()
