# Implementation Plan: Adequação do word_count_back ao Projeto B

**Branch**: `001-adequacao-projeto-b` | **Date**: 2026-11-09 | **Spec**: [spec.md](spec.md)

## Summary

Adequar a API Flask `word_count_back` ao Projeto B do Módulo 4, adicionando `POST /count` com validação, refatorando `app/` para SOLID com Service Layer, configurando Docker Compose, migrando CI para GitHub Actions, adicionando logs estruturados, métricas Prometheus e documentação completa (ADR, OpenAPI, k6, README).

## Technical Context

**Language/Version**: Python 3.9 (mantido)

**Primary Dependencies**: Flask 2.2.3, Flask-Cors 3.0.10, gunicorn (novo), prometheus-flask-exporter (novo), python-json-logger (novo), flake8 + Flake8-pyproject (novo)

**Storage**: N/A

**Testing**: pytest 7.2.1, coverage 7.1.0, pytest-cov (novo), k6 (smoke test)

**Target Platform**: Linux (container Docker, python:3.9)

**Project Type**: web-service (API REST)

**Performance Goals**: p95 ≤ 300ms para `POST /count` (SLO a calibrar com k6)

**Constraints**: Python 3.9 e imagem base existentes mantidos; sem banco de dados; sem autenticação

**Scale/Scope**: API single-endpoint, uso acadêmico, demonstração local + CI

## Constitution Check

A `constitution.md` está no template padrão (não preenchida). Sem princípios de governança definidos — nenhuma gate violation a registrar.

Checklist de qualidade aplicado:
- [x] Spec completa e validada antes do plan
- [x] Sem NEEDS CLARIFICATION pendentes
- [x] Decisões técnicas documentadas em `research.md`
- [x] Escopo delimitado (sem banco, sem auth, sem migração de versão Python)

## Project Structure

### Documentation (this feature)

```text
specs/001-adequacao-projeto-b/
├── plan.md              ← este arquivo
├── research.md          ← decisões técnicas resolvidas
├── data-model.md        ← entidades, regras de validação, módulos
├── quickstart.md        ← guia de validação end-to-end
├── contracts/
│   └── api-contract.md  ← contrato dos endpoints
└── tasks.md             ← gerado pelo /speckit-tasks (próximo passo)
```

### Source Code (repository root)

```text
word_count_back/
├── docker-compose.yml        ← novo
├── Dockerfile                ← modificar: gunicorn, ENV
├── README.md                 ← modificar: nível, Compose, testes, k6
├── CONTRIBUTORS.md           ← novo
├── .env.example              ← novo
├── pyproject.toml            ← novo: flake8, pytest, coverage mínimo 80%
├── requirements.txt          ← modificar: adicionar gunicorn, prometheus-flask-exporter, python-json-logger
├── requirements-dev.txt      ← novo: pytest-cov, flake8, Flake8-pyproject
├── app/
│   ├── __init__.py           ← modificar: criar factory do app
│   ├── counter.py            ← novo: Service Layer (count_words)
│   ├── validators.py         ← novo: validação de entrada
│   ├── routes.py             ← novo: GET depreciado + POST /count
│   ├── logging_config.py     ← novo: python-json-logger
│   ├── metrics.py            ← novo: prometheus-flask-exporter
│   └── main.py               ← modificar: ponto de entrada para gunicorn
├── tests/
│   ├── __init__.py
│   ├── test_counter.py       ← novo: testes unitários do Service Layer
│   ├── test_routes.py        ← novo: testes de integração via Flask test client
│   ├── tests_count_the_words.py ← modificar: adaptar para novo módulo
│   └── k6/
│       └── smoke.js          ← novo: smoke test k6
├── docs/
│   ├── adr/
│   │   └── 0001-decisao.md   ← novo: MADR POST vs GET
│   ├── openapi.yaml          ← novo: validado com Spectral
│   ├── desempenho.md         ← novo: SLO + p95 medido
│   └── ia.md                 ← novo: declaração de prompts de IA
└── .github/
    └── workflows/
        └── ci.yml            ← novo: lint, test, coverage, gitleaks, Spectral
```

**Structure Decision**: single project com separação de módulos dentro de `app/`. Sem Blueprint (overhead desnecessário para 2 rotas). Service Layer em `counter.py` é o único pattern registrado (M1-05).
