# vikor/models.py

from __future__ import annotations
from typing import Dict, Union

Number = Union[int, float]

class Alternative:
    __slots__ = ('name', 'scores')

    def __init__(self, name: str, scores: Dict[str, Number]) -> None:
        """
        Representa uma alternativa a ser avaliada.

        :param name: Nome da alternativa.
        :param scores: Dicionário contendo as pontuações da alternativa para cada critério.
                       As chaves devem ser strings correspondentes aos nomes dos critérios e os valores numéricos.
                       Exemplo: {'Custo': 100, 'Qualidade': 80}
        :raises TypeError: Se o nome não for uma string ou se scores não for um dicionário com chaves string e valores numéricos.
        """
        if not isinstance(name, str):
            raise TypeError("O nome deve ser uma string.")
        if not isinstance(scores, dict):
            raise TypeError("scores deve ser um dicionário.")
        for key, value in scores.items():
            if not isinstance(key, str):
                raise TypeError("Cada chave em scores deve ser uma string.")
            if not isinstance(value, (int, float)):
                raise TypeError("Cada valor em scores deve ser um número (int ou float).")
        self.name: str = name
        self.scores: Dict[str, Number] = scores.copy()  # Cria uma cópia defensiva do dicionário

    def __repr__(self) -> str:
        return f"Alternative(name={self.name!r}, scores={self.scores!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Alternative):
            return self.name == other.name and self.scores == other.scores
        return NotImplemented

    def __hash__(self) -> int:
        # Permite o uso de Alternative em conjuntos e como chave de dicionários.
        return hash((self.name, frozenset(self.scores.items())))


class Criterion:
    __slots__ = ('name', 'weight', 'is_benefit')

    def __init__(self, name: str, weight: Number, is_benefit: bool = True) -> None:
        """
        Representa um critério para a avaliação.

        :param name: Nome do critério.
        :param weight: Peso do critério, que influencia a importância relativa no cálculo.
                       Deve ser um número (int ou float) e preferencialmente não negativo.
        :param is_benefit: Indica se o critério é de benefício (True, quanto maior melhor) ou de custo (False, quanto menor melhor).
        :raises TypeError: Se o nome não for string, weight não for numérico ou is_benefit não for booleano.
        :raises ValueError: Se o peso for negativo.
        """
        if not isinstance(name, str):
            raise TypeError("O nome do critério deve ser uma string.")
        if not isinstance(weight, (int, float)):
            raise TypeError("O peso do critério deve ser um número (int ou float).")
        if weight < 0:
            raise ValueError("O peso do critério não pode ser negativo.")
        if not isinstance(is_benefit, bool):
            raise TypeError("is_benefit deve ser um valor booleano.")
        self.name: str = name
        self.weight: Number = weight
        self.is_benefit: bool = is_benefit

    def __repr__(self) -> str:
        return f"Criterion(name={self.name!r}, weight={self.weight!r}, is_benefit={self.is_benefit!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Criterion):
            return (
                self.name == other.name and 
                self.weight == other.weight and 
                self.is_benefit == other.is_benefit
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.weight, self.is_benefit))
