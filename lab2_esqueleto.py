"""
LAB 2 — Simulated Annealing: TSP com instância real ulysses16 (TSPLIB95)
=========================================================================
Sequência do Lab 1. O núcleo SA é importado diretamente — não reimplemente.
Siga os slides para implementar cada etapa na ordem indicada.

Instância: ulysses16 — 16 cidades, coordenadas geográficas reais (Mediterrâneo)
Ótimo conhecido: 6859
"""

import numpy as np
import matplotlib.pyplot as plt

# Importa o SA que você implementou no Lab 1
from lab1_esqueleto import simulated_annealing


# ══════════════════════════════════════════════
# DADOS — ulysses16 (não é necessário digitar)
# ══════════════════════════════════════════════

CIDADES = np.array([
    [38.24, 20.42], [39.57, 26.15], [40.56, 25.32], [36.26, 23.12],
    [33.48, 10.54], [37.56, 12.19], [38.42, 13.11], [37.52, 20.44],
    [41.23,  9.10], [41.17, 13.05], [36.08, -5.21], [38.47, 15.13],
    [38.15, 15.35], [37.51, 15.17], [35.49, 14.32], [39.36, 19.56]
])

OTIMO_CONHECIDO = 6859
N = len(CIDADES)


# ══════════════════════════════════════════════
# ETAPA 1 — Visualize a instância
# ══════════════════════════════════════════════

def plotar_cidades():
    """Plote as 16 cidades no mapa (lon no eixo x, lat no eixo y)."""
    # TODO: scatter plot das cidades com índices anotados
    pass


# ══════════════════════════════════════════════
# ETAPA 2 — Distância geográfica (fórmula GEO do TSPLIB)
# ══════════════════════════════════════════════

_PI  = 3.141592
_RRR = 6378.388  # raio da Terra (km)

def _to_rad(coord):
    """
    Converte grau decimal → radiano (padrão TSPLIB GEO).

    Fórmula (ver slide):
        deg = int(coord)
        min = coord - deg
        rad = PI * (deg + 5 * min / 3) / 180
    """
    # TODO: implemente a conversão
    pass


def geo_dist(c1, c2):
    """
    Distância inteira entre duas cidades c1=(lat,lon) e c2=(lat,lon).

    Fórmula (ver slide):
        q1 = cos(lon1 - lon2)
        q2 = cos(lat1 - lat2)
        q3 = cos(lat1 + lat2)
        d  = int( RRR * arccos( 0.5 * ((1+q1)*q2 - (1-q1)*q3) ) + 1 )
    """
    lat1, lon1 = _to_rad(c1[0]), _to_rad(c1[1])
    lat2, lon2 = _to_rad(c2[0]), _to_rad(c2[1])

    # TODO: calcule q1, q2, q3 e retorne a distância inteira
    pass


# Matriz de distâncias pré-calculada (evita recomputo a cada iteração)
# Descomente após implementar geo_dist:
# DIST = np.array([[geo_dist(CIDADES[i], CIDADES[j])
#                   for j in range(N)] for i in range(N)])


# ══════════════════════════════════════════════
# ETAPA 3 — Funções do problema TSP
# ══════════════════════════════════════════════

def p2_inicial():
    """Solução inicial: permutação aleatória dos índices das cidades."""
    # TODO: retorne np.random.permutation(N)
    pass


def p2_vizinho(sol):
    """
    Vizinhança: troca dois índices aleatórios (swap).
    Dica: escolha i, j com np.random.choice e troque nova[i] ↔ nova[j]
    """
    # TODO: implemente o swap
    pass


def p2_objetivo(sol):
    """Distância total do circuito fechado usando a matriz DIST."""
    # TODO: some DIST[sol[i], sol[(i+1) % N]] para i em range(N)
    pass


# ══════════════════════════════════════════════
# ETAPA 4 — Execute e calcule o gap
# ══════════════════════════════════════════════

def plotar_rota(ax, rota, titulo, cor="steelblue"):
    """Plota circuito no mapa com distância e gap no título."""
    coords  = CIDADES[rota]
    circuito = np.vstack([coords, coords[0]])
    ax.plot(circuito[:, 1], circuito[:, 0], "-o", color=cor, markersize=5)
    for i, (lat, lon) in enumerate(CIDADES):
        ax.annotate(str(i+1), (lon, lat),
                    textcoords="offset points", xytext=(4, 3), fontsize=7)
    dist = p2_objetivo(rota)
    gap  = (dist - OTIMO_CONHECIDO) / OTIMO_CONHECIDO * 100
    ax.set_title(f"{titulo}  |  dist={dist:.0f}  gap={gap:.1f}%")
    ax.grid(True, linestyle="--", alpha=0.3)


if __name__ == "__main__":
    np.random.seed(42)

    plotar_cidades()

    # TODO: gere a rota inicial e calcule a distância baseline

    # TODO: chame simulated_annealing com as funções do problema TSP
    # solucao, custo, historico = simulated_annealing(...)

    # TODO: imprima distância SA, ótimo e gap de otimalidade

    # TODO: plote rota inicial vs. rota SA lado a lado + curva de convergência

    # ── DESAFIO EXTRA ──────────────────────────────────────
    # Troque p2_vizinho por 2-opt (inverta um segmento da rota).
    # O gap melhora? Quanto?
