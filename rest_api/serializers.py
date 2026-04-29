from rest_framework import serializers


class AgendamentoInputSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_nome = serializers.CharField(max_length=255)
    inicio = serializers.DateTimeField()
