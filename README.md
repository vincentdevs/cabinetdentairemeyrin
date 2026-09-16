# Cabinet Dentaire Meyrin, ligne Reworked 1

Le site du Cabinet Dentaire, deux cabinets (Meyrin, vérifié, et Nyon, encore à
confirmer), 45 pages en français et les 45 mêmes en anglais, dans une seule
direction visuelle. Cette ligne est dérivée de la version élégante, les bleus,
et s'en sépare sur un point : la décoration dessinée a disparu.

## Ce qui change par rapport à la version dont elle vient

La version d'origine posait de petits dessins au trait dans les angles, une
dent dans le hero et en tête des pages intérieures, une courbe dans la bande
foncée et sous les questions fréquentes, un arc au-dessus de l'appel final.
Cinq motifs en tout, tous retirés.

Ce qui les remplace ne se dessine pas, cela se construit :

- **Un grain de papier** sur toute la page, à 5,5 % d'opacité en fusion
  multiply. Un aplat de couleur lit comme un remplissage d'écran, le même
  aplat sous un grain fin lit comme du papier couché. Un SVG en ligne, aucun
  fichier, aucun dégradé.
- **Des filets qui portent des numéros.** Chaque ouverture de section commence
  sur un filet qui traverse le conteneur, et les familles de soins portent leur
  numéro en chiffres tabulaires sur leur propre filet, comme un numéro de
  chapitre.
- **Une liste de soins devenue index.** Les mêmes lignes qu'avant, désormais
  numérotées, le numéro, le nom et le filet de la ligne passant au pétrole sous
  le curseur. Les chiffres viennent d'un compteur CSS, le balisage n'a pas
  bougé.
- **La photographie tenue dans un filet.** Un trait d'un pixel dessiné à
  l'intérieur du bord sépare l'image de la page sans l'encadrer. L'image est
  posée telle quelle, sans balayage ni mise à l'échelle.
- **Aucune animation au défilement.** Le contenu est présent à l'arrivée, rien
  n'apparaît en fondu, aucune image ne se met à l'échelle, l'en-tête garde le
  même filet du haut jusqu'au bas de la page. Le survol répond par la couleur,
  le nom d'un soin et le filet de sa ligne passent au pétrole, et rien ne se
  déplace. Les deux seules transitions qui restent disent un changement
  d'état : le trait du menu mobile qui devient une croix, et la flèche des
  questions fréquentes qui pivote.
- **Un index de tous les soins** ferme la page d'accueil : les 19 soins en
  trois colonnes, numérotés, sur filets. Un lecteur qui ne connaît pas le nom
  de ce qu'il cherche voit toute l'offre d'un coup.

Aucun dégradé, aucune icône dans un cercle, aucune forme flottante. Tout ce qui
est à l'écran pourrait être imprimé.

## Construire et regarder

```bash
python3 site/build.py            # écrit dist/
python3 site/build.py --serve    # construit puis sert dist/ sur http://localhost:4821/
```

Dépendance : Python 3 avec Pillow (`pip install pillow`) pour générer les
variantes d'images.

`dist/` n'est pas versionné. Le déploiement GitHub Pages reconstruit le site à
chaque push, puis rebase les chemins absolus sur le sous-chemin du dépôt avec
`site/tools/rebase_for_pages.py`.

## Les pages

Chaque page existe en français à la racine et en anglais sous `/en/`, avec les
mêmes routes et des liens `hreflang` croisés.

| Page | Chemin | Nombre |
| :--- | :--- | :--- |
| Accueil | `/` | 1 |
| Cabinets, choix et fiches | `/cabinets/`, `/cabinets/meyrin/`, `/cabinets/nyon/` | 3 |
| Soins, vue d'ensemble | `/soins/` | 1 |
| Familles de soins | `/soins/prevenir/`, `/soins/soigner/`, `/soins/restaurer/`, `/soins/harmoniser/` | 4 |
| Fiches de soin | `/soins/<soin>/` | 19 |
| Équipe et profils | `/equipe/`, `/equipe/<personne>/` | 7 |
| Première visite, urgences, contact, formulaire | | 4 |
| Blog, index et articles | `/blog/`, `/blog/<article>/` | 5 |
| Mentions légales | `/mentions-legales/` | 1 |

## Où se trouve quoi

| Chemin | Contenu |
| --- | --- |
| `site/content.py`, `site/content_en.py` | tout le texte, français et anglais |
| `site/content/` | les sources de contenu et les articles |
| `site/render.py` | la composition de chaque type de page |
| `site/a/styles.css` | la feuille de style, le bloc `REWORKED 1` en fin de fichier |
| `site/shared/script.js` | menu, menus déroulants, recherche, formulaire patient |
| `site/assets/` | polices, photographies, portraits |
| `site/tools/` | traitement des images et rebase pour GitHub Pages |

## Ce qui manque encore

Les informations que le cabinet n'a pas fournies portent un marqueur entre
crochets dans les pages, par exemple `[ADRESSE À CONFIRMER]`. Elles ne sont
jamais inventées. La liste complète, avec les prix, l'adresse de Nyon et les
titres et diplômes de l'équipe, vit dans le dépôt `cabinetdentairemeyrin-b`,
sous `key-information/`, avec en regard l'inventaire de tout le texte du site.
