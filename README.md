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
| **Teorema II** | As equações **clássicas** de Einstein admitem soluções exatas contendo curvas fechadas de tipo tempo | **Demonstrado como teorema** (Gödel, 1949) |

O Teorema II é deliberadamente estreito, e o documento insiste nisso: ele diz
o que as equações de campo admitem, não que a viagem ao passado seja
fisicamente realizável. A distância entre as duas coisas é grande e está
inteira em aberto — criação e estabilidade de uma garganta atravessável, as
desigualdades quânticas de Ford–Roman, a mudança de topologia, a retroação
quântica no horizonte de Cauchy. O § 11 traz o placar linha a linha, com cinco
itens marcados "em aberto".

## O que tem aqui

```
prova/
  viagem-no-tempo.html   o documento
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

Cobre a constante `c/g`, a tabela do foguete de 1 g (inclusive a coluna
`1 − v/c`, que exige forma estável porque a dupla precisão satura em zero), a
equação do foguete relativístico, as correções relativísticas do GPS, o
deslocamento temporal acumulado por Oleg Kononenko em órbita, a distância
própria e a aceleração de sustentação perto de um horizonte de Schwarzschild,
a assíntota da hipérbole de Rindler, a mudança de sinal de `g_φφ` na métrica de
Gödel, o orçamento de energia negativa de um buraco de minhoca e o limiar de
acionamento da máquina de Morris–Thorne–Yurtsever.

### `viagem-no-tempo.html`

Não carrega **script de terceiros**: as 143 equações estão embutidas como SVG,
pré-renderizadas na build. O próprio documento tem, sim, um `<script>` inline
que desenha os três diagramas em canvas, a partir das mesmas fórmulas do texto
— nenhum deles é ilustrativo. A única requisição externa é a folha de estilo do
Google Fonts, que degrada para as fontes de sistema declaradas.

O arquivo é escrito para o runtime de Artifacts, que injeta o
`<!doctype html>`, o `<head>`, o charset e a meta viewport ao publicar. Por
isso ele começa direto no conteúdo. Aberto localmente como arquivo solto, o
navegador entra em modo quirks e sem viewport a folha de estilo responsiva não
se aplica como projetada — envolva-o num HTML mínimo para inspecionar fora do
Artifact.

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
