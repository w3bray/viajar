# viajar

Um documento sobre viagem no tempo levado a sério: com a métrica escrita, as
contas abertas e a distinção entre o que está provado, o que está em aberto e
o que está excluído.

**[`prova/viagem-no-tempo.html`](prova/viagem-no-tempo.html)** — o documento.

## O argumento, em duas frases

"Viagem no tempo" esconde duas proposições com status epistêmicos muito
diferentes, e confundi-las é o que faz a discussão descarrilar.

| | Afirmação | Status |
|---|---|---|
| **Teorema I** | Ir a um instante arbitrariamente distante no futuro gastando tempo próprio arbitrariamente curto | **Demonstrado.** Teoricamente em 1905, experimentalmente desde 1941, em operação comercial desde 1978 |
| **Teorema II** | As equações de Einstein admitem soluções exatas contendo curvas fechadas de tipo tempo | **Demonstrado como teorema** (Gödel, 1949). Realizabilidade física em aberto |

O Teorema II não afirma que existe uma máquina do tempo em algum lugar. Afirma
que a teoria da gravitação mais bem testada que temos não proíbe a viagem ao
passado — e que a impossibilidade, se houver, terá de vir de fora das equações
de campo.

## O que tem aqui

```
prova/
  viagem-no-tempo.html   o documento, autossuficiente
  calculos.py            verificação numérica de cada número citado
  build-math.js          pré-renderiza a matemática para SVG inline
```

### `calculos.py`

Nenhuma dependência além da biblioteca padrão. Cada bloco imprime os números
que aparecem no texto, para que qualquer afirmação quantitativa possa ser
conferida linha a linha:

```
python3 prova/calculos.py
```

Cobre a constante `c/g`, a tabela do foguete de 1 g, a equação do foguete
relativístico, as correções relativísticas do GPS, o deslocamento temporal
acumulado por Gennady Padalka na ISS, a mudança de sinal de `g_φφ` na métrica de
Gödel, o orçamento de energia negativa de um buraco de minhoca e o limiar de
acionamento da máquina de Morris–Thorne–Yurtsever.

### `viagem-no-tempo.html`

Não carrega nenhum script em tempo de execução. As 135 equações estão embutidas
como SVG e os três diagramas são desenhados em canvas a partir das mesmas
fórmulas do texto — nenhum é ilustrativo. A única requisição externa é a folha
de estilo do Google Fonts, que degrada para as fontes de sistema declaradas.

### `build-math.js`

Regenera as equações. É idempotente e o arquivo gerado é a própria fonte: cada
trecho guarda o TeX original em `data-tex`, então dá para editar uma equação
nesse atributo e reconstruir, sem manter um segundo arquivo.

```
npm install mathjax-full
node prova/build-math.js
```

## Referências

O documento traz bibliografia completa: Gödel (1949), Morris–Thorne (1988),
Morris–Thorne–Yurtsever (1988), Echeverría–Klinkhammer–Thorne (1991), Deutsch
(1991), Hawking (1992), Friedman–Schleich–Witt (1993), Alcubierre (1994),
Ford–Roman (1996), Kay–Radzikowski–Wald (1997), Aaronson–Watrous (2009), entre
outros.
