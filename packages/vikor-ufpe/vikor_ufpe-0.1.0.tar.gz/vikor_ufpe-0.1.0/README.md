# README - Implementação do Método VIKOR

## Descrição
Este repositório contém uma implementação do método de tomada de decisão multicritério VIKOR. O VIKOR é um método baseado em compromissos, utilizado para selecionar a melhor alternativa entre um conjunto de opções considerando múltiplos critérios.

## Estrutura do Projeto

O projeto é organizado da seguinte maneira:

```
VIKOR/
└── Back_end/
    ├── vikor_main.py
    ├── setup.py
    ├── requirements.txt
    ├── pyproject.toml
    ├── vikor/
    │   ├── __init__.py
    │   ├── decision.py
    │   ├── exceptions.py
    │   ├── models.py
    │   ├── utils.py
    │   ├── tests/
    │   │   ├── __init__.py
    │   │   ├── test_decision.py
    │   │   ├── test_models.py
    │   │   ├── test_utils.py
    │   │   ├── test_vikor.py
```

- `vikor_main.py` - Script principal para executar a análise VIKOR com entrada JSON.
- `setup.py` - Configuração do pacote para instalação via `pip`.
- `requirements.txt` - Lista de dependências do projeto.
- `pyproject.toml` - Arquivo de metadados do projeto.
- `vikor/` - Diretório principal do código fonte.
  - `__init__.py` - Define o pacote VIKOR e expõe as classes principais.
  - `decision.py` - Contém a implementação da classe `Vikor`, que executa o método de decisão.
  - `exceptions.py` - Define classes de exceções específicas para erros do método VIKOR.
  - `models.py` - Define as classes `Alternative` e `Criterion`, que representam alternativas e critérios de decisão.
  - `utils.py` - Contém funções auxiliares para normalização e validação de dados.
  - `tests/` - Contém testes unitários para validar o funcionamento do método.
    - `__init__.py` - Define o pacote de testes.
    - `test_decision.py` - Testes para a classe `Vikor` e sua avaliação.
    - `test_models.py` - Testes para as classes `Alternative` e `Criterion`.
    - `test_utils.py` - Testes para as funções auxiliares.
    - `test_vikor.py` - Testes para a função `run_vikor`.

## Como Usar

1. **Definir os Dados de Entrada**
   
   Os dados de entrada devem ser um dicionário JSON com a seguinte estrutura:

   ```json
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
   ```

2. **Executar a Análise VIKOR**
   
   No terminal, execute o script `vikor_main.py`:
   
   ```bash
   python vikor_main.py
   ```

3. **Executar Testes**
   
   Para rodar os testes unitários, utilize:
   
   ```bash
   pytest vikor/tests/
   ```

4. **Saída dos Resultados**

   O script retorna um JSON com:
   - Índices `S`, `R` e `Q`
   - Ranking das alternativas
   - Solução compromisso
   - Intervalos de estabilidade dos pesos
   - Distância Euclidiana para a solução ideal

## Instalação

Para instalar o pacote e suas dependências, execute:

```bash
pip install -r requirements.txt
```

Se desejar instalar como um pacote Python, utilize:

```bash
pip install .
```

## Dependências

As dependências estão listadas no arquivo `requirements.txt`:
- `colorama==0.4.6`
- `iniconfig==2.0.0`
- `packaging==24.2`
- `pluggy==1.5.0`
- `pytest==8.3.5`
- `setuptools==76.0.0`

## Autores
- **Gustavo Silva - gds4@cin.ufpe.br**
- **Arlen Filho - afsf2@cin.ufpe.br**
- **Hyan Silva - hlvs@cin.ufpe.br**
- **Eraldo Cassimiro - ejces@cin.ufpe.br**

## Licença
Este projeto está licenciado sob a MIT License.

## Contribuição
Pull requests são bem-vindos! Certifique-se de seguir as boas práticas de programação e incluir testes adequados.

