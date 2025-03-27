# vikor.py

import math

from __future__ import annotations
from typing import Dict, List, Tuple, Any

from .models import Alternative, Criterion
from .decision import Vikor

def compute_distance_to_ideal(vikor_obj: Vikor, alternatives: List[Alternative], criteria: List[Criterion]) -> Dict[str, float]:
    """
    Calcula a distância Euclidiana de cada alternativa até a solução ideal.

    A solução ideal é definida, para cada critério, como o valor ideal (f_star)
    calculado no objeto VIKOR.

    :param vikor_obj: Objeto Vikor com os valores ideais já calculados.
    :param alternatives: Lista de alternativas.
    :param criteria: Lista de critérios.
    :return: Dicionário mapeando o nome da alternativa à sua distância Euclidiana da solução ideal.
    """
    vikor_obj._determine_ideal_solutions()
    distances: Dict[str, float] = {}
    for alt in alternatives:
        sum_sq: float = 0.0
        for crit in criteria:
            ideal_value: float = vikor_obj.f_star[crit.name]
            diff: float = ideal_value - alt.scores[crit.name]
            sum_sq += diff * diff
        distances[alt.name] = math.sqrt(sum_sq)
    return distances

def compute_weight_stability(
    alternatives: List[Alternative],
    original_criteria: List[Criterion],
    v: float,
    resolution: float = 0.01
) -> Dict[str, Tuple[float, float]]:
    """
    Realiza uma análise de sensibilidade para determinar os intervalos de estabilidade dos pesos de cada critério.

    Para cada critério, varia-se seu peso de 0 a 1 com o passo definido por 'resolution'.
    Os demais critérios são ajustados proporcionalmente para que a soma dos pesos seja 1.
    Retorna um dicionário que mapeia o nome do critério para um intervalo (mínimo, máximo)
    onde o ranking da melhor alternativa permanece inalterado.

    :param alternatives: Lista de alternativas.
    :param original_criteria: Lista de critérios originais.
    :param v: Parâmetro v do método VIKOR.
    :param resolution: Passo de variação para os pesos (default: 0.01).
    :return: Dicionário mapeando o nome do critério para um intervalo (mínimo, máximo) de peso.
    """
    stability: Dict[str, Tuple[float, float]] = {}

    # Obter ranking original com os pesos originais
    original_vikor: Vikor = Vikor(alternatives, original_criteria, v)
    original_scores: Dict[str, float] = original_vikor.evaluate()
    original_ranking = sorted(original_scores.items(), key=lambda x: x[1])
    best_alternative: str = original_ranking[0][0]

    for crit in original_criteria:
        stable_values: List[float] = []
        total_other: float = sum(c.weight for c in original_criteria if c.name != crit.name)
        weight: float = 0.0
        while weight <= 1.0:
            new_criteria: List[Criterion] = []
            for c in original_criteria:
                if c.name == crit.name:
                    new_weight: float = weight
                else:
                    new_weight = c.weight * ((1 - weight) / total_other) if total_other > 0 else 0.0
                new_criteria.append(Criterion(c.name, new_weight, c.is_benefit))
            new_vikor: Vikor = Vikor(alternatives, new_criteria, v)
            new_scores: Dict[str, float] = new_vikor.evaluate()
            new_ranking = sorted(new_scores.items(), key=lambda item: item[1])
            new_best: str = new_ranking[0][0]
            if new_best == best_alternative:
                stable_values.append(weight)
            weight += resolution
        if stable_values:
            stability[crit.name] = (min(stable_values), max(stable_values))
        else:
            stability[crit.name] = (None, None)
    return stability

def run_vikor(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executa o método VIKOR com base na estrutura de entrada e retorna os resultados completos.

    A entrada deve seguir o formato:
    
    {
      "method": "VIKOR",
      "parameters": {
        "alternatives": ["A1", "A2", "A3"],
        "criteria": ["C1", "C2", "C3"],
        "performance_matrix": {
          "A1": [0.7, 0.5, 0.8],
          "A2": [0.6, 0.7, 0.6],
          "A3": [0.8, 0.6, 0.7]
        },
        "criteria_types": {
          "C1": "max",
          "C2": "min",
          "C3": "max"
        },
        "weights": {
          "C1": 0.4,
          "C2": 0.3,
          "C3": 0.3
        },
        "v": 0.5
      }
    }
    
    Os resultados retornados incluem:
      - Índices S (soma ponderada), R (máxima distância) e Q (índice final);
      - Ranking das alternativas;
      - Solução compromisso (alternativa de menor Q);
      - Intervalos de estabilidade dos pesos;
      - Distância Euclidiana de cada alternativa para a solução ideal.
    
    :param input_data: Dicionário com os parâmetros de entrada.
    :return: Dicionário com os resultados da avaliação VIKOR.
    :raises ValueError: Se os parâmetros de entrada estiverem incompletos ou incorretos.
    """
    parameters: Dict[str, Any] = input_data.get("parameters", {})
    alt_names: List[str] = parameters.get("alternatives", [])
    crit_names: List[str] = parameters.get("criteria", [])
    perf_matrix: Dict[str, List[float]] = parameters.get("performance_matrix", {})
    crit_types: Dict[str, str] = parameters.get("criteria_types", {})
    weights: Dict[str, float] = parameters.get("weights", {})
    v: float = parameters.get("v", 0.5)

    # Validação básica dos parâmetros
    if not alt_names or not crit_names or not perf_matrix or not crit_types or not weights:
        raise ValueError("Parâmetros de entrada incompletos.")

    # Criação dos objetos Alternative
    alternatives: List[Alternative] = []
    for alt in alt_names:
        perf_list: List[float] = perf_matrix.get(alt, [])
        if len(perf_list) != len(crit_names):
            raise ValueError(f"Dados de performance incorretos para a alternativa {alt}.")
        scores: Dict[str, float] = {crit_names[i]: perf_list[i] for i in range(len(crit_names))}
        alternatives.append(Alternative(alt, scores))

    # Normaliza os pesos para que sua soma seja 1
    total_weight: float = sum(weights.get(c, 0) for c in crit_names)
    if total_weight == 0:
        raise ValueError("A soma dos pesos não pode ser zero.")
    normalized_weights: Dict[str, float] = {c: weights[c] / total_weight for c in crit_names}

    # Criação dos objetos Criterion (is_benefit=True para "max", False para "min")
    criteria: List[Criterion] = []
    for crit in crit_names:
        crit_type: str = crit_types.get(crit, "")
        if crit_type not in ("max", "min"):
            raise ValueError(f"Tipo de critério inválido para {crit}.")
        is_benefit: bool = crit_type == "max"
        criteria.append(Criterion(crit, normalized_weights[crit], is_benefit))

    # Instancia o objeto VIKOR e calcula os índices Q (o método calcula S e R internamente)
    vikor_obj: Vikor = Vikor(alternatives, criteria, v)
    q_scores: Dict[str, float] = vikor_obj.evaluate()

    # Calcula os índices S e R para apresentação dos resultados
    S: Dict[str, float] = {}
    R: Dict[str, float] = {}
    vikor_obj._determine_ideal_solutions()
    for alt in alternatives:
        s_sum: float = 0.0
        r_max: float = float('-inf')
        for crit in criteria:
            f_star: float = vikor_obj.f_star[crit.name]
            f_minus: float = vikor_obj.f_minus[crit.name]
            f_val: float = alt.scores[crit.name]
            # Cálculo da normalização conforme o tipo do critério
            if crit.is_benefit:
                denom: float = f_star - f_minus if f_star != f_minus else 1e-10
                normalized: float = (f_star - f_val) / denom
            else:
               denom = f_minus - f_star if f_minus != f_star else 1e-10
               normalized = (f_val - f_star) / denom
            s_sum += crit.weight * normalized
            r_max = max(r_max, crit.weight * normalized)
        S[alt.name] = s_sum
        R[alt.name] = r_max

    # Define o ranking com base no índice Q (quanto menor, melhor)
    ranking_items: List[Tuple[str, float]] = sorted(q_scores.items(), key=lambda item: item[1])
    ranking: List[str] = [item[0] for item in ranking_items]
    compromise_solution: str = ranking[0] if ranking else ""

    # Calcula a estabilidade dos pesos e a distância à solução ideal
    weight_stability: Dict[str, Tuple[float, float]] = compute_weight_stability(alternatives, criteria, v, resolution=0.01)
    distance_to_ideal: Dict[str, float] = compute_distance_to_ideal(vikor_obj, alternatives, criteria)

    return {
        "method": "VIKOR",
        "results": {
            "scores": {
                alt: {"S": S[alt], "R": R[alt], "Q": q_scores[alt]} for alt in alt_names
            },
            "ranking": ranking,
            "compromise_solution": compromise_solution,
            "weight_stability": weight_stability,
            "distance_to_ideal": distance_to_ideal,
        }
    }