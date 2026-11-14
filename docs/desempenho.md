# Relatório de Desempenho

## SLO declarado

95% das requisições a `POST /count` respondem em até **300 ms** (p95 ≤ 300 ms).

## Ambiente de medição

- Imagem: `python:3.9`
- Servidor: `gunicorn 20.1.0` (4 workers sync)
- Plataforma: Docker local (macOS)
- Ferramenta: k6 (10 VUs, 30s)

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
| p95     | 5.53 ms |
| p90     | 4.60 ms |
| mediana | 2.88 ms |
| média   | 3.22 ms |
| máximo  | 81.35 ms |
| VUs     | 10 |
| Duração | 30s |
| Requisições | 86 771 |
| Taxa    | 2 892 req/s |
| Falhas  | 0% |

## Comparação com o SLO

| SLO | p95 medido | Status |
|-----|-----------|--------|
| ≤ 300 ms | 5.53 ms | ✅ Aprovado |

## Notas

- O SLO de 300 ms é folgado para este ambiente — o p95 real ficou em 5.53 ms, 54x abaixo do limite.
- O primeiro teste com 1 worker apresentou 25% de falhas por saturação do worker sync. Corrigido com 4 workers.
- Para medir, a API deve estar rodando via `docker compose up` antes de executar o k6.

## Resultado — Produção (Vercel)

| Métrica | Valor medido |
|---------|-------------:|
| p95 | 204.92 ms |
| p90 | 198.17 ms |
| mediana | 187.65 ms |
| média | 189.77 ms |
| máximo | 556.02 ms |
| VUs | 10 |
| Duração | 30s |
| Requisições | 1.577 |
| Taxa | 52,22 req/s |
| Falhas | 0% |

## Comparação com o SLO

| SLO | p95 medido | Status |
|-----|-----------:|--------|
| ≤ 300 ms | 204.92 ms | ✅ Aprovado |

- O SLO de 300 ms foi cumprido em produção.
- O p95 ficou aproximadamente **1,46x abaixo do limite**.
- 100% dos checks passaram, sem falhas HTTP.
- A latência média em produção foi de 189,77 ms, contra 3,22 ms no ambiente local.

## Comparação: Local vs. Produção

| Métrica | Local | Produção |
|---------|-------:|---------:|
| p95 | 5,53 ms | 204,92 ms |
| p90 | 4,60 ms | 198,17 ms |
| Mediana | 2,88 ms | 187,65 ms |
| Média | 3,22 ms | 189,77 ms |
| Máximo | 81,35 ms | 556,02 ms |
| Requisições | 86.771 | 1.577 |
| Taxa | 2.892 req/s | 52,22 req/s |
| Falhas | 0% | 0% |

**Análise:** a aplicação apresenta latência significativamente maior em produção, o que é esperado devido a fatores como rede, infraestrutura da Vercel e execução serverless. Mesmo assim, o p95 permanece abaixo do SLO de 300 ms.

*Observação: os testes têm ambientes e volumes diferentes. Portanto, essa comparação é indicativa, não um benchmark controlado.*