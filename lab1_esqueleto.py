"""
LAB 1 — Simulated Annealing: representação binária para minimização de f(x)
============================================================================
Siga os slides para implementar cada etapa na ordem indicada.
"""

import numpy as np
import matplotlib.pyplot as plt


# ══════════════════════════════════════════════
# ETAPA 1 — Visualize o problema
# ══════════════════════════════════════════════

def plotar_funcao():
    """Plote f(x) = x * sin(x) no intervalo [-20, 20]."""
    x = np.linspace(-20, 20, 1000)

    # TODO: calcule y = f(x)
    y = None

    plt.figure(figsize=(8, 3))
    plt.plot(x, y, color="steelblue")
    plt.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    plt.title("f(x) = x · sin(x)")
    plt.xlabel("x"); plt.ylabel("f(x)")
    plt.tight_layout()
    plt.show()


# ══════════════════════════════════════════════
# ETAPA 2 — Representação binária
# ══════════════════════════════════════════════

N_BITS = 16
X_MIN  = -20.0
X_MAX  =  20.0

def decodificar(sol):
    """
    Converte vetor binário → valor real em [X_MIN, X_MAX].

    Fórmula (ver slide):
        inteiro = valor inteiro do vetor de bits (base 2)
        x = X_MIN + inteiro * (X_MAX - X_MIN) / (2^N_BITS - 1)
    """
    # TODO: implemente a decodificação
    pass


# ══════════════════════════════════════════════
# ETAPA 3 — Funções do problema
# ══════════════════════════════════════════════

def p1_inicial():
    """Gera solução inicial: vetor binário aleatório de N_BITS elementos."""
    # TODO: retorne um np.array de 0s e 1s com tamanho N_BITS
    pass


def p1_vizinho(sol):
    """
    Gera um vizinho: copia sol e inverte (flip) um bit aleatório.
    Dica: nova[i] = 1 - nova[i]
    """
    # TODO: implemente o flip de bit
    pass


def p1_objetivo(sol):
    """Calcula o custo: f(x) avaliado no x decodificado."""
    # TODO: decodifique sol e retorne f(x)
    pass


# ══════════════════════════════════════════════
# ETAPA 4 — Núcleo SA (já implementado — leia e entenda)
# ══════════════════════════════════════════════

def simulated_annealing(
    inicial_fn,
    vizinho_fn,
    objetivo_fn,
    T0=500.0,
    T_min=1e-4,
    alpha=0.997,
    n_iter=100
):
    """
    Simulated Annealing genérico.
    Recebe 3 funções e busca o mínimo de objetivo_fn.
    Este núcleo será reutilizado no Lab 2 sem nenhuma alteração.
    """
    atual = inicial_fn()
    custo_atual = objetivo_fn(atual)
    melhor = atual.copy()
    melhor_custo = custo_atual
    T = T0
    historico = [custo_atual]

    while T > T_min:
        for _ in range(n_iter):
            candidato = vizinho_fn(atual)
            custo_candidato = objetivo_fn(candidato)
            delta = custo_candidato - custo_atual
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                atual = candidato
                custo_atual = custo_candidato
                if custo_atual < melhor_custo:
                    melhor = atual.copy()
                    melhor_custo = custo_atual
            historico.append(custo_atual)
        T *= alpha

    return melhor, melhor_custo, historico


# ══════════════════════════════════════════════
# ETAPA 5 — Execute e analise
# ══════════════════════════════════════════════

if __name__ == "__main__":
    np.random.seed(42)

    plotar_funcao()

    # TODO: chame simulated_annealing com as funções do problema
    # solucao, custo, historico = simulated_annealing(...)

    # TODO: decodifique a solução e imprima x e f(x)

    # TODO: marque o ponto encontrado no gráfico de f(x)

    # TODO: plote a curva de convergência (historico)

    # ── DESAFIO EXTRA ──────────────────────────────────────
    # Rode com N_BITS = 8 e N_BITS = 24. O que muda na qualidade?
