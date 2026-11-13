# Consignes de rédaction — « Le grand livre des jeux de cartes »

Livre EPUB en **français** (pas d'écriture inclusive), lu sur une liseuse Kobo (écran 6 pouces,
noir et blanc). Il est généré par pandoc à partir de fichiers Markdown. Le lecteur veut un
ouvrage **très détaillé, généreux, agréable à lire** : assez de règles pour pouvoir jouer
réellement avec le livre seul, plus le contexte, la stratégie et les variantes.

## Exactitude

- Les règles doivent être justes. Quand une règle varie selon les régions ou les clubs, dis-le
  et donne la version la plus courante, puis les autres en variantes. N'invente jamais un
  détail : si tu n'es pas sûr d'un point précis, formule-le prudemment (« selon les tables… »).
- Les noms commerciaux de jeux modernes sont autorisés (c'est un livre personnel).

## Format Markdown (strict)

- Le fichier commence par `# <Titre du chapitre>` puis 2 à 4 paragraphes d'introduction à la
  famille de jeux (ce qui les rassemble, le vocabulaire propre, comment choisir parmi eux).
- Chaque jeu est un titre `## <Nom du jeu>`. Sous-sections en `###`. Rien en dessous de `###`
  (utilise du gras ou des listes si besoin).
- **Pas de tableaux larges** (écran étroit) ; un petit tableau de 2–3 colonnes est toléré pour
  les valeurs des cartes. **Pas d'emoji ni de symboles exotiques** (pas d'étoiles ★) : les
  polices de la liseuse ne les ont pas. Les symboles de couleur ♠ ♥ ♦ ♣ sont autorisés mais
  écris de préférence « pique, cœur, carreau, trèfle ».
- Pas de HTML, pas de liens externes.

## Fiche de chaque jeu (dans cet ordre)

```
## Nom du jeu

*Autres noms : …* (omettre si aucun)

- **Famille :** jeu de plis / rami / défausse / patience / …
- **Joueurs :** 2 à 4 (idéal : 4, en deux équipes de 2)
- **Matériel :** 1 jeu de 32 cartes ; bloc et crayon pour les scores ; jetons …
- **Durée d'une partie :** environ 30 à 45 min
- **Âge conseillé :** dès 10 ans
- **Diffusion :** Très répandu / Répandu / Régional (préciser où) / Niche
- **Hasard / réflexion :** ex. « 40 % hasard, 60 % réflexion » ou une phrase
- **Fun :** 4/5 — une demi-phrase qui justifie
- **Challenge :** 4/5 — une demi-phrase qui justifie

### En bref
Deux ou trois phrases : l'esprit du jeu, ce qui le rend unique.

### Histoire et origine
Origine, époque, anecdotes, où on y joue aujourd'hui.

### But du jeu

### Mise en place
Préparation du paquet (cartes retirées, ordre et valeur des cartes), distribution.

### Déroulement
Les règles complètes, pas à pas, de façon à pouvoir jouer. Listes numérotées bienvenues.

### Décompte des points
(si pertinent ; fin de partie)

### Conseils de stratégie
Plusieurs conseils concrets, du débutant au joueur confirmé.

### Variantes
Chaque variante en **gras** suivie de son explication ; préciser si elle change le nombre
de joueurs ou le matériel.

### Verdict
Pour qui, dans quelle situation, ce qui plaît, ce qui peut déplaire.
```

Barèmes : **Fun** = plaisir et ambiance autour de la table ; **Challenge** = profondeur de
réflexion, marge de progression (la Bataille vaut 0/5 : aucune décision). Sois honnête et
nuancé, n'attribue pas 4/5 à tout le monde.

Longueur visée : **500 à 1 000 mots par jeu majeur**, 250 à 500 pour les jeux secondaires.
Les jeux de niche intéressants méritent autant d'attention que les classiques.

## Organisation du fichier

Écris dans le dossier
`src/`
un ou plusieurs fichiers nommés `<NN>-<slug>-<k>.md` (k = 1, 2, 3… s'il faut découper pour
écrire en plusieurs fois ; ils seront concaténés dans l'ordre). Seul le fichier `-1` contient le
titre `#` du chapitre. Ne touche à aucun autre fichier. Les jeux couverts par d'autres
chapitres ne doivent pas avoir de fiche chez toi (tu peux y renvoyer en une phrase).

Quand tu as fini, relis ton fichier (structure des titres, fiche complète pour chaque jeu) et
réponds seulement par : la liste des jeux rédigés, le nombre de mots approximatif (`wc -w`),
et les points de règles dont tu n'es pas certain.
