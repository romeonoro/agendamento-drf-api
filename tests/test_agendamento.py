import unittest
from datetime import datetime, time, timedelta

from core.agendamento import Agendamento, Medico
from core.exceptions import (
    CancelamentoInvalidoError,
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
    MedicoNaoEncontradoError,
    PacienteNaoEncontradoError,
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

    def test_deve_retornar_duracao_minutos_corretamente(self) -> None:
        agendamento = Agendamento(
            paciente_id=1, inicio=datetime.now(), duracao_minutos=45
        )
        self.assertEqual(agendamento.duracao_minutos, 45)

    def test_nao_deve_cancelar_agendamento_de_outro_paciente(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        horario_existente = datetime(2026, 4, 25, 10, 0)

        # Agendamento pertence ao paciente 123
        consulta_no_banco = Agendamento(
            paciente_id=123, inicio=horario_existente, duracao_minutos=30
        )
        lista_do_repositorio = [consulta_no_banco]

        horario_cancelado = datetime(2026, 4, 25, 10, 0)
        paciente_invalido_id = 456

        # Tenta cancelar passando o ID 456 (deve falhar)
        with self.assertRaisesRegex(
            CancelamentoInvalidoError, "Não é possível cancelar este agendamento"
        ):
            medico.cancelar(
                paciente_id=paciente_invalido_id,
                data_hora=horario_cancelado,
                agendamentos_existentes=lista_do_repositorio,
            )

    def test_cancelamento_de_agendamento_com_sucesso(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        horario_da_consulta = datetime(2026, 4, 25, 10, 0)

        # O momento em que o paciente liga para cancelar (2 dias antes da consulta)
        momento_do_cancelamento = datetime(2026, 4, 23, 10, 0)

        consulta_no_banco = Agendamento(
            paciente_id=123, inicio=horario_da_consulta, duracao_minutos=30
        )

        # Simulamos que a consulta está ativa e retornou do banco
        lista_do_repositorio = [consulta_no_banco]

        # Act: Cancela com antecedência válida e IDs corretos
        medico.cancelar(
            paciente_id=123,
            data_hora=horario_da_consulta,
            agendamentos_existentes=lista_do_repositorio,
            data_hora_atual=momento_do_cancelamento,  # Passando o tempo controlado
        )

        # Assert: A consulta dentro da lista deve estar com status inativo/cancelado
        self.assertFalse(consulta_no_banco.ativo)

    def test_excecao_paciente_nao_encontrado_gera_mensagem_correta(self) -> None:
        erro = PacienteNaoEncontradoError(paciente_id=99)
        self.assertEqual(str(erro), "Nenhuma consulta encontrada para o Paciente 99.")

    def test_excecao_medico_nao_encontrado_gera_mensagem_correta(self) -> None:
        erro = MedicoNaoEncontradoError(medico_id=88)
        self.assertEqual(str(erro), "Nenhuma consulta encontrada para o Médico 88.")

    def test_deve_usar_data_atual_se_nenhuma_for_fornecida_ao_cancelar(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        # Cria uma consulta para daqui a 30 dias para não barrar na regra de 24h
        data_futura = datetime.now() + timedelta(days=30)
        consulta = Agendamento(paciente_id=1, inicio=data_futura, duracao_minutos=30)

        # Act: Cancela sem passar o data_hora_atual
        medico.cancelar(
            paciente_id=1, data_hora=data_futura, agendamentos_existentes=[consulta]
        )

        self.assertFalse(consulta.ativo)

    def test_nao_deve_cancelar_se_agendamento_nao_estiver_na_lista(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        horario_buscado = datetime(2026, 4, 25, 10, 0)

        # Act & Assert: Passa uma lista vazia, simulando que o agendamento não existe
        with self.assertRaisesRegex(
            CancelamentoInvalidoError,
            "Nenhum agendamento ativo encontrado neste horário.",
        ):
            medico.cancelar(
                paciente_id=1, data_hora=horario_buscado, agendamentos_existentes=[]
            )

    def test_nao_deve_cancelar_agendamento_com_antecedencia_menor_que_24h(self) -> None:
        medico = Medico(
            nome="Dr. House",
            inicio_turno=time(8, 0),
            fim_turno=time(12, 0),
            intervalo_atendimento=30,
        )
        # Consulta marcada
        horario_da_consulta = datetime(2026, 4, 25, 10, 0)
        consulta_no_banco = Agendamento(
            paciente_id=1, inicio=horario_da_consulta, duracao_minutos=30
        )

        # Paciente tenta cancelar apenas 10 horas antes da consulta
        momento_do_cancelamento = datetime(2026, 4, 25, 0, 0)

        # Act & Assert: O domínio deve barrar o cancelamento tardio
        with self.assertRaisesRegex(
            CancelamentoInvalidoError,
            "Cancelamentos só são permitidos com 24 horas de antecedência",
        ):
            medico.cancelar(
                paciente_id=1,
                data_hora=horario_da_consulta,
                agendamentos_existentes=[consulta_no_banco],
                data_hora_atual=momento_do_cancelamento,
            )
