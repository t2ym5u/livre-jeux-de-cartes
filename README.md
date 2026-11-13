# Le grand livre des jeux de cartes

Encyclopédie pratique de 169 jeux de cartes, en français : règles complètes, histoire,
stratégie, variantes, aide-mémoire, notes de fun et de challenge. Pensée pour une liseuse
(Kobo Aura, 758×1024 à 212 dpi).

## Organisation

- `src/` : les sources Markdown, un ou plusieurs fichiers par chapitre (`NN-slug-k.md`,
  concaténés dans l'ordre). `00*` = pages liminaires, `01`–`09` = chapitres de fiches,
  `90` = glossaire.
- `assets/` : couverture (SVG), feuille de style, métadonnées EPUB.
- `docs/` : consignes de rédaction (`GABARIT.md`) et de relecture (`RELECTURE.md`).
- `build.py` : construit le livre.
- `dist/` : les sorties, l'EPUB et une édition Markdown en un seul fichier.

## Construire

```bash
python3 build.py
```

Dépendances : `pandoc`, `rsvg-convert` (librsvg). Contrôle conseillé : `epubcheck dist/*.epub`.

Le script ajoute un identifiant `#jeu-<slug>` à chaque fiche, convertit les renvois
`[[Nom du jeu]]` ou `[[Nom du jeu|texte]]` en liens, signale les liens cassés (code de sortie
non nul), génère le chapitre d'index à partir des fiches, met en place les espaces insécables
de la typographie française et produit la couverture avec le nombre de jeux.

## Écrire une fiche

Suivre `docs/GABARIT.md` (ordre des rubriques, barèmes Fun / Challenge, pas de `####`, pas
d'emoji), puis ajouter l'aide-mémoire et les liens selon `docs/RELECTURE.md`. L'index et la
couverture se mettent à jour seuls.
