# Tasks: Adequação do word_count_back ao Projeto B

**Input**: Design documents from `specs/001-adequacao-projeto-b/`

**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ ✅

**Organization**: Tasks agrupadas por user story para implementação e teste independentes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependências incompletas)
- **[Story]**: user story correspondente (US1–US7)

---

## Phase 1: Setup (Infraestrutura compartilhada)

**Purpose**: Preparar dependências, arquivos de configuração e estrutura de pastas antes de qualquer implementação.

- [x] T001 Adicionar `gunicorn`, `prometheus-flask-exporter`, `python-json-logger` em `requirements.txt`
- [x] T002 Criar `requirements-dev.txt` com `pytest-cov`, `flake8`, `Flake8-pyproject`
- [x] T003 [P] Criar `pyproject.toml` com seções `[tool.flake8]` (max-line-length=88, exclude=.git,__pycache__) e `[tool.pytest.ini_options]` (addopts = "--cov=app --cov-fail-under=80")
- [x] T004 [P] Criar `.env.example` com variáveis `FLASK_ENV`, `PORT=5000`, `MAX_TEXT_LENGTH=100000`, `LOG_LEVEL=INFO`
- [x] T005 [P] Verificar que `.env` está listado em `.gitignore`; adicionar se ausente

**Checkpoint**: dependências e configuração prontas — nenhum código de app ainda.

---

## Phase 2: Foundational (Pré-requisitos bloqueantes)

**Purpose**: Refatorar `app/` para SOLID e configurar infraestrutura transversal (logs, métricas) antes de qualquer rota nova.

**⚠️ CRITICAL**: nenhuma user story pode começar antes desta fase.

- [x] T006 Criar `app/counter.py` com função `count_words(text: str) -> int`: strip, split por whitespace, filtrar vazios, remover duplicatas, retornar len — comportamento idêntico ao atual de `app/main.py`
- [x] T007 Criar `app/validators.py` com função `validate_count_request(data: dict) -> str` que valida presença e tipo do campo `text` (deve ser str) e tamanho máximo de `MAX_TEXT_LENGTH` (lido de `os.environ`, padrão 100000); levanta `ValueError` com mensagem descritiva em cada caso de falha
- [x] T008 [P] Criar `app/logging_config.py` que configura `python-json-logger` no logger raiz com campos `level`, `route`, `status`, `duration`, `request_id`; expõe função `setup_logging()`
- [x] T009 [P] Criar `app/metrics.py` que inicializa `PrometheusMetrics` do `prometheus-flask-exporter`; expõe instância `metrics` para ser registrada no app
- [x] T010 Reescrever `app/__init__.py` como factory: função `create_app()` que instancia Flask, registra CORS, chama `setup_logging()`, registra `metrics`, e importa rotas de `app/routes.py`
- [x] T011 Reescrever `app/main.py` como ponto de entrada: `app = create_app()` — compatível com `gunicorn app.main:app`
- [x] T012 Atualizar `Dockerfile`: substituir `ENTRYPOINT flask --app app/main run --host "0.0.0.0"` por `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]`; adicionar `ENV FLASK_ENV=production PORT=5000`

**Checkpoint**: app sobe com `gunicorn app.main:app`, logs em JSON, `/metrics` responde.

---

## Phase 3: User Story 1 — Contar palavras via POST (Priority: P1) 🎯 MVP

**Goal**: `POST /count` aceita JSON `{"text": "..."}` e retorna `{"count": N}` com a mesma lógica de contagem já existente.

**Independent Test**: `curl -X POST http://localhost:5000/count -H "Content-Type: application/json" -d '{"text": "hello world"}'` retorna `{"count": 2}`.

- [x] T013 [US1] Criar `app/routes.py` com rota `POST /count`
- [x] T014 [US1] Adicionar rota `GET /count/` e `GET /count/<text>` em `app/routes.py`
- [x] T015 [US1] Adaptar `tests/tests_count_the_words.py` para importar `count_words` de `app.counter`
- [x] T016 [US1] Criar `tests/test_counter.py` com testes unitários de `count_words`

**Checkpoint**: `pytest tests/test_counter.py tests/tests_count_the_words.py` passa; `POST /count` responde corretamente.

---

## Phase 4: User Story 2 — Validação de entrada e respostas de erro (Priority: P2)

**Goal**: Clientes recebem 400 ou 413 com `{"error": "..."}` para entradas inválidas.

**Independent Test**: três `curl` com corpo ausente, `text` numérico e texto de 100 001 caracteres retornam 400, 400 e 413 respectivamente.

- [x] T017 [US2] Criar `tests/test_routes.py` com testes de integração via Flask test client
- [x] T018 [US2] Verificar `app/validators.py` e reativar `--cov-fail-under=80` em `pyproject.toml`

**Checkpoint**: `pytest tests/test_routes.py` passa; todos os casos de erro retornam o código e formato corretos.

---

## Phase 5: User Story 3 — GET depreciado mantido (Priority: P3)

**Goal**: `GET /count/<text>` continua funcionando e aparece como depreciado no OpenAPI.

**Independent Test**: `curl http://localhost:5000/count/hello` retorna `1`; OpenAPI marca o endpoint como `deprecated: true`.

- [x] T019 [P] [US3] Criar `docs/openapi.yaml` com OpenAPI 3.0
- [x] T020 [P] [US3] Criar `docs/adr/0001-decisao.md` no template MADR

**Checkpoint**: OpenAPI válido; ADR escrito; GET ainda responde corretamente.

---

## Phase 6: User Story 4 — Ambiente reproduzível com Docker Compose (Priority: P2)

**Goal**: `docker compose up` sobe a API; `--profile front` sobe API + front.

**Independent Test**: em máquina limpa com Docker, `docker compose up -d && curl http://localhost:5000/count/hello` retorna `1`.

- [x] T021 [US4] Criar `docker-compose.yml` com serviço `api`
- [x] T022 [US4] Adicionar serviço `front` com `profiles: [front]` em `docker-compose.yml`

**Checkpoint**: `docker compose up --build -d` sobe; `curl http://localhost:5000/count/hello` retorna `1`; `docker compose --profile front up` sobe os dois.

---

## Phase 7: User Story 5 — CI verde no GitHub Actions (Priority: P1)

**Goal**: todo push dispara lint, testes, coverage ≥ 80% e varredura de segredos; tudo verde.

**Independent Test**: push ao repositório → workflow passa todas as etapas sem erro.

- [ ] T023 [US5] Criar `.github/workflows/ci.yml` com jobs: `lint` (flake8 app/ tests/), `test` (pytest com --cov=app --cov-fail-under=80), `secrets-scan` (gitleaks/gitleaks-action@v2), `spectral` (stoplight/spectral-action@v0 em docs/openapi.yaml); jobs `lint` e `secrets-scan` em paralelo; `test` após `lint`; `spectral` após `test`
- [ ] T024 [US5] Remover `.travis.yml` do repositório
- [ ] T025 [US5] Atualizar badge do CI no `README.md` para apontar para o workflow do GitHub Actions

**Checkpoint**: push verde no GitHub; badge verde no README; sem referência ao Travis.

---

## Phase 8: User Story 6 — Observabilidade: logs, métricas e SLO (Priority: P3)

**Goal**: cada requisição gera log JSON; `/metrics` expõe histograma; `docs/desempenho.md` declara SLO com p95 medido.

**Independent Test**: `docker compose logs api | head -3` mostra JSON; `curl http://localhost:5000/metrics | grep flask_http` retorna histograma; `docs/desempenho.md` tem número real de p95.

- [ ] T026 [US6] Adicionar middleware em `app/__init__.py` (ou `app/routes.py`) que, após cada requisição, emite log JSON com campos: `level`, `route`, `status`, `duration_ms`, `request_id` (uuid gerado por requisição via `flask.g`)
- [ ] T027 [US6] Criar `tests/k6/smoke.js`: cenário com 10 VUs por 30s em `POST /count`, threshold `p(95) < 300`
- [ ] T028 [US6] Executar `k6 run tests/k6/smoke.js` com a API rodando via Compose; registrar resultado real de p95 em `docs/desempenho.md` com: ambiente (Docker local, python:3.9, gunicorn), comando exato, p95 medido, comparação com SLO de 300ms; ajustar valor do SLO se necessário

**Checkpoint**: logs JSON visíveis; `/metrics` responde; `docs/desempenho.md` tem números reais.

---

## Phase 9: User Story 7 — Documentação completa (Priority: P2)

**Goal**: README permite subir, testar e rodar k6 em ambiente limpo; todos os docs de entrega presentes.

**Independent Test**: seguir apenas o README em ambiente limpo → API sobe, testes passam, k6 roda.

- [ ] T029 [P] [US7] Reescrever `README.md`: primeira linha declara "Projeto B — Módulo 4"; seções: como subir com Compose, como rodar testes, como rodar lint, como rodar k6, badge do CI, link para ADR e OpenAPI
- [ ] T030 [P] [US7] Criar `CONTRIBUTORS.md` com nome da autora, lista de commits/PRs relevantes e descrição do que foi feito
- [ ] T031 [P] [US7] Criar `docs/ia.md` declarando os prompts de IA utilizados, decisões tomadas com base neles e o que foi revisado/ajustado manualmente

**Checkpoint**: README testado em ambiente limpo (clone novo ou container); todos os arquivos de entrega presentes.

---

## Phase 10: Polish & Fechamento

**Purpose**: validação final, limpeza e envio.

- [ ] T032 [P] Rodar `flake8 app/ tests/` localmente e corrigir eventuais erros remanescentes
- [ ] T033 [P] Rodar `pytest --cov=app --cov-fail-under=80` localmente e confirmar verde
- [ ] T034 Testar o README em ambiente limpo: clonar o repositório em diretório novo, seguir apenas o README, confirmar que API sobe, testes passam e k6 roda
- [ ] T035 Confirmar que nenhum segredo está no repositório (`git log --all` + gitleaks local)
- [ ] T036 Enviar link do repositório e link da execução verde do CI no Moodle até 13/11

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: sem dependências — começar imediatamente
- **Phase 2 (Foundational)**: depende de Phase 1 — bloqueia todas as user stories
- **Phase 3 (US1 POST)**: depende de Phase 2
- **Phase 4 (US2 Validação)**: depende de Phase 3 (usa `validate_count_request` e rotas)
- **Phase 5 (US3 GET depreciado)**: depende de Phase 2; pode rodar em paralelo com Phase 3
- **Phase 6 (US4 Compose)**: depende de Phase 2; pode rodar em paralelo com Phase 3
- **Phase 7 (US5 CI)**: depende de Phase 3 e 4 (testes precisam existir)
- **Phase 8 (US6 Observabilidade)**: depende de Phase 2 (logs/metrics já na factory); k6 depende de Phase 6
- **Phase 9 (US7 Docs)**: depende de todas as fases anteriores (ADR, OpenAPI, k6, p95)
- **Phase 10 (Polish)**: depende de todas as fases

### Parallel Opportunities

Após Phase 2 concluída, podem rodar em paralelo:
- Phase 3 + Phase 5 + Phase 6 (arquivos diferentes)
- T019 e T020 dentro de Phase 5 (OpenAPI e ADR são arquivos independentes)
- T029, T030, T031 dentro de Phase 9

---

## Parallel Example: após Phase 2

```
Phase 3 (US1): app/routes.py, tests/test_counter.py
Phase 5 (US3): docs/openapi.yaml, docs/adr/0001-decisao.md   ← paralelo com Phase 3
Phase 6 (US4): docker-compose.yml                            ← paralelo com Phase 3
```

---

## Implementation Strategy

### MVP (Phases 1–3 + 7)

1. Phase 1: Setup
2. Phase 2: Foundational
3. Phase 3: US1 — POST /count funcionando
4. Phase 7: CI verde
5. **PARAR e validar**: API responde, testes passam, CI verde

### Ordem recomendada para prazo de 4 dias

| Dia | Phases |
|-----|--------|
| Seg 09/11 | 1, 2, 7 (CI primeiro) |
| Ter 10/11 | 3, 4, 5, 6 |
| Qua 11/11 | 8 (parcial: logs + metrics), 9 (ADR, OpenAPI, README) |
| Qui 12/11 | 8 (k6 + desempenho.md), 9 (CONTRIBUTORS, ia.md) |
| Sex 13/11 | 10 (Polish + envio) |

---

## Notes

- [P] = arquivos diferentes, sem dependências incompletas
- Commit após cada fase ou task lógica
- Parar em cada checkpoint para validar antes de avançar
- `MAX_TEXT_LENGTH` lido de env em `validators.py` — não hardcoded
- O valor do SLO em `docs/desempenho.md` deve vir de medição real do k6 (T028), não estimado
