from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from application.use_cases import CancelarAgendamentoUseCase, CriarAgendamentoUseCase
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

        # 1. Instancia o repositório e injeta no Caso de Uso
        repositorio = DjangoAgendamentoRepository()
        use_case = CriarAgendamentoUseCase(repositorio=repositorio)

        try:
            # 2. A View apenas manda o Caso de Uso agir
            use_case.execute(paciente_id=dados["paciente_id"], inicio=dados["inicio"])

            return Response(
                {"mensagem": "Agendamento criado!"}, status=status.HTTP_201_CREATED
            )

        # 3. Tratamento das exceções traduzindo para HTTP
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

        # 1. Instancia o repositório concreto (Infra)
        repositorio = DjangoAgendamentoRepository()

        # 2. Injeta o repositório no Caso de Uso (Aplicação)
        use_case = CancelarAgendamentoUseCase(repositorio=repositorio)

        try:
            # 3. A View apenas manda o Caso de Uso executar a ação
            use_case.execute(agendamento_id=int(pk), paciente_id=int(paciente_id))

            return Response(
                {"mensagem": "Agendamento cancelado com sucesso."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            # Captura o erro do Use Case de "não encontrado"
            return Response({"erro": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except CancelamentoInvalidoError as e:
            # Captura as regras de negócio quebradas pelo Core
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
