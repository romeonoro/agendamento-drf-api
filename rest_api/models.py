from django.db import models


class AgendamentoModel(models.Model):
    # Usando os campos exatos que a sua entidade precisa
    paciente_id = models.IntegerField()
    medico_nome = models.CharField(max_length=255)
    inicio = models.DateTimeField()
    duracao_minutos = models.IntegerField()

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agendamentos"
