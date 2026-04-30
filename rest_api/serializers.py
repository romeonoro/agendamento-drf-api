# pylint: disable=abstract-method
from rest_framework import serializers  # type: ignore


class AgendamentoInputSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_nome = serializers.CharField(max_length=255)
    inicio = serializers.DateTimeField()


class AgendamentoOutputSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_nome = serializers.CharField()
    inicio = serializers.DateTimeField()
    duracao_minutos = serializers.IntegerField()
