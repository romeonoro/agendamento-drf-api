from datetime import time

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.agendamento import Medico
from core.exceptions import (
    CancelamentoInvalidoError,
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

        medico = Medico(
            nome="Dr. Sistema",
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

    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        paciente_id = request.data.get("paciente_id")

        if not paciente_id:
            return Response(
                {"erro": "O campo paciente_id é obrigatório no corpo da requisição."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Instancia o repositório aqui e busca a entidade
        repositorio = DjangoAgendamentoRepository()
        agendamento_core = repositorio.buscar_por_id(pk)

        if not agendamento_core:
            return Response(
                {"erro": "Agendamento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        medico = Medico(
            nome="Dr. Sistema",
            inicio_turno=time(8, 0),
            fim_turno=time(18, 0),
            intervalo_atendimento=30,
        )

        agendamentos_do_medico = [agendamento_core]

        try:
            # 3. EXECUTAR A REGRA DE NEGÓCIO
            medico.cancelar(
                paciente_id=int(paciente_id),
                data_hora=agendamento_core.inicio,
                agendamentos_existentes=agendamentos_do_medico,
                data_hora_atual=timezone.now(),
            )

            # 4. PERSISTIR A MUDANÇA
            repositorio.atualizar(agendamento_core)

            return Response(
                {"mensagem": "Agendamento cancelado com sucesso."},
                status=status.HTTP_200_OK,
            )

        except CancelamentoInvalidoError as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(
                {"erro": "Ocorreu um erro inesperado ao processar o cancelamento."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        """
        Endpoint para listar todos os agendamentos (GET /agendamentos/)
        """
        repo = DjangoAgendamentoRepository()
        dados_brutos = repo.listar_todos()
        serializer = AgendamentoOutputSerializer(dados_brutos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
