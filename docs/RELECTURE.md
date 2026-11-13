# Consignes de relecture d'un chapitre

Le livre est décrit dans `GABARIT.md` (dossier docs/) : lis-le d'abord. Tu relis **un seul
chapitre** (les fichiers `src/<NN>-*.md`) et tu fais trois choses, dans cet ordre.

## 1. Vérifier les règles sur le web

- Pour chaque jeu, vérifie avec WebSearch / WebFetch (ou l'agent `web-fetch` si tu n'as pas
  WebFetch) les **points incertains listés dans ta consigne**, puis tout chiffre ou règle qui
  te paraît douteux en relisant (barèmes, nombre de cartes distribuées, valeurs, dates,
  auteurs). Sources à privilégier : pagat.com (référence des jeux traditionnels), les
  fédérations (FFB pour le bridge, FFT pour le tarot, FFBelote…), BoardGameGeek et les règles
  des éditeurs pour les jeux modernes, Wikipédia en recoupement.
- Corrige le texte directement (Edit). Quand les sources divergent, garde la règle la plus
  courante et mentionne l'autre comme variante. Si un point reste invérifiable, laisse ou
  rends la formulation prudente.
- Ne réécris pas ce qui est juste : on corrige, on n'élague pas. Garde le style et la longueur.

## 2. Ajouter un aide-mémoire à chaque fiche

Juste **avant** `### Verdict`, ajoute une section :

```
### Aide-mémoire

- **Cartes :** 32 cartes ; à l'atout V 20, 9 14, As 11, 10 10, R 4, D 3 ; hors atout As 11, 10 10…
- **Donne :** 3 puis 2 cartes, retourne, puis 3 (ou 2) au preneur…
- **Obligations :** fournir ; couper ; monter à l'atout…
- **Points :** 162 par donne, dix de der…
- **Fin de partie :** 1 000 ou 2 000 points.
```

5 à 10 puces très denses, faites pour être consultées en pleine partie : ordre et valeur des
cartes, distribution, obligations, barème, fin de partie. Uniquement ce qui sert à jouer.

## 3. Transformer les renvois en liens

Chaque fiche de jeu aura un identifiant `#jeu-<slug>` : le nom du titre `##`, sans accents,
en minuscules, où chaque suite de caractères non alphanumériques devient un seul `-` (sans `-`
au début ni à la fin). Exemples : « Belote coinchée / Contrée » → `#jeu-belote-coinchee-contree`,
« 6 qui prend ! » → `#jeu-6-qui-prend`, « Dame de pique » → `#jeu-dame-de-pique`.

Quand le texte renvoie à un autre jeu qui a sa fiche dans le livre (« voir la Belote »,
« cousin du Whist », « traité au chapitre des patiences »), transforme le nom en lien Markdown :
`[Belote](#jeu-belote)`. Seulement pour les **renvois explicites**, une ou deux fois par fiche
au plus, pas pour chaque mention. Liste des fiches du livre : lance
`grep -h '^## ' src/0[1-9]-*.md` depuis le dossier du livre. N'ajoute **pas** d'id aux
titres, le script de construction s'en charge.

## Règles

- Ne touche qu'aux fichiers de ton chapitre.
- Pas de `####`, pas de HTML, pas d'emoji.
- Compte rendu final, court : les corrections de règles faites (jeu, avant → après, source),
  les points restés invérifiables, le nombre d'aide-mémoires ajoutés, le nombre de liens.
