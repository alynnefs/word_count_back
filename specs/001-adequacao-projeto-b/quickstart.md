# Quickstart: Validação end-to-end

**Branch**: `001-adequacao-projeto-b`

## Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.9+ (para rodar testes localmente)
- k6 instalado (`brew install k6` no macOS)

## 1. Subir a API com Docker Compose

```bash
cp .env.example .env          # ajuste variáveis se necessário
docker compose up --build -d
```

Verificar que a API responde:

```bash
curl -s http://localhost:5000/count/hello
# esperado: 1

curl -s -X POST http://localhost:5000/count \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}' 
# esperado: {"count": 2}
```

## 2. Rodar os testes localmente

```bash
pip install -r requirements-dev.txt
pytest --cov=app --cov-fail-under=80
```

Todos os testes devem passar e a cobertura deve ser ≥ 80%.

## 3. Verificar lint

```bash
flake8 app/ tests/
```

Sem erros.

## 4. Validar casos de erro

```bash
# 400 — corpo ausente
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/count
# esperado: 400

# 400 — campo text não é string
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/count \
  -H "Content-Type: application/json" -d '{"text": 123}'
# esperado: 400

# 413 — texto acima do limite
python3 -c "import json; print(json.dumps({'text': 'a ' * 50001}))" | \
  curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/count \
  -H "Content-Type: application/json" -d @-
# esperado: 413
```

## 5. Verificar métricas e logs

```bash
# Métricas Prometheus
curl -s http://localhost:5000/metrics | grep flask_http

# Logs estruturados (JSON)
docker compose logs api | head -5
# cada linha deve ser JSON com campos: level, route, status, duration, request_id
```

## 6. Rodar o smoke test k6

```bash
docker compose up -d   # API deve estar rodando
k6 run tests/k6/smoke.js
# verificar: p95 ≤ 300ms (SLO declarado em docs/desempenho.md)
```

## 7. Subir com o front (opcional)

```bash
docker compose --profile front up
# API em http://localhost:5000
# Front em http://localhost:8080 (ou porta configurada)
```

## Resultados esperados

| Cenário                        | Resultado                          |
|--------------------------------|------------------------------------|
| `docker compose up`            | API responde na porta 5000         |
| `pytest --cov-fail-under=80`   | Verde, cobertura ≥ 80%             |
| `flake8`                       | Sem erros                          |
| POST com texto válido          | 200 `{"count": N}`                 |
| POST sem corpo                 | 400 `{"error": "..."}`             |
| POST com texto > 100k chars    | 413 `{"error": "..."}`             |
| GET /metrics                   | Histograma de latência presente    |
| k6 smoke test                  | p95 ≤ 300ms                        |
