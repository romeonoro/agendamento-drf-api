# Módulo de Agendamento Inteligente (MVP)

Este projeto é o núcleo (Core Domain) de uma API de agendamentos para clínicas. O objetivo principal é automatizar a validação de disponibilidade médica, reduzindo o tempo de marcação e eliminando completamente os conflitos de horários.

## 🏗️ Arquitetura e Padrões de Projeto

O desenvolvimento deste módulo segue rigorosos padrões de qualidade de engenharia de software:

* **Domain-Driven Design (DDD):** Isolamento completo das regras de negócio em um modelo de domínio rico. A classe `Medico` é a guardiã de suas próprias regras (Invariantes).
* **Test-Driven Development (TDD):** Todo o código de produção foi guiado por testes automatizados, garantindo cobertura total das regras de negócio antes da implementação.
* **Design by Contract (DbC):** As interações ocorrem através de contratos estritos (Pré-condições e Pós-condições). Se um contrato for quebrado, o sistema falha rapidamente (Fail-Fast) lançando exceções de domínio específicas.

## 📂 Estrutura do Projeto

O projeto adota uma estrutura limpa, separando o código de produção do código de testes:

```text
agendamentos/
├── api/
│   ├── agendamento.py      # Domínio rico e contratos (Médico, Agendamento)
├── tests/
│   └── test_agendamento.py # Suíte de testes unitários (Cenários de Aceitação)
├── .gitignore               
├── requirements.txt               
└── README.md
```

## ⚙️ Regras de Negócio Implementadas (Contratos)

As seguintes regras foram blindadas no domínio através de testes unitários:

*   **RF01 - Configuração de Grade:** Permite definir o horário de início, fim do turno do médico e o intervalo padrão de atendimento.
*   **RF02 - Validação de Horário (Pré-condição):** O sistema rejeita o agendamento (`ForaDoHorarioError`) se o horário solicitado estiver fora do turno de trabalho do médico.
*   **RF03 - Prevenção de Sobreposição (Pré-condição):** O sistema impede (`ConflitoHorarioError`) dois agendamentos no mesmo horário ou sobrepostos para o mesmo médico.
*   **RF04 - Duração Fixa:** Cada consulta possui uma duração padrão em minutos, parametrizável na criação do médico.
