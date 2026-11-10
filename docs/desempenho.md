# Relatório de Desempenho

## SLO declarado

95% das requisições a `POST /count` respondem em até **300 ms** (p95 ≤ 300 ms).

## Ambiente de medição

- Imagem: `python:3.9`
- Servidor: `gunicorn 20.1.0` (worker sync, 1 worker)
- Plataforma: Docker local (macOS)
- Ferramenta: k6

## Comando

```bash
docker compose up -d
k6 run tests/k6/smoke.js
```

Ou com URL customizada:

```bash
k6 run -e BASE_URL=http://localhost:5001 tests/k6/smoke.js
```

## Resultado

| Métrica | Valor medido |
|---------|-------------|
| p95     | _a preencher após execução_ |
| p99     | _a preencher após execução_ |
| mediana | _a preencher após execução_ |
| VUs     | 10 |
| Duração | 30s |

## Comparação com o SLO

| SLO | p95 medido | Status |
|-----|-----------|--------|
| ≤ 300 ms | _a preencher_ | _a preencher_ |

## Notas

- O valor do SLO será ajustado se o p95 medido indicar que 300 ms é muito restritivo ou muito folgado para o ambiente local.
- Para medir, a API deve estar rodando via `docker compose up` antes de executar o k6.
