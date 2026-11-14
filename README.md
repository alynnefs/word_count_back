**Projeto B**

[![CI](https://github.com/alynnefs/word_count_back/actions/workflows/ci.yml/badge.svg)](https://github.com/alynnefs/word_count_back/actions/workflows/ci.yml)

[Back](https://word-count-back.vercel.app/) | [Front](https://word-count-front.vercel.app/)

**Tabela de entregas**
|Módulo| Entregável| Evidência |
|--|--|--|
|M1| Compose que sobe com 1 comando, SOLID, 1 pattern justificado| [compose](https://github.com/alynnefs/word_count_back/blob/main/docker-compose.yml), [SOLID pode ser verificado na pasta app](https://github.com/alynnefs/word_count_back/tree/main/app). Pattern Service Layer* |
|M2|Testes unitários do domínio e 1 teste de integração| [Testes unitários](https://github.com/alynnefs/word_count_back/tree/main/tests/unit), [testes de integração](https://github.com/alynnefs/word_count_back/tree/main/tests/integration), [testes E2E](https://github.com/alynnefs/word_count_front/tree/main/tests/e2e)|
|M2|Coverage mínimo declarado e respeitado|  [declarado](https://github.com/alynnefs/word_count_back/blob/a68af79a7d913da6eea406bc45c9222578210003/specs/001-adequacao-projeto-b/plan.md?plain=1#L63), [respeitado](https://github.com/alynnefs/word_count_back/actions/runs/43528722781/job/132240951714#step:5:34)
|M3|CI verde: install, lint, test| [CI](https://github.com/alynnefs/word_count_back/actions/workflows/ci.yml)|
|M3|.env.example no repositório, segredos fora dele| [.env.example](https://github.com/alynnefs/word_count_back/blob/main/.env.example), [segredos](https://github.com/alynnefs/word_count_front/settings/secrets/actions)|
|M3|Logs estruturados, 1 métrica e 1 SLO simples| [logs](https://github.com/search?q=repo%3Aalynnefs%2Fword_count_back+LOG_LEVEL&type=code), [métrica](https://word-count-back.vercel.app/docs/#/default/getMetrics), [SLO](https://github.com/alynnefs/word_count_back/blob/db1ad0da4c8dd7fbbda531992c682b99a18641f2/docs/desempenho.md#slo-declarado)
|M4|README do primeiro dia e 1 ADR| [README inicial](https://github.com/alynnefs/word_count_back/commit/e9895b24f6cc1ceae3426605d3a04e76ee10d031), [ADR](https://github.com/alynnefs/word_count_back/blob/main/docs/adr/0001-decisao.md)
|M4|	OpenAPI do endpoint principal e 1 smoke test k6 com p95 medido| [endpoint principal](https://word-count-back.vercel.app/), [teste de carga (smoke)](https://github.com/alynnefs/word_count_back/tree/main/tests/k6), [p95](https://github.com/alynnefs/word_count_back/blob/main/docs/desempenho.md)|
|Extra|Issues organizadas em projeto | [projeto](https://github.com/users/alynnefs/projects/1)|
|Extra|Front simples| [repositório](https://github.com/alynnefs/word_count_front)|


**Pattern Service Layer** *

Escolhi o pattern Service Layer porque era necessário organizar a execução de um caso de uso. Ele funciona como intermediário entre o Controller (rota Flask) e a lógica responsável pelo processamento. A ideia é manter o Controller responsável pelo HTTP e deixar a execução do caso de uso fora dele. 

Fluxo conceitual:
![image](https://hackmd.io/_uploads/BJB6ANBCMx.png)

# Word Count — Back

API Flask que recebe um texto e retorna a contagem de palavras únicas.

- Decisão de arquitetura: [ADR 0001](docs/adr/0001-decisao.md)
- Contrato da API: [OpenAPI](docs/openapi.yaml)
- Relatório de desempenho: [docs/desempenho.md](docs/desempenho.md)

## Como subir com Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
```

> **macOS**: a porta 5000 é ocupada pelo AirPlay Receiver. Edite `.env` e defina `PORT=5001` antes de subir.

Verificar que a API responde:

```bash
curl http://localhost:5001/count/hello
# esperado: 1

curl -X POST http://localhost:5001/count \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
# esperado: {"count": 2}
```

Para subir também o front-end:

```bash
docker compose --profile front up
```

## Como rodar os testes

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Cobertura mínima exigida: 80% (aplicada automaticamente).

## Como rodar o lint

```bash
flake8 app/ tests/
```

## Como rodar o smoke test k6

Com a API rodando via Compose:

```bash
k6 run tests/k6/smoke.js
```

O resultado reporta o p95 de latência e compara com o SLO declarado em [docs/desempenho.md](docs/desempenho.md).

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/count` | Conta palavras únicas — corpo JSON `{"text": "..."}` |
| GET | `/count/<text>` | ⚠️ Depreciado — mantido por compatibilidade com o front |
| GET | `/metrics` | Métricas Prometheus (histograma de latência) |

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `PORT` | `5000` | Porta exposta pelo container |
| `MAX_TEXT_LENGTH` | `100000` | Limite de caracteres do texto |
| `LOG_LEVEL` | `INFO` | Nível de log |
| `FLASK_DEBUG` | `0` | Debug mode (0 = desligado) |
