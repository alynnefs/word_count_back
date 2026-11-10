**Projeto B — Módulo 4**

[![CI](https://github.com/alynnefs/word_count_back/actions/workflows/ci.yml/badge.svg)](https://github.com/alynnefs/word_count_back/actions/workflows/ci.yml)

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
