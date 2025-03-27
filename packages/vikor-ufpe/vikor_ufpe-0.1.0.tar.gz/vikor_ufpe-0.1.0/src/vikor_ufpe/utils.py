# vikor/utils.py

from __future__ import annotations
from typing import List
from .models import Alternative, Criterion
from .exceptions import VikorMissingScoreError

__all__ = ["normalize_value", "validate_alternatives_scores"]

def normalize_value(f_star: float, f_minus: float, f: float) -> float:
    """
    Normaliza o valor 'f' com base no valor ideal (f_star) e anti-ideal (f_minus).

    A normalização é calculada como:
        (f_star - f) / (f_star - f_minus)
    Se f_star for igual a f_minus, utiliza-se um denominador muito pequeno (1e-10) para evitar divisão por zero.

    :param f_star: Valor ideal para o critério (ex.: maior para benefício ou menor para custo).
    :param f_minus: Valor anti-ideal para o critério.
    :param f: Valor a ser normalizado.
    :return: Valor normalizado.
    """
    denom: float = f_star - f_minus
    if denom == 0:
        # Evita divisão por zero utilizando um valor muito pequeno.
        denom = 1e-10
    return (f_star - f) / denom

def validate_alternatives_scores(alternatives: List[Alternative], criteria: List[Criterion]) -> None:
    """
    Valida se todas as alternativas possuem pontuações para cada critério informado.

    Percorre cada alternativa e, para cada critério, verifica se a pontuação existe.
    Se faltar a pontuação para algum critério, levanta a exceção VikorMissingScoreError.

    :param alternatives: Lista de alternativas.
    :param criteria: Lista de critérios.
    :raises VikorMissingScoreError: Se alguma alternativa não possuir pontuação para um critério.
    """
    for alt in alternatives:
        for crit in criteria:
            if crit.name not in alt.scores:
                raise VikorMissingScoreError(alt.name, crit.name)
