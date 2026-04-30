# Agendamento Médico MVP

Este é um MVP de um sistema de agendamento de consultas médicas desenvolvido com foco em rigor técnico, testabilidade e qualidade de código. O projeto utiliza os princípios de Clean Architecture e Test-Driven Development (TDD) para garantir uma base sólida e evolutiva.

## 🎯 Objetivo

O projeto foi desenvolvido como um desafio técnico para gerenciar turnos médicos e agendamentos de pacientes, garantindo que regras de negócio complexas — como antecedência de cancelamento e conflitos de horário — sejam respeitadas de forma resiliente.

## 🏗️ Arquitetura

A solução segue os princípios da Arquitetura Limpa, dividindo as responsabilidades em quatro camadas principais:

* **Core (Domain):** Contém as entidades (`Medico`, `Agendamento`) e as regras de negócio puras, sem dependências externas.
* **Application (Use Cases):** Orquestra o fluxo de dados, implementando casos de uso como `CriarAgendamento` e `CancelarAgendamento`.
* **Infra (Infrastructure):** Implementações concretas de persistência utilizando o ORM do Django e definições de interfaces (Repository Pattern).
* **Web (REST API):** Camada de interface externa construída com Django Rest Framework, responsável por Serializers e ViewSets.

> **Nota Técnica:** O projeto aplica Design by Contract e Encapsulamento rigoroso para prevenir estados inválidos no domínio.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.11
* **Framework Web:** Django & Django Rest Framework
* **Ambiente:** Windows
* **Qualidade:** Pylint, Mypy, Flake8, Black e Isort
* **Testes:** Pytest com Pytest-cov

## 🚀 Como Executar

O projeto utiliza um ambiente virtual e scripts de automação para facilitar o desenvolvimento.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/agendamento-mvp
   ```

2. **Crie e ative o virtualenv:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

## 🧪 Qualidade e Testes

A qualidade é monitorada continuamente através do script `check.ps1`. Atualmente, o projeto mantém:

* **Nota Pylint:** 10.00/10
* **Cobertura de Testes:** 94% (com 100% de cobertura no Core e Application)
* **Tipagem:** Verificação estrita com Mypy

Para rodar a bateria completa de verificações:
```powershell
.\check.ps1
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
