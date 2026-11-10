# API Contract: word_count_back

**Branch**: `001-adequacao-projeto-b`
**Format**: OpenAPI 3.0 (rascunho para `docs/openapi.yaml`)

## Endpoints

### POST /count *(principal)*

**Request**
```
Content-Type: application/json

{
  "text": "string (máx. 100 000 caracteres)"
}
```

**Responses**

| Status | Corpo                        | Quando                                      |
|--------|------------------------------|---------------------------------------------|
| 200    | `{"count": <inteiro>}`       | Texto válido processado                     |
| 400    | `{"error": "<mensagem>"}`    | Corpo ausente, campo inválido ou não string |
| 413    | `{"error": "<mensagem>"}`    | Texto acima de 100 000 caracteres           |

---

### GET /count/\<text\> *(depreciado)*

**Request**: texto na URL (path parameter), codificado em URL.

**Responses**

| Status | Corpo                  | Quando              |
|--------|------------------------|---------------------|
| 200    | `<inteiro>` (string)   | Texto processado    |

> ⚠️ Depreciado. Mantido por compatibilidade com o front. Migrar para `POST /count`.

---

### GET /metrics

Expõe métricas no formato Prometheus (histograma de latência por rota).

---

## Invariantes do contrato

- Toda resposta de erro usa `{"error": "<mensagem>"}`.
- `POST /count` sempre retorna JSON; `GET /count/<text>` retorna string plana (comportamento legado mantido).
- O campo `count` é sempre inteiro ≥ 0.
