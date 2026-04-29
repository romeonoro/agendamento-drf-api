from datetime import time

from rest_framework import status, viewsets
from rest_framework.response import Response

from core.agendamento import Medico
from core.exceptions import (
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
)
from infra.django_repository import DjangoAgendamentoRepository

from .serializers import AgendamentoInputSerializer, AgendamentoOutputSerializer


class AgendamentoViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = AgendamentoInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dados = serializer.validated_data
        repo = DjangoAgendamentoRepository()

        # 1. MONTANDO O MÉDICO
        medico = Medico(
            nome=dados["medico_nome"],
            inicio_turno=time(8, 0),
            fim_turno=time(18, 0),
            intervalo_atendimento=30,
        )

        # 2. BUSCANDO O CONTEXTO PARA A REGRA DE NEGÓCIO
        # Precisamos saber a agenda do dia para o médico não encavalar horários
        data_do_agendamento = dados["inicio"].date()
        existentes = repo.buscar_por_medico_e_data(medico.nome, data_do_agendamento)

        try:
            # 3. EXECUTANDO O CORE (A sua classe assume o controle aqui!)
            novo_agendamento = medico.agendar(
                paciente_id=dados["paciente_id"],
                data_hora=dados["inicio"],
                agendamentos_existentes=existentes,
            )

            # 4. SALVANDO E RETORNANDO
            repo.salvar(novo_agendamento, medico.nome)
            return Response(
                {"mensagem": "Agendamento criado!"}, status=status.HTTP_201_CREATED
            )

        # Tratamento das suas exceções customizadas
        except IntervaloInvalidoError:
            return Response(
                {"erro": "Os agendamentos devem ser a cada 30 minutos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ForaDoHorarioError:
            return Response(
                {"erro": "Horário fora do turno de trabalho do médico."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ConflitoHorarioError:
            return Response(
                {"erro": "O médico já possui paciente neste horário."},
                status=status.HTTP_409_CONFLICT,
            )

    def list(self, request):
        """
        Endpoint para listar todos os agendamentos (GET /agendamentos/)
        """
        repo = DjangoAgendamentoRepository()
        dados_brutos = repo.listar_todos()
        serializer = AgendamentoOutputSerializer(dados_brutos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
