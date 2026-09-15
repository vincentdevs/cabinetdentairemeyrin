# Cabinet Dentaire Meyrin et Nyon, un site, quatre versions, deux langues

Un seul site pour le Cabinet Dentaire, avec ses deux cabinets (Meyrin, vérifié, et Nyon, encore à confirmer), construit à partir des mêmes informations et de la même architecture, puis habillé de deux identités visuelles. Chaque habillage peut devenir le site final tel quel.

- **A1 et A2, les bleus** (`/version-a1/`, `/version-a2/`) : blanc chaud, bleu pâle, pétrole. Newsreader pour les titres, Instrument Sans pour le texte. Angles droits, filets fins. Le hero porte une vraie photo du cabinet, la salle de soins pour A1, le fauteuil et l'écran pour A2.
- **B1 et B2, rose et bleu** (`/version-b1/`, `/version-b2/`) : crème, cobalt, turquoise, rose. Bricolage Grotesque pour les titres, DM Sans pour le texte. Angles arrondis, boutons pilule, cartes blanches sur fonds teintés. Le hero porte une illustration vectorielle de la salle de soins, aux aplats doux pour B1, en blocs géométriques pour B2 (générées avec Gamma dans la palette, sources dans `site/assets/refs/gamma-*.jpg`, deux variantes bleues inutilisées y sont aussi).

## Construire et regarder

```bash
python3 site/build.py            # écrit dist/
python3 site/build.py --serve    # construit puis sert dist/ sur http://localhost:4821/
```

`dist/index.html` est la page de comparaison. Les deux sites partagent `dist/assets/` (polices auto-hébergées, photos en jpg et webp à 480, 960 et 1600 px).

Dépendance : Python 3 avec Pillow (`pip install pillow`) pour générer les variantes d'images.

## Ce qu'il y a dans chaque version

Chaque version existe en français (`/version-a/…`) et en anglais (`/version-a/en/…`), avec les mêmes routes et des liens `hreflang` croisés.

| Page | Chemin | Nombre |
| :--- | :--- | :--- |
| Accueil | `/` | 1 |
| Cabinets, choix et fiches | `/cabinets/`, `/cabinets/meyrin/`, `/cabinets/nyon/` | 3 |
| Soins, vue d'ensemble | `/soins/` | 1 |
| Familles de soins | `/soins/prevenir/`, `/soins/soigner/`, `/soins/restaurer/`, `/soins/harmoniser/` | 4 |
| Fiches de soin | `/soins/<soin>/` | 19 |
| Équipe et profils | `/equipe/`, `/equipe/<personne>/` | 7 |
| Première visite | `/premiere-visite/` | 1 |
| Formulaire patient | `/formulaire/` | 1 |
| Urgences | `/urgences/` | 1 |
| Blog et articles | `/blog/`, `/blog/<article>/` | 5 |
| Contact | `/contact/` | 1 |
| Informations légales, 404 | `/mentions-legales/`, `/404.html` | 2 |

Soit 46 pages par langue, 92 par version, 368 en tout, plus un index de recherche `search.json` par langue, `robots.txt` et `sitemap.xml`.

## Ce que les tours 3 et 4 ont ajouté

- **Accueil** : hero plein écran (titre, sous-titre, actions et accès rapides à gauche, illustration du cabinet à droite, dérivée de la photo de la salle de soins et déclinée dans chaque palette par `site/tools/illustrate.py`), puis le cabinet et sa façon de faire, l'équipe en résumé, ce qui nous distingue, les deux carrés de cabinets (photo, nom, adresse, « Contacter le cabinet de … », « Formulaire pour ce cabinet »), une section par famille de soins avec la liste de ce qui est pratiqué, la première visite, le blog et l'appel final.
- **Menus déroulants** Soins et Cabinets dans la barre, recherche à la loupe (Cmd ou Ctrl+K), sélecteur de langue, logo officiel en-tête et pied de page.
- **Pages cabinet** : informations pratiques, plan, espaces, soins pratiqués sur place, bloc contact ancré (`#contact`) avec téléphone, courriel, réservation et formulaire pré-rempli pour ce cabinet.
- **Fiches de soin** : bloc « En pratique » (rendez-vous, devis et financement, accident, lieu) avec les réserves à confirmer, emplacement vidéo.
- **Blog** : index et quatre articles, FR et EN.
- **Contact** : les deux cabinets avec leurs moyens, puis un formulaire nom, courriel, téléphone, cabinet facultatif, motif, message.
- **Formulaire patient** (`/formulaire/`) : six étapes, brouillon local, numéro AVS validé, nLPD, impression, envoi par messagerie.
- **Portraits** détourés et alignés sur la ligne des yeux dans des disques de couleur (`site/tools/portraits.py`).
- **Anglais** complet sous `/en/`.

## Où vivent les choses

```
site/
  build.py        construit les deux versions, génère les images responsives
  content.py      contenu partagé : coordonnées, équipe, familles, étapes, textes fixes
  content/        content-source.json, les fiches de soins et profils publiés par le cabinet (25 août 2026)
  render.py       gabarits communs aux deux versions et aux deux langues, avec les chaînes d'interface FR et EN
  content_en.py   contenu anglais (mêmes structures que content.py) ; content/content-en.json porte les fiches de soin traduites
  tools/          grade.py (étalonnage photo), portraits.py (détourage et alignement), duo.py (hero des deux médecins), yunet.onnx
  a/, b/          styles.css et favicon.svg de chaque version ; shared/script.js est commun
  tools/grade.py  applique le même étalonnage (hautes lumières chaudes, ombres bleutées) à toutes les photos
  assets/         polices, refs/ (les visuels fournis), stock/ (versions étalonnées), photos-graded/, team-graded/, illustrations/
```

## Ce qui est vérifié et ce qui ne l'est pas

Tout ce qui est factuel vient de la présentation publiée par le cabinet : équipe, diplômes, langues, adresse, horaires, téléphone, courriel, transports, accès. Les fiches de soins reprennent les textes déjà rédigés pour le cabinet.

Ce que le cabinet n'a pas confirmé reste entre crochets dans les pages, et doit être rempli ou retiré avant la mise en ligne :

- tout ce qui concerne Nyon : adresse, étage, horaires, arrêt, lignes, stationnement, équipe et photos (la photo affichée est marquée « Photo d'illustration »)
- les langues des deux assistantes, `[LANGUES À CONFIRMER]`
- l'orthodontie, `[ORTHODONTIE À CONFIRMER]`
- l'équipement et les protocoles d'hygiène, `[ÉQUIPEMENT À CONFIRMER]`, `[PROTOCOLE D'HYGIÈNE À CONFIRMER]`
- le numéro du service de garde, `[NUMÉRO DU SERVICE DE GARDE À CONFIRMER]`
- les informations légales, hébergeur, responsable de publication, protection des données

Il n'y a aucun avis patient, aucun chiffre, aucun prix et aucune promesse de résultat. Le formulaire de contact passe par `mailto:` et ne demande aucune donnée de santé ; il est prévu pour être branché sur un envoi serveur au moment du déploiement.

## Qualité

- Gate de mise en page (`design-layout-humanizer/scripts/check-layout.mjs`) : zéro signal mesurable à 1440, 768 et 390 px sur douze pages par version.
- Contraste AA sur le texte courant et les boutons dans les deux palettes, focus visible, navigation clavier, menu mobile fermable à la touche Échap, `prefers-reduced-motion` respecté.
- Schémas `Dentist`, `FAQPage`, `Person`, `MedicalWebPage`, balises Open Graph, canonical, sitemap.
- Images en `<picture>` webp + jpg avec `srcset`, `width` et `height`, chargement différé sous le pli, polices préchargées.
