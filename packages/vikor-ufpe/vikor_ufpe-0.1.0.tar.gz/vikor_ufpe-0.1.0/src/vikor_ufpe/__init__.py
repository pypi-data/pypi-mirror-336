# vikor/__init__.py

"""
Pacote VIKOR: Implementação do método de decisão multicritério.

Este pacote expõe as classes e funções principais utilizadas para construir e executar
o método VIKOR, incluindo as classes de modelos, a lógica de decisão, as funções auxiliares e
as exceções específicas.

Uso:
    from vikor import Alternative, Criterion, Vikor, normalize_value, validate_alternatives_scores

Versão:
    0.1.0
"""

__version__ = "0.1.0"

from .main import run_vikor
from .models import Alternative, Criterion
from .decision import Vikor
from .utils import normalize_value, validate_alternatives_scores
from .exceptions import *

__all__ = [
    "run_vikor",
    "Alternative",
    "Criterion",
    "Vikor",
    "normalize_value",
    "validate_alternatives_scores",
    "VikorError",
    "VikorParameterError",
    "VikorInputError",
    "VikorMissingScoreError",
    "VikorCalculationError",
    "VikorNormalizationError",
    "VikorDataTypeError",
    "VikorConfigurationError",
]
