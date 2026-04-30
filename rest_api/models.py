from django.db import models  # type: ignore


class AgendamentoModel(models.Model):
    # Usando os campos exatos que a sua entidade precisa
    paciente_id = models.IntegerField()
    medico_nome = models.CharField(max_length=255)
    inicio = models.DateTimeField()
    duracao_minutos = models.IntegerField()
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "agendamentos"
