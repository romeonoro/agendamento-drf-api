from rest_framework import serializers


class AgendamentoInputSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_nome = serializers.CharField(max_length=255)
    inicio = serializers.DateTimeField()


class AgendamentoOutputSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_nome = serializers.CharField()
    inicio = serializers.DateTimeField()
    duracao_minutos = serializers.IntegerField()
