# ADR 0001 — Receber texto no corpo de POST em vez de parâmetro de URL

**Status**: Aceito
**Data**: 2026-11-09

## Contexto

O endpoint original recebe o texto na URL (`GET /count/<texto>`). Essa abordagem tem três problemas concretos:

1. **Limite de tamanho**: URLs têm limite prático de ~2000 caracteres na maioria dos clientes e servidores, o que impede contar palavras em textos longos.
2. **Codificação obrigatória**: espaços e caracteres especiais precisam ser codificados (`%20`, `%C3%A7`), tornando o uso manual e a depuração mais difíceis.
3. **Exposição em logs**: o texto aparece nos logs de acesso do servidor, o que pode ser indesejável para conteúdo sensível.

## Opções consideradas

### Opção 1 — Manter GET com texto na URL

- Simples, sem mudança de contrato.
- Mantém todos os problemas listados acima.
- Não permite validar tamanho e retornar 413.

### Opção 2 — POST /count com corpo JSON `{"text": "..."}`

- Sem limite prático de tamanho no corpo.
- Sem necessidade de codificação de URL.
- Texto não aparece em logs de acesso.
- Permite validar o campo e retornar 400/413 com mensagem descritiva.
- Requer migração do front-end.

## Decisão

Adotar **POST /count com corpo JSON**, mantendo o `GET /count/<texto>` como depreciado por compatibilidade com o front-end existente durante o período de transição.

## Consequências

- Textos longos (até 100 000 caracteres) passam a funcionar corretamente.
- É possível validar a entrada e responder 413 para textos acima do limite.
- O front-end precisará migrar para o POST em uma versão futura.
- O OpenAPI documenta os dois endpoints e marca o GET como `deprecated: true`.
- O ADR serve de base para a apresentação do projeto.
