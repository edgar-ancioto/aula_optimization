"""
LAB 2 — Simulated Annealing: TSP com instância real ulysses16 (TSPLIB95)
=========================================================================
Sequência do Lab 1 (lab1_sa_binario.py).

O núcleo simulated_annealing() é importado diretamente do Lab 1.
O que muda aqui são apenas as 3 funções do problema:
    - p2_inicial  : permutação aleatória das 16 cidades
    - p2_vizinho  : troca dois índices (swap)
    - p2_objetivo : distância total do circuito

Instância: ulysses16 — 16 cidades com coordenadas geográficas reais
           representando paradas da Odisseia de Ulisses no Mediterrâneo.
Ótimo conhecido: 6859  (fonte: TSPLIB95, Groetschel/Padberg)
"""

import numpy as np
import matplotlib.pyplot as plt

# Importa o núcleo SA do Lab 1 — não copiamos, reutilizamos
from lab1_sa_binario import simulated_annealing


# ──────────────────────────────────────────────
# INSTÂNCIA ulysses16 — coordenadas (lat, lon)
# ──────────────────────────────────────────────

CIDADES = np.array([
    [38.24, 20.42], [39.57, 26.15], [40.56, 25.32], [36.26, 23.12],
    [33.48, 10.54], [37.56, 12.19], [38.42, 13.11], [37.52, 20.44],
    [41.23,  9.10], [41.17, 13.05], [36.08, -5.21], [38.47, 15.13],
    [38.15, 15.35], [37.51, 15.17], [35.49, 14.32], [39.36, 19.56]
])

OTIMO_CONHECIDO = 6859
# Rota ótima (0-indexed) para referência visual
ROTA_OTIMA = np.array([0,13,12,11,6,5,14,4,10,8,9,15,2,1,3,7])
N = len(CIDADES)

# ──────────────────────────────────────────────
# DISTÂNCIA GEOGRÁFICA — fórmula TSPLIB GEO
# (coordenadas em graus decimais → distância em km)
# ──────────────────────────────────────────────

_PI  = 3.141592
_RRR = 6378.388

def _to_rad(coord):
    deg = int(coord)
    mn  = coord - deg
    return _PI * (deg + 5.0 * mn / 3.0) / 180.0

def geo_dist(c1, c2):
    """Distância inteira entre duas cidades (lat, lon) — padrão TSPLIB GEO."""
    lat1, lon1 = _to_rad(c1[0]), _to_rad(c1[1])
    lat2, lon2 = _to_rad(c2[0]), _to_rad(c2[1])
    q1 = np.cos(lon1 - lon2)
    q2 = np.cos(lat1 - lat2)
    q3 = np.cos(lat1 + lat2)
    return int(_RRR * np.arccos(0.5 * ((1.0 + q1)*q2 - (1.0 - q1)*q3)) + 1.0)

# Matriz de distâncias pré-calculada (evita recomputo a cada iteração)
DIST = np.array([[geo_dist(CIDADES[i], CIDADES[j])
                  for j in range(N)] for i in range(N)])


# ──────────────────────────────────────────────
# PROBLEMA 2 — TSP
# Representação: np.array de permutação de índices
# ──────────────────────────────────────────────

def p2_inicial():
    """Solução inicial: rota aleatória."""
    return np.random.permutation(N)


def p2_vizinho(sol):
    """Vizinhança: troca dois índices aleatórios (swap)."""
    nova = sol.copy()
    i, j = np.random.choice(N, size=2, replace=False)
    nova[i], nova[j] = nova[j], nova[i]
    return nova


def p2_objetivo(sol):
    """Custo: distância total do circuito fechado (usa matriz pré-calculada)."""
    return sum(DIST[sol[i], sol[(i+1) % N]] for i in range(N))


# ──────────────────────────────────────────────
# UTILITÁRIOS DE VISUALIZAÇÃO
# ──────────────────────────────────────────────

def plot_rota(ax, rota, titulo, cor="steelblue"):
    coords = CIDADES[rota]
    circuito = np.vstack([coords, coords[0]])          # fecha o circuito
    ax.plot(circuito[:, 1], circuito[:, 0], "-o",      # lon no eixo x, lat no y
            color=cor, markersize=5, linewidth=1.2)
    for i, (lat, lon) in enumerate(CIDADES):
        ax.annotate(str(i + 1), (lon, lat),
                    textcoords="offset points", xytext=(4, 3), fontsize=7)
    dist = p2_objetivo(rota)
    gap  = (dist - OTIMO_CONHECIDO) / OTIMO_CONHECIDO * 100
    ax.set_title(f"{titulo}\ndist={dist:.0f}  |  gap={gap:.1f}%  (ótimo={OTIMO_CONHECIDO})")
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.grid(True, linestyle="--", alpha=0.3)


# ──────────────────────────────────────────────
# EXECUÇÃO E VISUALIZAÇÃO
# ──────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)

    # --- Mapa das cidades ---
    fig0, ax0 = plt.subplots(figsize=(7, 5))
    ax0.scatter(CIDADES[:, 1], CIDADES[:, 0], color="steelblue", s=60, zorder=3)
    for i, (lat, lon) in enumerate(CIDADES):
        ax0.annotate(str(i + 1), (lon, lat),
                     textcoords="offset points", xytext=(5, 4), fontsize=8)
    ax0.set_title("ulysses16 — 16 cidades no Mediterrâneo")
    ax0.set_xlabel("Longitude"); ax0.set_ylabel("Latitude")
    ax0.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

    # --- Rota inicial (baseline) ---
    rota_inicial = p2_inicial()
    dist_inicial = p2_objetivo(rota_inicial)
    print(f"Distância inicial (aleatória): {dist_inicial:.0f}")

    # --- Rodar o SA ---
    solucao, custo_sa, historico = simulated_annealing(
        p2_inicial, p2_vizinho, p2_objetivo,
        T0=1000, T_min=1e-3, alpha=0.995, n_iter=200
    )
    gap = (custo_sa - OTIMO_CONHECIDO) / OTIMO_CONHECIDO * 100
    melhoria = (dist_inicial - custo_sa) / dist_inicial * 100

    print(f"Distância SA            : {custo_sa:.0f}")
    print(f"Ótimo conhecido         : {OTIMO_CONHECIDO}")
    print(f"Gap de otimalidade      : {gap:.1f}%")
    print(f"Melhoria vs. aleatória  : {melhoria:.1f}%")

    # --- Visualização comparativa ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    plot_rota(axes[0], rota_inicial, "Rota inicial (aleatória)", cor="gray")
    plot_rota(axes[1], solucao,      "Rota SA",                  cor="seagreen")

    axes[2].plot(historico, color="seagreen", linewidth=0.7)
    axes[2].axhline(OTIMO_CONHECIDO, color="tomato", linestyle="--",
                    linewidth=1, label=f"Ótimo = {OTIMO_CONHECIDO}")
    axes[2].set_title("Curva de convergência")
    axes[2].set_xlabel("Iteração"); axes[2].set_ylabel("Distância")
    axes[2].legend()

    plt.tight_layout()
    plt.show()

    # ── EXPERIMENTO: efeito da vizinhança ───────────────────────────
    # Descomente para comparar swap vs. 2-opt em aula:
    #
    # def p2_vizinho_2opt(sol):
    #     nova = sol.copy()
    #     i, j = sorted(np.random.choice(N, size=2, replace=False))
    #     nova[i:j+1] = nova[i:j+1][::-1]   # inverte segmento
    #     return nova
    #
    # sol2, custo2, _ = simulated_annealing(
    #     p2_inicial, p2_vizinho_2opt, p2_objetivo,
    #     T0=1000, T_min=1e-3, alpha=0.995, n_iter=200
    # )
    # print(f"SA com 2-opt: {custo2:.0f}  (gap={((custo2-OTIMO_CONHECIDO)/OTIMO_CONHECIDO*100):.1f}%)")
