# Feature Specification: Adequação do word_count_back ao Projeto B

**Feature Branch**: `001-adequacao-projeto-b`

**Created**: 2026-11-09

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Contar palavras via POST (Priority: P1)

Um desenvolvedor ou avaliador envia um texto em formato JSON para a API e recebe a contagem de palavras, sem depender de codificação de URL ou limite de tamanho de path.

**Why this priority**: É o núcleo funcional da API e base para todos os outros entregáveis (testes, ADR, OpenAPI, k6).

**Independent Test**: Pode ser testado com um `curl -X POST /count -d '{"text": "hello world"}'` e deve retornar `{"count": 2}`.

**Acceptance Scenarios**:

1. **Given** um texto válido no corpo JSON, **When** `POST /count` é chamado, **Then** retorna 200 com a contagem correta de palavras.
2. **Given** um texto com espaços múltiplos ou nas bordas, **When** `POST /count` é chamado, **Then** a contagem não é afetada pelos espaços extras.
3. **Given** um texto com acentos ou quebras de linha, **When** `POST /count` é chamado, **Then** a contagem é correta.
4. **Given** texto vazio `""`, **When** `POST /count` é chamado, **Then** retorna `{"count": 0}`.

---

### User Story 2 — Validação de entrada e respostas de erro (Priority: P2)

Um cliente da API recebe respostas de erro claras e padronizadas quando envia dados inválidos.

**Why this priority**: Sem validação, a API pode falhar silenciosamente ou retornar erros genéricos, dificultando a integração e os testes.

**Independent Test**: Pode ser testado enviando corpo ausente, campo não textual e texto acima do limite; cada caso deve retornar o código HTTP correto com mensagem de erro no formato documentado.

**Acceptance Scenarios**:

1. **Given** corpo ausente ou malformado, **When** `POST /count` é chamado, **Then** retorna 400 com mensagem de erro padronizada.
2. **Given** campo `text` com valor não textual (ex.: número, lista), **When** `POST /count` é chamado, **Then** retorna 400.
3. **Given** texto acima de 100 000 caracteres, **When** `POST /count` é chamado, **Then** retorna 413.

---

### User Story 3 — Endpoint GET depreciado mantido (Priority: P3)

O front-end existente continua funcionando sem alterações enquanto não migra para o POST.

**Why this priority**: Evita quebrar o front durante o período de transição, sem custo de manutenção adicional.

**Independent Test**: `GET /count/<texto>` retorna a mesma contagem que `POST /count` para o mesmo texto.

**Acceptance Scenarios**:

1. **Given** o mesmo texto, **When** chamado via `GET /count/<texto>` e via `POST /count`, **Then** ambos retornam a mesma contagem.
2. **Given** a documentação OpenAPI, **When** consultada, **Then** o GET aparece marcado como depreciado.

---

### User Story 4 — Ambiente reproduzível com Docker Compose (Priority: P2)

Qualquer pessoa consegue subir a API localmente com um único comando, sem instalar Python ou dependências manualmente.

**Why this priority**: Critério direto da rubrica (M1) e pré-requisito para o teste do README em ambiente limpo.

**Independent Test**: Em uma máquina limpa com Docker, `docker compose up` sobe a API e um `curl` retorna resposta válida.

**Acceptance Scenarios**:

1. **Given** Docker instalado, **When** `docker compose up` é executado, **Then** a API responde na porta 5000.
2. **Given** `--profile front`, **When** `docker compose up --profile front` é executado, **Then** API e front sobem juntos.
3. **Given** variáveis de ambiente no `.env`, **When** a API sobe, **Then** lê a configuração do ambiente corretamente.

---

### User Story 5 — CI verde no GitHub Actions (Priority: P1)

Todo commit passa por lint, testes e verificação de cobertura automaticamente, com resultado visível no repositório.

**Why this priority**: Critério direto da rubrica (M2 e M3); sem CI verde o projeto não está completo.

**Independent Test**: Um push ao repositório dispara o workflow e todas as etapas passam (lint, test, coverage ≥ 80%).

**Acceptance Scenarios**:

1. **Given** um push ao repositório, **When** o workflow do Actions executa, **Then** lint, testes e coverage passam.
2. **Given** cobertura abaixo de 80%, **When** o CI executa, **Then** o workflow falha com mensagem clara.
3. **Given** um segredo no código, **When** o gitleaks executa no CI, **Then** o workflow falha.

---

### User Story 6 — Observabilidade: logs, métricas e SLO (Priority: P3)

Operadores conseguem monitorar a saúde da API em produção através de logs estruturados e métricas de latência.

**Why this priority**: Critério da rubrica (M3); entregável necessário mas não bloqueia o funcionamento da API.

**Independent Test**: Cada requisição gera um log em JSON; `GET /metrics` retorna histograma de latência; `docs/desempenho.md` declara o SLO com valor medido.

**Acceptance Scenarios**:

1. **Given** uma requisição à API, **When** processada, **Then** um log JSON é emitido com nível, rota, status, duração e id da requisição.
2. **Given** múltiplas requisições, **When** `GET /metrics` é chamado, **Then** retorna histograma de latência por rota.
3. **Given** o relatório de desempenho, **When** consultado, **Then** declara SLO com p95 medido pelo k6.

---

### User Story 7 — Documentação completa (Priority: P2)

Avaliadores e colaboradores entendem o projeto, as decisões técnicas e conseguem reproduzir tudo só pelo README.

**Why this priority**: Critério direto da rubrica (M4); peso 30.

**Independent Test**: Em ambiente limpo, seguindo apenas o README, a API sobe, os testes passam e o k6 roda.

**Acceptance Scenarios**:

1. **Given** o README, **When** seguido em ambiente limpo, **Then** a API sobe, os testes passam e o k6 roda sem passos adicionais.
2. **Given** o ADR 0001, **When** consultado, **Then** documenta contexto, opções, decisão (POST vs GET) e consequências.
3. **Given** o OpenAPI, **When** validado com Spectral, **Then** sem erros; GET marcado como depreciado.
4. **Given** o smoke test k6, **When** executado, **Then** reporta p95 e compara com o SLO declarado.

---

### Edge Cases

- O que acontece quando o texto contém apenas espaços ou quebras de linha?
- Como a API se comporta com caracteres especiais e emojis?
- O que acontece se o `Content-Type` não for `application/json` no POST?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A API DEVE aceitar `POST /count` com corpo JSON `{"text": "..."}` e retornar `{"count": N}`.
- **FR-002**: A API DEVE manter `GET /count/<texto>` funcionando, marcado como depreciado.
- **FR-003**: A API DEVE retornar 400 para corpo ausente ou campo `text` não textual.
- **FR-004**: A API DEVE retornar 413 para texto acima de 100 000 caracteres.
- **FR-005**: O formato de erro DEVE ser consistente em todos os casos de erro.
- **FR-006**: A contagem DEVE ignorar espaços múltiplos, espaços nas bordas e quebras de linha.
- **FR-007**: A API DEVE ser servida por um servidor de produção (gunicorn), mantendo Python 3.9.
- **FR-008**: A API DEVE ler configuração do ambiente via variáveis de ambiente.
- **FR-009**: O projeto DEVE ter `docker-compose.yml` que sobe a API com `docker compose up`.
- **FR-010**: O front DEVE ser opcional via `--profile front` no Compose.
- **FR-011**: O CI DEVE executar lint, testes e coverage mínimo de 80% a cada push.
- **FR-012**: O CI DEVE executar varredura de segredos com gitleaks.
- **FR-013**: A API DEVE emitir logs estruturados em JSON por requisição.
- **FR-014**: A API DEVE expor métricas de latência em `/metrics` (histograma, permite calcular p95).
- **FR-015**: O repositório DEVE conter ADR 0001 (MADR), OpenAPI validado com Spectral e smoke test k6.
- **FR-016**: O repositório DEVE conter `CONTRIBUTORS.md`, `docs/ia.md` e `docs/desempenho.md` com SLO e p95 medido.

### Key Entities

- **Requisição de contagem**: texto de entrada (string, máx. 100 000 caracteres) e contagem de palavras resultante (inteiro).
- **Erro**: código HTTP, mensagem descritiva, formato JSON consistente.
- **Métrica de latência**: histograma por rota, permite calcular p95.
- **SLO**: 95% das requisições a `/count` em até 300 ms (valor a calibrar com k6).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docker compose up` sobe a API em ambiente limpo em menos de 2 minutos.
- **SC-002**: CI executa e fica verde em menos de 5 minutos a cada push.
- **SC-003**: Cobertura de testes igual ou superior a 80%; CI falha automaticamente abaixo disso.
- **SC-004**: 95% das requisições a `/count` respondem em até 300 ms (SLO a calibrar com k6 antes da entrega).
- **SC-005**: Todos os testes passam, incluindo casos de borda (texto vazio, espaços, acentos, limite de tamanho).
- **SC-006**: OpenAPI validado pelo Spectral sem erros; ADR com contexto, opções, decisão e consequências.
- **SC-007**: README permite subir, testar e rodar o k6 em ambiente limpo sem passos adicionais.

## Assumptions

- Python 3.9 e imagem base existente são mantidos; atualização de versão está fora do escopo.
- O front-end (`word_count_front`) não é alterado; entra apenas como serviço opcional no Compose.
- Banco de dados e autenticação estão fora do escopo.
- O projeto é individual; `CONTRIBUTORS.md` é assinado pela autora.
- O valor final do SLO (300 ms p95) será calibrado com a medição real do k6 antes da entrega.
- O coverage mínimo é 80%; pode ser ajustado após revisão dos testes existentes.
- O limite de tamanho do texto é 100 000 caracteres; pode ser ajustado se houver justificativa.
