class ForaDoHorarioError(Exception):
    def __init__(
        self, message: str = "Médico não está disponível neste horário."
    ) -> None:
        super().__init__(message)


class ConflitoHorarioError(Exception):
    def __init__(self, message: str = "Conflito de Horário.") -> None:
        super().__init__(message)


class IntervaloInvalidoError(Exception):
    def __init__(
        self, message: str = "O horário deve respeitar a grade de intervalos."
    ) -> None:
        super().__init__(message)


class AgendamentoNaoEncontradoError(Exception):
    def __init__(self, paciente_id: int) -> None:
        mensagem = f"Nenhuma consulta encontrada para o Paciente {paciente_id}."
        super().__init__(mensagem)
