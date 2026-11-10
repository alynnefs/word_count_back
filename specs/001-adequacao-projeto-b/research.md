# Research: Adequação do word_count_back ao Projeto B

**Date**: 2026-11-09 | **Branch**: `001-adequacao-projeto-b`

## 1. Servidor de produção: gunicorn vs Flask dev server

- **Decision**: gunicorn
- **Rationale**: O servidor de desenvolvimento do Flask não é thread-safe e não é adequado para medição de desempenho real. O gunicorn é o padrão para APIs Flask em produção, compatível com Python 3.9 e sem conflitos com as dependências existentes.
- **Alternatives considered**: waitress (Windows-friendly, mas desnecessário aqui), uvicorn (ASGI, requer migração para async — fora do escopo).

## 2. Estrutura da app: separação de responsabilidades (SOLID / M1-04)

- **Decision**: separar em três módulos dentro de `app/`: `counter.py` (regra de negócio pura), `validators.py` (validação de entrada), `routes.py` (rotas Flask). `main.py` passa a ser o ponto de entrada que monta o app.
- **Rationale**: A regra de contagem atual está acoplada à rota. Separar permite testar `counter.py` sem subir o Flask, atendendo M1-04 e facilitando o pattern do M1-05.
- **Alternatives considered**: manter tudo em `main.py` (não atende SOLID); usar Blueprint (overhead desnecessário para uma API com 2 rotas).

## 3. Design pattern (M1-05): Service Layer

- **Decision**: Service Layer — `counter.py` expõe uma função `count_words(text: str) -> int` que encapsula toda a lógica de contagem. As rotas chamam esse serviço.
- **Rationale**: É o pattern mais simples que atende o critério: a regra de negócio fica isolada, testável e reutilizável pelas duas rotas (GET e POST). Strategy seria adequado se houvesse múltiplos algoritmos de contagem — não é o caso.
- **Alternatives considered**: Strategy (desnecessário com um único algoritmo), Repository (não há persistência).

## 4. Comportamento da contagem: palavras únicas vs todas as palavras

- **Decision**: manter o comportamento atual — conta palavras únicas (remove duplicatas).
- **Rationale**: O comportamento já está documentado nos testes existentes (`test_duplicate_word`: "hello word word" → 2). Mudar quebraria os testes e o contrato com o front.
- **Alternatives considered**: contar todas as ocorrências (mudaria o contrato existente — descartado).

## 5. Logs estruturados: biblioteca

- **Decision**: `python-json-logger` (pacote `pythonjsonlogger`)
- **Rationale**: Integra com o módulo `logging` padrão do Python sem dependências pesadas. Produz JSON com campos customizáveis. Compatível com Python 3.9.
- **Alternatives considered**: `structlog` (mais poderoso, mas mais complexo para o escopo); logging manual com `json.dumps` (frágil).

## 6. Métricas: biblioteca

- **Decision**: `prometheus-flask-exporter`
- **Rationale**: Expõe `/metrics` automaticamente com histogramas de latência por rota, sem código adicional além da inicialização. Compatível com Flask 2.x e Python 3.9.
- **Alternatives considered**: `prometheus_client` puro (requer mais código manual); OpenTelemetry (overhead de setup para o escopo do projeto).

## 7. Linter: ferramenta

- **Decision**: `flake8` configurado via `pyproject.toml` (via `flake8` + `Flake8-pyproject` ou via `setup.cfg`). Como `pyproject.toml` é o arquivo alvo do M1-06, usar `[tool.flake8]` com `Flake8-pyproject`.
- **Rationale**: `black` já está no `requirements.txt` para formatação. `flake8` complementa com verificação de estilo e erros. Alternativa `ruff` é mais moderna mas pode ter conflitos com Python 3.9 em algumas configurações — flake8 é mais seguro.
- **Alternatives considered**: `ruff` (mais rápido, mas menos testado com o stack existente); `pylint` (muito verboso para o escopo).

## 8. Varredura de segredos: gitleaks

- **Decision**: `gitleaks` via action `gitleaks/gitleaks-action` no CI.
- **Rationale**: Integração direta com GitHub Actions, sem instalação manual. Varre o histórico completo na primeira execução.
- **Alternatives considered**: `truffleHog` (mais complexo de configurar); `detect-secrets` (requer baseline manual).

## 9. OpenAPI: validação com Spectral

- **Decision**: `stoplight/spectral-action` no CI para validar `docs/openapi.yaml`.
- **Rationale**: Action oficial do Spectral, sem instalação local obrigatória. Valida contra o ruleset padrão OAS.
- **Alternatives considered**: validação local com `spectral-cli` (requer Node.js instalado — adiciona dependência ao ambiente).

## 10. Formato de erro padronizado

- **Decision**: `{"error": "<mensagem descritiva>"}` com o código HTTP correspondente.
- **Rationale**: Simples, consistente e fácil de documentar no OpenAPI. Não há necessidade de campos adicionais (código de erro interno, stack trace) para o escopo do projeto.
