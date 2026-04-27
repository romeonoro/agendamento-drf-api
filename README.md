# Módulo de Agendamento Inteligente (MVP)

Este projeto é o núcleo (Core Domain) de uma API de agendamentos para clínicas. O objetivo principal é automatizar a validação de disponibilidade médica, reduzindo o tempo de marcação e eliminando completamente os conflitos de horários.

## 🚀 Tecnologias Utilizadas

O projeto foi desenhado com foco em isolamento de domínio. Por isso, as tecnologias são divididas entre o estado atual e a visão de futuro:

**Stack Atual (MVP):**
* **Linguagem:** Python 3.11 (Puro, sem frameworks externos no Core Domain).
* **Testes:** `unittest` (Biblioteca padrão do Python).
* **Qualidade de Código (Linters/Formatters):** `black`, `isort`, `flake8`.

**Roadmap Futuro (Camada de Adapters/API):**
* À medida que a aplicação evoluir para uma interface web completa, a infraestrutura será acoplada utilizando **Django** e **Django REST Framework (DRF)** para gerenciamento de rotas, banco de dados relacional e serialização de dados.

## 🏗️ Arquitetura e Padrões de Projeto

O desenvolvimento deste módulo segue rigorosos padrões de qualidade de engenharia de software:

* **Domain-Driven Design (DDD):** Isolamento completo das regras de negócio em um modelo de domínio rico. A classe `Medico` atua como Entidade Pura e guardiã de suas próprias regras (Invariantes).
* **Clean Architecture & Repository Pattern:** Separação estrita entre "Regras de Negócio" e "Persistência de Dados". O domínio desconhece a infraestrutura.
* **Test-Driven Development (TDD):** Todo o código de produção foi guiado por testes automatizados, garantindo cobertura total das regras de negócio antes da implementação.
* **Design by Contract (DbC):** As interações ocorrem através de contratos estritos. Se um contrato for quebrado, o sistema falha rapidamente (Fail-Fast) lançando exceções de domínio específicas.

## 📂 Estrutura do Projeto

O projeto adota uma estrutura limpa, separando o código de produção, infraestrutura e testes:

```text
agendamentos/
├── api/
│   ├── agendamento.py      # Domínio rico (Entidades Médico e Agendamento)
│   └── exceptions.py       # Exceções de domínio e contratos
├── docs/                   # Documentação arquitetural e diagramas do sistema
├── infra/
│   └── repository.py       # Adaptadores de persistência (Banco em Memória)
├── tests/
│   ├── test_agendamento.py # Testes unitários das regras de negócio (Domínio)
│   └── test_repository.py  # Testes unitários de persistência (Infraestrutura)
├── main.py                 # Orquestrador / Script de demonstração (MVP)
├── check.ps1               # Script utilitário para rodar linters, tipagem e testes
├── pyproject.toml          # Configurações unificadas de ferramentas (black, isort, pytest, mypy, pylint)
├── .pre-commit-config.yaml # Configuração dos hooks do Git (pre-commit)
├── .flake8                 # Configurações do linter (Ignora regras conflitantes com o Black)
├── .gitignore
├── requirements.txt        # Dependências de Produção (Atualmente vazio)
├── requirements-dev.txt    # Dependências de Desenvolvimento (Linters e Formatters)
└── README.md
```

## ⚙️ Como Executar o Projeto

Como o foco atual é o Core Domain, a aplicação roda via terminal para demonstrar a orquestração entre o Repositório e o Domínio.

1. **Clone o repositório** e acesse a pasta do projeto.
2. **Execute o script principal** de demonstração:
   ```bash
   python main.py
   ```

## 🧪 Como Rodar os Testes

O projeto conta com uma suíte automatizada que garante o funcionamento dos contratos e da persistência. Os testes estão divididos para respeitar as fronteiras da arquitetura (`test_agendamento.py` para o domínio e `test_repository.py` para a infraestrutura).

Você pode rodar os testes de duas maneiras:

**Opção 1: Usando `unittest` (Padrão do Python)**
Para buscar e rodar todos os testes de forma rápida usando a biblioteca padrão:
```bash
python -m unittest discover tests
```

**Opção 2: Usando `pytest` (Recomendado, com Cobertura)**
Para rodar os testes com saída aprimorada e relatório de cobertura de código (100% garantido), utilize o `pytest` (já configurado no `pyproject.toml`):
```bash
python -m pytest --cov
```

## 🛠️ Como Contribuir

Para manter a padronização e a qualidade do código, utilizamos ferramentas de formatação e análise estática.

1. **Crie e ative** o seu ambiente virtual (`.venv`).
2. **Instale as dependências** de desenvolvimento:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. **Antes de realizar um commit**, execute as seguintes ferramentas de linting para garantir que o código segue o padrão PEP8:
   * **Organize os imports**: `isort .`
   * **Formate o código**: `black .`
   * **Inspecione por erros**: `flake8 .`

## 📝 Observações para Code Review

Esta seção detalha as evoluções arquiteturais feitas neste MVP para facilitar o processo de revisão de código:

### 1. Separação de Responsabilidades (Repository Pattern)
* **Decisão**: A classe `Medico` teve seu estado interno de lista removido. O armazenamento de dados foi delegado para o `AgendamentoRepositorio` na camada de infra.
* **Porquê**: Aplicação estrita da Inversão de Dependência e SRP (Single Responsibility Principle). O Domínio (Médico) recebe os dados externos apenas para validar intersecções de tempo, garantindo que as regras de negócio permaneçam agnósticas a futuros bancos de dados (como PostgreSQL via Django).

### 2. Design by Contract (DbC)
* **Decisão**: Uso do padrão Fail-Fast com exceções personalizadas (`ForaDoHorarioError`, `ConflitoHorarioError`, `IntervaloInvalidoError`).
* **Porquê**: O código valida as pré-condições antes de aprovar a devolução da Entidade para o banco de dados. Isso garante que o sistema nunca entre em um estado inválido.

### 3. Dados Derivados
* **Decisão**: A propriedade `fim` do agendamento não é construída diretamente na instanciação, mas calculada dinamicamente.
* **Porquê**: Evita a inconsistência de dados. Ao armazenar apenas `inicio` e `duracao`, garantimos que o horário de término seja sempre a "fonte única da verdade".

### 4. Tipagem Estática (Type Hinting)
* **Decisão**: Uso rigoroso de tipos em todos os métodos e atributos.
* **Porquê**: Melhora a legibilidade e previne erros comuns de passagem de parâmetros durante o desenvolvimento e integração com o Repositório.
