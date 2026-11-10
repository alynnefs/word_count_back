# Declaração de uso de IA

Este documento declara os prompts e interações com ferramentas de IA que contribuíram para o desenvolvimento deste projeto, conforme exigido pelo Projeto B do Módulo 4.

## Ferramenta utilizada

Amazon Q Developer (via plugin no VS Code / IDE).

## Prompts que importaram

### Planejamento e especificação

- Geração da RFC-001 com checklist de entregáveis mapeados para a rubrica
- Execução do fluxo speckit (`/speckit-specify`, `/speckit-plan`, `/speckit-tasks`) para gerar spec, plano e tasks a partir da RFC
- Decisões técnicas documentadas em `specs/001-adequacao-projeto-b/research.md`

### Implementação

- Refatoração de `app/` para SOLID (separação de counter, validators, routes, factory)
- Implementação do `POST /count` com validação e respostas de erro padronizadas
- Configuração do gunicorn, logging JSON e prometheus-flask-exporter
- Criação do `docker-compose.yml` com healthcheck e profile opcional
- Criação do workflow de CI no GitHub Actions
- Correções de compatibilidade (Werkzeug, ubuntu-22.04, Spectral CLI)
- Smoke test k6 e relatório de desempenho

## Decisões que continuam sendo minhas

- Escolha do Service Layer como pattern (em vez de Strategy)
- Manter o GET depreciado em vez de remover (decisão documentada no ADR 0001)
- Valor do SLO (300ms p95) calibrado com medição real
- Escolha de 4 workers no gunicorn após identificar falhas com 1 worker
- Revisão e validação de todo o código gerado antes de commitar

## O que foi revisado manualmente

Todo o código gerado foi lido, testado localmente e ajustado antes de cada commit. Os testes foram executados localmente (`pytest`) e no CI antes de mergear cada PR.
