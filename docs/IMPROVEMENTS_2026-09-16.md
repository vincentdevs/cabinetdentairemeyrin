# Reworked 1, séance du 16 septembre 2026

Point de départ : la version élégante du site (dépôt `cabinetdentairemeyrin`),
copiée telle quelle. Rien n'a changé dans le contenu, l'architecture, les
routes ni les traductions. Le travail porte uniquement sur la couche visuelle.

## Ce qui a été retiré

Cinq motifs au trait, dessinés en pseudo-éléments dans la feuille de style :

| Sélecteur | Motif | Où |
| --- | --- | --- |
| `.hero-full::after` | dent, filet pétrole, point turquoise | accueil, en haut à droite |
| `.phero:not(.phero-urg)::before` | dent, filet pétrole | toutes les pages intérieures |
| `.philo::after` | courbe de sourire | bande foncée de l'accueil |
| `.faq::before` | courbe de sourire | bas des questions fréquentes |
| `.close::after` | arc à graduations | au-dessus de l'appel final |

Ils sont neutralisés par `content: none` plutôt que supprimés, pour que la
comparaison avec la version d'origine reste lisible dans le diff.

## Ce qui a été ajouté

Le bloc `REWORKED 1`, en fin de `site/a/styles.css`, en onze sections
commentées. Les décisions qui comptent :

1. **Grain de papier** (`body::after`, SVG `feTurbulence` en ligne, opacité
   0,055, `mix-blend-mode: multiply`, `z-index: 200`, `pointer-events: none`).
   C'est le seul moyen de donner de la matière à un aplat sans dégradé. Retiré
   à l'impression.
2. **Filet d'ouverture** sur `.sec-head-split` et sur l'en-tête des soins, plus
   le numéro de famille (`.hfam-n`) passé en chiffres tabulaires letterspacés
   sur son propre filet.
3. **Index des soins** dans les sections familles. Le sélecteur porte
   l'ancêtre `.hfam-txt` parce qu'une règle plus spécifique écrite plus haut
   dans la feuille gagnait sinon et faisait passer les quatre éléments de la
   grille sur deux colonnes, ce qui mélangeait le numéro, le nom et la
   question. C'est le seul piège rencontré pendant la séance.
4. **Filet intérieur sur les photographies** (`::after` en `box-shadow: inset`)
   et pose lente de l'image en fin de révélation, de 1,045 à 1, au lieu du
   balayage abandonné au tour précédent.
5. **Interactions sur des lignes** : lien à deux filets superposés dont le
   second se trace au survol, bouton qui se remplit par le bas, en-tête qui
   gagne `backdrop-filter` et un filet au défilement.
6. **Index complet des soins** en clôture d'accueil, section `.tindex`, trois
   colonnes CSS, une entrée par soin, numérotée par compteur. Le balisage est
   généré dans `home()` à partir de `C.FAMILIES`, donc aucun nom n'est saisi
   deux fois.

## Contrôles passés

- Gate `check-layout.mjs` : 13 pages à 1440, 768 et 390 px, aucun signalement.
  Le gate refuse les dégradés, ce qui a orienté toute la direction vers le
  grain et les filets.
- Aucune page ne défile horizontalement à 390 px.
- Lecture des rendus à 1440 et 390 px : accueil, section famille, bande
  foncée, index des soins, fiche de soin.
- Mouvement désactivé sous `prefers-reduced-motion`.

## Ce qui reste ouvert

- Le grain est fixé à 5,5 %. Au-delà de 8 % il se voit sur les aplats clairs,
  en dessous de 3 % il ne sert plus à rien.
- Les portraits gardent leur cadrage rond hérité. Un cadrage carré irait mieux
  avec le système de filets, mais cela touche la production des images et non
  la feuille de style.
- L'index de clôture reprend les 19 soins. Si la liste dépasse la trentaine, il
  faudra le passer en deux colonnes par famille plutôt qu'en trois colonnes
  continues.


## Passe sobre, même séance

Demande : retirer les animations au défilement et rendre l'interface plus
minimale. Ce qui a été enlevé, et ce qui reste.

### Retiré du JavaScript

- Le système de révélation entier : l'`IntersectionObserver`, les classes `.r`
  et `.in` posées au défilement, et le filet de sécurité qui rattrapait les
  blocs oubliés. Sans révélation, il n'y a plus rien à rattraper.
- L'écouteur de défilement qui posait `.scrolled` sur l'en-tête.
- Le défilement animé vers l'étape suivante du formulaire patient, devenu
  instantané.

Il reste dans `script.js` ce qui rend le site utilisable : menu mobile, menus
déroulants, recherche, mémoire du cabinet choisi, et les six étapes du
formulaire patient avec la validation du numéro AVS.

### Retiré de la feuille de style

- `scroll-behavior: smooth` sur `html`.
- Les états `.js .r` et `.js .mask`, neutralisés en opacité 1, sans transform
  ni `clip-path`.
- Tous les zooms d'image au survol, sur les cartes de cabinet, les articles et
  les moitiés d'écran.
- Les blocs qui se soulevaient de 2 ou 3 px au survol.
- Le filet du lien qui se traçait, remplacé par un filet permanent qui passe
  de 45 % à 100 % d'opacité, et le remplissage du bouton qui montait par le
  bas, remplacé par le changement de fond.
- Le glissement de 4 px du nom d'un soin dans l'index.

### Vérifié après coup

- Aucun élément laissé invisible ou déplacé sur l'accueil, les soins,
  l'équipe, le blog et le formulaire, à 1440 et 390 px. Les seules opacités
  inférieures à 1 qui subsistent sont voulues : les radios personnalisées du
  formulaire, masquées derrière leur étiquette, et la légende vidéo à 85 et
  90 % sur son panneau foncé.
- Gate `check-layout.mjs` : 13 pages à 1440, 768 et 390 px, aucun signalement.
- Aucun défilement horizontal à 390 px.
