from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from core.agendamento import Agendamento


class AgendamentoRepositorio(ABC):
    @abstractmethod
    def buscar_por_id(self, agendamento_id: int) -> Optional[Agendamento]:
        """Busca um agendamento pelo ID. Retorna None se não encontrar."""

    @abstractmethod
    def atualizar(self, agendamento: Agendamento) -> None:
        """Atualiza os dados de um agendamento existente."""

    @abstractmethod
    def listar_todos(self) -> List[Agendamento]:
        """Retorna todos os agendamentos cadastrados."""

    @abstractmethod
    def buscar_por_medico_e_data(
        self, medico_nome: str, data: date
    ) -> List[Agendamento]:
        """Busca agendamentos de um médico específico em uma data específica."""

    @abstractmethod
    def salvar(self, agendamento: Agendamento, medico_nome: str) -> None:
        """Persiste um novo agendamento no sistema."""
