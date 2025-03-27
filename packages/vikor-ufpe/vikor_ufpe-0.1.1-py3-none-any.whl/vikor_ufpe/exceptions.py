# vikor/exceptions.py

from typing import Optional

class VikorError(Exception):
    """Exceção base para erros relacionados ao método VIKOR."""
    pass


class VikorParameterError(VikorError):
    """Exceção para erros relacionados a parâmetros inválidos."""
    def __init__(self, message: str = "Parâmetro inválido.") -> None:
        super().__init__(message)


class VikorInputError(VikorError):
    """Exceção para erros na entrada de dados (alternativas ou critérios)."""
    def __init__(self, message: str = "Erro na entrada de dados.") -> None:
        super().__init__(message)


class VikorMissingScoreError(VikorInputError):
    """Exceção para casos em que uma alternativa não possui a pontuação necessária para um critério."""
    def __init__(self, alternative: str, criterion: str, message: Optional[str] = None) -> None:
        if message is None:
            message = f"A alternativa '{alternative}' não possui a pontuação para o critério '{criterion}'."
        super().__init__(message)


class VikorCalculationError(VikorError):
    """Exceção para erros ocorridos durante os cálculos dos índices VIKOR."""
    def __init__(self, message: str = "Erro durante o cálculo do método VIKOR.") -> None:
        super().__init__(message)


class VikorNormalizationError(VikorError):
    """Exceção para erros ocorridos durante a normalização dos dados."""
    def __init__(self, message: str = "Erro durante a normalização dos dados.") -> None:
        super().__init__(message)


class VikorDataTypeError(VikorError):
    """Exceção para casos em que os dados fornecidos não são do tipo esperado."""
    def __init__(self, message: str = "Tipo de dado inválido.") -> None:
        super().__init__(message)


class VikorConfigurationError(VikorError):
    """Exceção para erros de configuração do ambiente ou da biblioteca."""
    def __init__(self, message: str = "Erro na configuração da biblioteca VIKOR.") -> None:
        super().__init__(message)
