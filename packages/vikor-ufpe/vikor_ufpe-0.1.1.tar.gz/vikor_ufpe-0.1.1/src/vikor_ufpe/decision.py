# vikor/decision.py

from __future__ import annotations

from typing import List, Dict
from .models import Alternative, Criterion
from .exceptions import VikorError
from .utils import normalize_value, validate_alternatives_scores

class Vikor:
    def __init__(self, alternatives: List[Alternative], criteria: List[Criterion], v: float = 0.5) -> None:
        """
        Inicializa a classe VIKOR com as alternativas, os critérios e o parâmetro v.

        :param alternatives: Lista de alternativas a serem avaliadas.
        :param criteria: Lista de critérios considerados.
        :param v: Parâmetro de ponderação (entre 0 e 1) que reflete o trade-off entre utilidade e arrependimento.
                  v = 1 prioriza a utilidade do grupo; v = 0 prioriza o menor arrependimento individual; v = 0.5 é o equilíbrio.
        :raises VikorError: Se os parâmetros não atenderem os requisitos (por exemplo, v fora do intervalo ou listas vazias).
        """
        self.alternatives: List[Alternative] = alternatives
        self.criteria: List[Criterion] = criteria
        self.v: float = v
        self.f_star: Dict[str, float] = {}   # Armazena o valor ideal (melhor) para cada critério.
        self.f_minus: Dict[str, float] = {}    # Armazena o valor anti-ideal (pior) para cada critério.
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """
        Valida os parâmetros de entrada.
        
        :raises VikorError: Se v não estiver entre 0 e 1 ou se as listas de alternativas ou critérios estiverem vazias.
        """
        if not (0 <= self.v <= 1):
            raise VikorError("O parâmetro v deve estar entre 0 e 1.")
        if not self.alternatives:
            raise VikorError("A lista de alternativas não pode estar vazia.")
        if not self.criteria:
            raise VikorError("A lista de critérios não pode estar vazia.")

        # Verifica se todas as alternativas possuem pontuações para todos os critérios.
        validate_alternatives_scores(self.alternatives, self.criteria)

    def _determine_ideal_solutions(self) -> None:
        """
        Determina os valores ideais (melhor) e anti-ideais (pior) para cada critério,
        considerando se o critério é de benefício ou de custo.
        
        Para um critério de benefício, o valor ideal é o máximo e o anti-ideal é o mínimo;
        para um critério de custo, o ideal é o mínimo e o anti-ideal o máximo.
        
        :raises VikorError: Se alguma alternativa não possuir pontuação para um critério.
        """
        for crit in self.criteria:
            scores: List[float] = []
            for alt in self.alternatives:
                score = alt.scores.get(crit.name)
                if score is None:
                    raise VikorError(
                        f"Uma ou mais alternativas não possuem pontuação para o critério '{crit.name}'."
                    )
                scores.append(float(score))
            # Definindo os valores ideal e anti-ideal com base no tipo do critério.
            if crit.is_benefit:
                self.f_star[crit.name] = max(scores)
                self.f_minus[crit.name] = min(scores)
            else:
                self.f_star[crit.name] = min(scores)
                self.f_minus[crit.name] = max(scores)

    def evaluate(self) -> Dict[str, float]:
        """
        Executa o método VIKOR e retorna os índices Q para cada alternativa.
        
        O índice Q é calculado a partir dos índices S (soma das distâncias ponderadas) e R (máxima distância individual).
        Estes índices são derivados de uma normalização dos valores das alternativas em relação aos valores ideais.
        
        :return: Dicionário onde a chave é o nome da alternativa e o valor é o índice Q calculado.
        :raises VikorError: Se ocorrer um erro durante os cálculos (por exemplo, divisão por zero não tratada).
        """
        self._determine_ideal_solutions()

        S: Dict[str, float] = {}  # Soma das distâncias ponderadas (medida agregada de utilidade).
        R: Dict[str, float] = {}  # Máxima distância ponderada (medida de arrependimento).

        # Calcula S e R para cada alternativa.
        for alt in self.alternatives:
            S_sum: float = 0.0
            R_max: float = float('-inf')
            for crit in self.criteria:
                f_star: float = self.f_star[crit.name]
                f_minus: float = self.f_minus[crit.name]
                f_ij: float = float(alt.scores[crit.name])
                
                normalized: float = normalize_value(f_star, f_minus, f_ij)
                S_sum += crit.weight * normalized
                R_max = max(R_max, crit.weight * normalized)
            S[alt.name] = S_sum
            R[alt.name] = R_max

        # Verifica a consistência dos valores calculados.
        if not S or not R:
            raise VikorError("Erro ao calcular as medidas agregadas S ou R.")

        S_values: List[float] = list(S.values())
        R_values: List[float] = list(R.values())
        S_min: float = min(S_values)
        S_max: float = max(S_values)
        R_min: float = min(R_values)
        R_max: float = max(R_values)

        Q: Dict[str, float] = {}
        for alt in self.alternatives:
            S_diff: float = S_max - S_min if S_max != S_min else 1e-10
            R_diff: float = R_max - R_min if R_max != R_min else 1e-10
            Q[alt.name] = self.v * (S[alt.name] - S_min) / S_diff + (1 - self.v) * (R[alt.name] - R_min) / R_diff

        return Q
