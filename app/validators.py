import os


MAX_TEXT_LENGTH = int(os.environ.get("MAX_TEXT_LENGTH", 100000))


def validate_count_request(data):
    if not data or not isinstance(data, dict):
        raise ValueError("corpo JSON ausente ou inválido")
    if "text" not in data:
        raise ValueError("campo 'text' obrigatório")
    if not isinstance(data["text"], str):
        raise ValueError("campo 'text' deve ser uma string")
    if len(data["text"]) > MAX_TEXT_LENGTH:
        raise OverflowError(
            f"texto excede o limite de {MAX_TEXT_LENGTH} caracteres"
        )
