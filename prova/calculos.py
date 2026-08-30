#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculos.py — verificacao numerica de todos os numeros citados em
`prova/viagem-no-tempo.html`.

Rode com:  python3 prova/calculos.py

Nao ha dependencias externas: apenas a biblioteca padrao. Cada bloco imprime
o numero que aparece no documento, de modo que qualquer afirmacao quantitativa
do texto possa ser conferida linha a linha.

Unidades SI salvo indicacao contraria. Constantes: CODATA 2018 / IAU 2015.
"""

from math import sinh, cosh, tanh, sqrt, exp, pi, log, asinh

# --------------------------------------------------------------------------
# Constantes
# --------------------------------------------------------------------------
c     = 2.99792458e8        # m/s        (exata, por definicao do metro)
G     = 6.67430e-11         # m^3/kg/s^2
hbar  = 1.054571817e-34     # J s
g0    = 9.80665             # m/s^2      (gravidade padrao, exata)
M_sun = 1.98892e30          # kg
M_jup = 1.89813e27          # kg
GM_E  = 3.986004418e14      # m^3/s^2    (WGS-84)
R_E   = 6.371e6             # m          (raio medio)
yr    = 3.15576e7           # s          (ano juliano, 365.25 d)
day   = 86400.0             # s
ly    = c * yr              # m
l_P   = sqrt(hbar * G / c**3)   # comprimento de Planck

SEP = "-" * 74


def head(n, title):
    print("\n" + SEP)
    print(f"[{n}] {title}")
    print(SEP)


# ==========================================================================
head("1", "A constante do foguete de 1 g:  c/g")
# ==========================================================================
# Sob aceleracao propria constante a, a hiperbole de Rindler da
#   t(tau) = (c/a) sinh(a tau / c)
#   x(tau) = (c^2/a) [cosh(a tau / c) - 1]
# A escala natural do problema e c/a. Para a = g ela vale quase exatamente
# um ano — a coincidencia que torna o foguete de 1 g tao elegante.
T_g = c / g0                    # segundos
print(f"c/g = {T_g:.4e} s = {T_g/yr:.4f} ano")
print(f"c^2/g = {c**2/g0:.4e} m = {c**2/g0/ly:.4f} ano-luz")
K = T_g / yr                    # anos por unidade de rapidez
print(f"=> rapidez acumulada:  eta = a*tau/c = tau[anos] / {K:.4f}")


# ==========================================================================
head("2", "Foguete de 1 g — viagem so de ida (tabela do documento)")
# ==========================================================================
print(f"{'tau (ano)':>10} {'t Terra (ano)':>18} {'distancia (al)':>18} "
      f"{'1 - v/c':>13} {'gamma':>14}")
for tau in (1, 2, 5, 10, 20, 30):
    eta = tau / K
    t_terra = K * sinh(eta)
    x_dist  = K * (cosh(eta) - 1.0)
    # 1 - tanh(eta) satura em zero na dupla precisao a partir de eta ~ 19.
    # A forma equivalente 2/(e^{2eta}+1) e estavel e e a que o documento cita.
    um_menos_v = 2.0 / (exp(2 * eta) + 1.0)
    fmt = ",.2f" if t_terra < 1e5 else ".4g"
    print(f"{tau:>10} {t_terra:>18{fmt}} {x_dist:>18{fmt}} "
          f"{um_menos_v:>13.3e} {cosh(eta):>14,.4g}")

# Ida e volta em quatro fases iguais (acelera, freia, volta, freia):
#   t_total = 4 (c/a) sinh(a tau_total / 4c)
print()
for tau_total in (20, 40, 60):
    eta_fase = (tau_total / 4) / K
    t_terra = 4 * K * sinh(eta_fase)
    print(f"ida e volta: {tau_total} anos de bordo  ->  "
          f"{t_terra:>14,.0f} anos na Terra")


# ==========================================================================
head("3", "O preco: equacao do foguete relativistico")
# ==========================================================================
# Para um foguete de fotons (exaustao a c, eficiencia perfeita), a razao de
# massas e M_i/M_f = exp(Delta eta), somando a rapidez de TODAS as fases.
for rotulo, fases, tau_total in (
        ("ida 10 anos (acelera + freia)", 2, 10),
        ("ida e volta 40 anos (4 fases)", 4, 40)):
    eta_fase = (tau_total / fases) / K
    razao = exp(fases * eta_fase)
    print(f"{rotulo}: Delta eta = {fases*eta_fase:.2f}, "
          f"M_i/M_f = {razao:.3e}")
    print(f"    combustivel para 1 t de carga util: {razao*1000:.2e} kg "
          f"({razao*1000/9.39e20:.3g} x a massa de Ceres)")


# ==========================================================================
head("4", "GPS — a correcao relativistica que seu celular usa")
# ==========================================================================
r_sat = 2.65600e7               # m, semieixo maior da orbita GPS
v_sat = sqrt(GM_E / r_sat)      # m/s, orbita circular
print(f"raio orbital = {r_sat:.4e} m,  v = {v_sat:.1f} m/s")

# Termo gravitacional: relogio no alto corre MAIS RAPIDO
grav = (GM_E / c**2) * (1.0 / R_E - 1.0 / r_sat)
# Termo cinematico: relogio em movimento corre MAIS DEVAGAR
cine = v_sat**2 / (2 * c**2)
print(f"gravitacional : +{grav*day*1e6:.2f} us/dia")
print(f"cinematico    : -{cine*day*1e6:.2f} us/dia")
liq = (grav - cine) * day
print(f"LIQUIDO       : +{liq*1e6:.2f} us/dia  (satelite adianta)")
print(f"erro de posicao se ignorado: {liq*c/1000:.2f} km/dia")


# ==========================================================================
head("5", "Estacao Espacial — viagem ao futuro ja realizada por humanos")
# ==========================================================================
h_iss, v_iss = 4.20e5, 7660.0
r_iss = R_E + h_iss
gr = (GM_E / c**2) * (1.0 / R_E - 1.0 / r_iss)
ci = v_iss**2 / (2 * c**2)
taxa = ci - gr                                 # relogio a bordo atrasa
print(f"taxa liquida = {taxa:.4e} s/s (a bordo atrasa)")
# O recorde de tempo acumulado em orbita mudou: Oleg Kononenko ultrapassou
# Gennady Padalka em fevereiro de 2024 e encerrou a quinta missao com ~1111
# dias. Padalka fica como referencia historica.
for nome, dias in (("Padalka  (878 d, ex-recorde)", 878),
                   ("Kononenko (1111 d, recorde)", 1111)):
    print(f"  {nome:<30} -> {taxa*dias*day*1000:>5.1f} ms para o futuro")


# ==========================================================================
head("6", "Relogio optico do NIST: dilatacao gravitacional em 33 cm")
# ==========================================================================
h = 0.33
print(f"Delta nu/nu = g h / c^2 = {g0*h/c**2:.3e}   (Chou et al., 2010)")


# ==========================================================================
head("7", "Buraco negro: o que custa fazer 1 hora valer 7 anos")
# ==========================================================================
# Schwarzschild estatico:  dtau/dt = sqrt(1 - r_s/r)
fator = 7 * 365.25 * 24 / 1.0        # 7 anos por hora
print(f"fator pedido = {fator:,.0f}")
razao = 1.0 / fator
r_sobre_rs = 1.0 / (1.0 - razao**2)  # de sqrt(1 - rs/r) = 1/fator
excesso = r_sobre_rs - 1.0
M = 1e8 * M_sun
r_s = 2 * G * M / c**2
r = r_s * r_sobre_rs
print(f"buraco negro de 1e8 massas solares: r_s = {r_s:.4e} m")
print(f"r/r_s = 1 + {excesso:.4e}")

# ATENCAO. r - r_s e uma diferenca de COORDENADA de Schwarzschild, nao uma
# distancia medida com regua. Perto do horizonte a metrica estica o radial
# de forma brutal, e as duas diferem por cinco ordens de grandeza.
print(f"\n  r - r_s (coordenada, NAO e distancia) = {excesso*r_s:.1f} m")


def dist_propria(r, r_s):
    """Integral exata de dr/sqrt(1 - r_s/r) do horizonte ate r."""
    return sqrt(r * (r - r_s)) + r_s * log((sqrt(r - r_s) + sqrt(r)) / sqrt(r_s))


L = dist_propria(r, r_s)
print(f"  distancia PROPRIA ate o horizonte      = {L:.4e} m = {L/1000:,.0f} km")
print(f"  (aprox. de horizonte proximo, 2 r_s sqrt(eps) = {2*r_s*sqrt(excesso)/1000:,.0f} km)")

# Aceleracao propria necessaria para permanecer estatico (nao cair):
#   a = (GM/r^2) / sqrt(1 - r_s/r)
a_estatico = (G * M / r**2) / sqrt(1 - r_s / r)
print(f"\n  aceleracao propria para PAIRAR        = {a_estatico:.4e} m/s^2")
print(f"                                        = {a_estatico/g0:.3e} g")
print("  => pairar ali nao e 'de graca': custa ~950 milhoes de g de empuxo,")
print("     nove ordens de grandeza pior que o foguete de 1 g do bloco 2.")
print("  => a rota viavel e QUEDA LIVRE: uma orbita circular estavel em torno")
print("     de um Kerr quase extremo, onde a aceleracao propria e zero. E a")
print("     construcao de Thorne para o planeta de Miller, e exige spin a")
print("     menos de ~1e-14 do valor extremo.")


# ==========================================================================
head("7b", "Assintota da hiperbole de Rindler (horizonte do bloco 2)")
# ==========================================================================
# Com x = K(cosh n - 1) e ct = K sinh n, temos ct - x -> K, e nao 0.
# Logo a assintota e a reta  ct = x + K,  deslocada de K em relacao a reta
# de 45 graus que passa pela origem. A reta ct = x NAO e o horizonte: e
# apenas o raio de luz emitido no evento de partida, que ULTRAPASSA a nave.
print("ct - x ao longo da trajetoria, para rapidez crescente:")
for n in (1, 3, 6, 10, 20):
    print(f"  eta = {n:>2}  ->  ct - x = {K*sinh(n) - K*(cosh(n)-1):.6f}")
print(f"limite = K = c/g = {K:.6f} ano-luz")
print("=> horizonte de Rindler:  ct = x + K   (nao  ct = x)")


# ==========================================================================
head("8", "Godel (1949) — a curva fechada de tipo tempo, explicitamente")
# ==========================================================================
# Metrica de Godel em coordenadas cilindricas:
#   ds^2 = 4a^2 [ -dt^2 + dr^2 - (sinh^4 r - sinh^2 r) dphi^2
#                 + 2 sqrt(2) sinh^2 r dphi dt + dz^2 ]
# A curva t, r, z fixos e phi em [0, 2pi) e FECHADA. Seu vetor tangente e
# d/dphi, cuja norma ao quadrado e g_phiphi:
#   g_phiphi = 4a^2 sinh^2(r) [1 - sinh^2(r)]
# Assinatura (-,+,+,+): g_phiphi < 0  <=>  tangente de tipo TEMPO.
def g_phiphi(r, a=1.0):
    s2 = sinh(r) ** 2
    return 4 * a * a * s2 * (1.0 - s2)

r_c = asinh(1.0)
print(f"raio critico: r_c = arcsinh(1) = ln(1+sqrt2) = {r_c:.6f}")
print(f"conferencia: ln(1+sqrt(2)) = {log(1+sqrt(2)):.6f}")
print()
print(f"{'r':>8} {'g_phiphi/a^2':>16}  tipo da curva fechada")
for r in (0.30, 0.60, r_c, 1.00, 1.50, 2.00):
    v = g_phiphi(r)
    if abs(v) < 1e-12:
        tipo = "NULA  (fronteira)"
    elif v > 0:
        tipo = "espaco  (curva comum)"
    else:
        tipo = "TEMPO  <-- CTC"
    print(f"{r:>8.4f} {v:>16.6f}  {tipo}")

# Tempo proprio gasto ao percorrer a volta completa, para r > r_c:
#   Delta tau = 2 pi * 2a sinh(r) sqrt(sinh^2 r - 1)
print()
print("tempo proprio de uma volta completa (em unidades de a):")
for r in (1.00, 1.50, 2.00):
    s = sinh(r)
    print(f"  r = {r:.2f} -> Delta tau = {2*pi*2*s*sqrt(s*s-1):.4f} a  "
          f"(finito e positivo: a viagem se completa)")


# ==========================================================================
head("9", "Buraco de minhoca: o orcamento de energia negativa")
# ==========================================================================
# Escala de massa exotica para uma garganta de raio b0:  |M| ~ b0 c^2 / G
for b0 in (1.0, 100.0, 1e3):
    M_ex = b0 * c**2 / G
    print(f"garganta b0 = {b0:>6.0f} m -> |M| ~ {M_ex:.3e} kg negativos "
          f"= {M_ex/M_jup:.2f} massas de Jupiter")

# Efeito Casimir: energia negativa MEDIDA em laboratorio.
#   <T_00> = -pi^2 hbar c / (720 a^4)
print()
for a_gap in (1e-6, 1e-7):
    rho = -pi**2 * hbar * c / (720 * a_gap**4)
    print(f"Casimir, placas a {a_gap*1e9:.0f} nm: rho = {rho:.3e} J/m^3 "
          f"(NEGATIVA, medida por Lamoreaux 1997)")

# Limite de Ford-Roman para a casca de materia exotica (ordem de grandeza)
print()
print(f"comprimento de Planck: l_P = {l_P:.4e} m")
for b0 in (1.0, 1e3):
    print(f"  garganta {b0:>6.0f} m -> casca exotica ~ sqrt(l_P b0) = "
          f"{sqrt(l_P*b0):.2e} m")
print(f"  (raio do proton = 8.4e-16 m, ou seja "
      f"{8.4e-16/sqrt(l_P*1.0):.0f}x mais espesso)")


# ==========================================================================
head("10", "Morris-Thorne-Yurtsever: ligando a maquina do tempo")
# ==========================================================================
# Bocas A e B separadas por L. Boca B faz uma viagem relativistica e
# envelhece menos. O deslocamento temporal acumulado atraves da garganta e
#   Delta = T (1 - 1/gamma)
# A maquina passa a existir (surgem CTCs) quando Delta >= L/c.
L = 10.0
v = 0.9999 * c
gamma = 1.0 / sqrt(1 - (v / c) ** 2)
T = 1.0 * yr
Delta = T * (1 - 1 / gamma)
print(f"bocas separadas por L = {L:.0f} m  ->  limiar L/c = {L/c*1e9:.1f} ns")
print(f"boca B a v = 0.9999c: gamma = {gamma:.2f}")
print(f"A envelhece {T/yr:.0f} ano; B envelhece {T/gamma/day:.2f} dias")
print(f"deslocamento Delta = {Delta/day:.1f} dias = {Delta/(L/c):.3e} x L/c")
print(f"=> CTCs existem. Alcance maximo para o passado: {Delta/day:.1f} dias")
print("=> e NUNCA antes do instante em que Delta cruzou L/c: a maquina nao")
print("   alcanca um passado anterior a si mesma. (Teorema, nao opiniao.)")


# ==========================================================================
head("11", "Muons: dilatacao temporal medida a 0,2 %")
# ==========================================================================
tau_0 = 2.1969811e-6            # s, vida media do muon em repouso
print(f"vida media em repouso: {tau_0*1e6:.4f} us  (c*tau_0 = {c*tau_0:.1f} m)")
gamma_cern = 29.327             # anel de armazenamento do CERN, 1977
print(f"CERN 1977, gamma = {gamma_cern}: vida media prevista = "
      f"{gamma_cern*tau_0*1e6:.2f} us")
print("medida compativel com a previsao dentro de 2e-3. O muon literalmente")
print(f"viveu {gamma_cern:.1f} vezes mais por estar em movimento.")


print("\n" + SEP)
print("Fim. Todos os numeros do documento saem daqui.")
print(SEP)
