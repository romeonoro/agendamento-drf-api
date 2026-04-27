import unittest
from datetime import datetime, time

from api.agendamento import Agendamento, Medico
from api.exceptions import (
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
)


class TestAgendamento(unittest.TestCase):

    def test_agendamento_com_sucesso(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )

        horario_desejado = datetime(2026, 4, 24, 9, 0)
        paciente_id = 123

        agendamento_criado = medico.agendar(
            paciente_id=paciente_id,
            data_hora=horario_desejado,
            agendamentos_existentes=[],
        )

        self.assertEqual(agendamento_criado.inicio, horario_desejado)
        self.assertEqual(agendamento_criado.paciente_id, paciente_id)
        self.assertEqual(agendamento_criado.fim, datetime(2026, 4, 24, 9, 30))

    def test_erro_agendamento_fora_do_horario(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )

        horario_desejado = datetime(2026, 4, 25, 14, 0)
        paciente_id = 123

        with self.assertRaisesRegex(
            ForaDoHorarioError, "Médico não está disponível neste horário"
        ):
            medico.agendar(
                paciente_id=paciente_id,
                data_hora=horario_desejado,
                agendamentos_existentes=[],
            )

    def test_erro_conflito_de_horario(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        horario_existente = datetime(2026, 4, 25, 10, 0)

        consulta_no_banco = Agendamento(
            paciente_id=123, inicio=horario_existente, duracao_minutos=30
        )
        lista_do_repositorio = [consulta_no_banco]

        horario_conflitante = datetime(2026, 4, 25, 10, 0)
        paciente_id_2 = 456

        with self.assertRaisesRegex(ConflitoHorarioError, "Conflito de Horário"):
            medico.agendar(
                paciente_id=paciente_id_2,
                data_hora=horario_conflitante,
                agendamentos_existentes=lista_do_repositorio,
            )

    def test_deve_bloquear_consulta_que_termina_apos_fim_do_turno(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(11, 45),
            intervalo_atendimento=30,
        )

        horario_limite = datetime(2026, 4, 25, 11, 30)

        with self.assertRaises(ForaDoHorarioError):
            medico.agendar(
                paciente_id=888, data_hora=horario_limite, agendamentos_existentes=[]
            )

    def test_deve_bloquear_horario_quebrado_fora_do_intervalo(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )

        horario_quebrado = datetime(2026, 4, 25, 10, 7)

        with self.assertRaises(IntervaloInvalidoError):
            medico.agendar(
                paciente_id=123, data_hora=horario_quebrado, agendamentos_existentes=[]
            )

    def test_propriedade_nome_do_medico(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        self.assertEqual(medico.nome, "Dr. House")
