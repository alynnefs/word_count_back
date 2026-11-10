# Data Model: Adequação do word_count_back ao Projeto B

**Branch**: `001-adequacao-projeto-b`

## Entidades

### CountRequest (entrada do POST /count)

| Campo | Tipo    | Obrigatório | Validação                                      |
|-------|---------|-------------|------------------------------------------------|
| text  | string  | sim         | Deve ser string; máx. 100 000 caracteres       |

Erros de validação:
- Corpo ausente ou `Content-Type` não JSON → 400 `{"error": "corpo JSON ausente ou inválido"}`
- Campo `text` ausente → 400 `{"error": "campo 'text' obrigatório"}`
- Campo `text` não é string → 400 `{"error": "campo 'text' deve ser uma string"}`
- `text` com mais de 100 000 caracteres → 413 `{"error": "texto excede o limite de 100000 caracteres"}`

### CountResponse (resposta de sucesso)

| Campo | Tipo    | Descrição                              |
|-------|---------|----------------------------------------|
| count | inteiro | Número de palavras únicas no texto     |

### ErrorResponse (resposta de erro)

| Campo | Tipo   | Descrição              |
|-------|--------|------------------------|
| error | string | Mensagem de erro legível |

## Regra de contagem (Service Layer)

`count_words(text: str) -> int`

1. Strip de espaços e quebras de linha nas bordas.
2. Split por whitespace (cobre espaços múltiplos e `\n`, `\t`).
3. Filtrar tokens vazios.
4. Remover duplicatas (preservando ordem de aparição).
5. Retornar `len` da lista resultante.

Casos especiais:
- Texto vazio ou só espaços → 0
- Texto com acentos → tratado normalmente (split por whitespace, não por caractere)
- Emojis → tratados como tokens (sem tratamento especial)

## Estrutura de módulos em `app/`

```
app/
├── __init__.py       # cria e configura o Flask app
├── counter.py        # Service Layer: count_words()
├── validators.py     # valida CountRequest, levanta exceções tipadas
├── routes.py         # registra GET /count/<text> e POST /count
├── logging_config.py # configura python-json-logger
├── metrics.py        # inicializa prometheus-flask-exporter
└── main.py           # ponto de entrada (importado pelo gunicorn/flask)
```

## Variáveis de ambiente

| Variável         | Padrão  | Descrição                              |
|------------------|---------|----------------------------------------|
| FLASK_ENV        | production | Modo do Flask                       |
| PORT             | 5000    | Porta de escuta                        |
| MAX_TEXT_LENGTH  | 100000  | Limite de caracteres do texto          |
| LOG_LEVEL        | INFO    | Nível de log                           |
