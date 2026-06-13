"""
LAB 1 — Simulated Annealing: representação binária para minimização de f(x)
============================================================================
Problema: encontrar o mínimo global de f(x) = x · sin(x) em [-20, 20]

Conceito central:
  A solução é sempre um np.ndarray.
  O núcleo do SA não muda entre problemas — só as 3 funções plugadas:
    - inicial_fn  : gera a solução inicial
    - vizinho_fn  : gera um vizinho da solução atual
    - objetivo_fn : calcula o custo (queremos minimizar)

No Lab 2 (lab2_tsp.py) vamos importar simulated_annealing daqui
e resolver o TSP trocando apenas essas 3 funções.
"""

import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# NÚCLEO GENÉRICO — reutilizado no Lab 2
# ──────────────────────────────────────────────

def simulated_annealing(inicial_fn, vizinho_fn, objetivo_fn,
                        T0=1000.0, T_min=1e-3, alpha=0.995, n_iter=200):
    """
    Simulated Annealing genérico.

    Parâmetros
    ----------
    inicial_fn  : () -> np.ndarray          gera solução inicial
    vizinho_fn  : (np.ndarray) -> np.ndarray gera solução vizinha
    objetivo_fn : (np.ndarray) -> float      calcula custo (minimizar)
    T0          : temperatura inicial
    T_min       : temperatura de parada
    alpha       : taxa de resfriamento (T = T * alpha a cada ciclo)
    n_iter      : iterações por nível de temperatura

    Retorna
    -------
    melhor       : np.ndarray   melhor solução encontrada
    melhor_custo : float
    historico    : list[float]  custo registrado a cada iteração
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
            # Aceita melhora sempre; piora com probabilidade e^(-delta/T)
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                atual = candidato
                custo_atual = custo_candidato

                if custo_atual < melhor_custo:
                    melhor = atual.copy()
                    melhor_custo = custo_atual

            historico.append(custo_atual)
        T *= alpha

    return melhor, melhor_custo, historico


# ──────────────────────────────────────────────
# PROBLEMA 1 — f(x) = x · sin(x), x em [-20, 20]
# Representação: vetor binário de N_BITS elementos
# ──────────────────────────────────────────────

N_BITS   = 16          # precisão: 2^16 = 65.536 valores distintos
X_MIN    = -20.0
X_MAX    =  20.0


def decodificar(sol):
    """Converte vetor binário para valor real em [X_MIN, X_MAX]."""
    inteiro = int("".join(sol.astype(str)), 2)
    return X_MIN + inteiro * (X_MAX - X_MIN) / (2**N_BITS - 1)


def p1_inicial():
    """Solução inicial: vetor binário aleatório."""
    return np.random.randint(0, 2, size=N_BITS)


def p1_vizinho(sol):
    """Vizinhança: flip de um bit aleatório."""
    nova = sol.copy()
    i = np.random.randint(0, len(nova))
    nova[i] = 1 - nova[i]
    return nova


def p1_objetivo(sol):
    """Custo: f(x) = x · sin(x) avaliado no x decodificado."""
    x = decodificar(sol)
    return x * np.sin(x)


# ──────────────────────────────────────────────
# EXECUÇÃO E VISUALIZAÇÃO
# ──────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)

    # --- Gráfico da função ---
    xs = np.linspace(X_MIN, X_MAX, 1000)
    ys = xs * np.sin(xs)

    plt.figure(figsize=(8, 3))
    plt.plot(xs, ys, color="steelblue")
    plt.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    plt.title("f(x) = x · sin(x)")
    plt.xlabel("x"); plt.ylabel("f(x)")
    plt.tight_layout()
    plt.savefig("grafico_fx.png", dpi=150)
    plt.show()

    # --- Rodar o SA ---
    solucao, custo, historico = simulated_annealing(
        p1_inicial,
        p1_vizinho,
        p1_objetivo,
        T0=500,
        T_min=1e-4,
        alpha=0.997,
        n_iter=100
    )
    x_encontrado = decodificar(solucao)

    print(f"\nSolução binária : {solucao}")
    print(f"x decodificado  : {x_encontrado:.4f}")
    print(f"f(x)            : {custo:.4f}")

    # --- Resultado no gráfico ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(xs, ys, color="steelblue", label="f(x)")
    ax1.scatter([x_encontrado], [custo], color="tomato", zorder=5,
                label=f"SA: x={x_encontrado:.2f}, f={custo:.2f}")
    ax1.axvline(x_encontrado, color="tomato", linestyle="--", linewidth=0.8)
    ax1.set_title("f(x) = x · sin(x) — solução encontrada")
    ax1.set_xlabel("x"); ax1.set_ylabel("f(x)")
    ax1.legend()

    ax2.plot(historico, color="steelblue", linewidth=0.7)
    ax2.set_title("Curva de convergência")
    ax2.set_xlabel("Iteração"); ax2.set_ylabel("Custo")

    plt.tight_layout()
    plt.show()

    # ── EXPERIMENTO: efeito de N_BITS na qualidade ──────────────────
    # Descomente para explorar em aula:
    #
    # for bits in [8, 12, 16, 20]:
    #     N_BITS = bits
    #     sol, c, _ = simulated_annealing(p1_inicial, p1_vizinho, p1_objetivo)
    #     print(f"N_BITS={bits:2d}  x={decodificar(sol):.4f}  f={c:.4f}")
