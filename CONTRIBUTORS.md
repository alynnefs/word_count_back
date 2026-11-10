# Contributors

## Alynne Ferreira (@alynnefs)

Autora e responsável por todas as modificações deste projeto.

### O que foi feito

- Refatoração de `app/` para SOLID: separação em `counter.py`, `validators.py`, `routes.py`, `logging_config.py`, `metrics.py`
- Adição de `POST /count` com validação de entrada (400/413)
- Manutenção do `GET /count/<text>` como depreciado
- Configuração do gunicorn como servidor de produção (4 workers)
- Criação do `docker-compose.yml` com healthcheck e perfil opcional para o front
- Migração do CI de Travis para GitHub Actions (lint, test, coverage, gitleaks, Spectral)
- Logs estruturados em JSON por requisição (request_id, route, status, duration_ms)
- Métricas Prometheus expostas em `/metrics`
- ADR 0001 (MADR): decisão POST vs GET
- OpenAPI 3.0 validado com Spectral
- Smoke test k6 com threshold p95 < 300ms
- Relatório de desempenho com p95 medido (5.53ms)
- Documentação completa no README
