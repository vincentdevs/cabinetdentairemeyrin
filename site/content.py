"""Shared content for both directions of the Cabinet Dentaire Meyrin site.

Everything factual comes from the practice's own published material as
captured on 2026-08-25 (content/content-source.json). Anything the practice
has not confirmed stays a bracketed placeholder and is never filled in by
guesswork. No testimonials, no figures, no prices.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
SOURCE = json.load(open(HERE / "content" / "content-source.json", encoding="utf-8"))

DOMAIN = "https://www.cabinetdentairemeyrin.com"
NAME = "Cabinet Dentaire Meyrin"
PHONE = "022 320 19 19"
PHONE_INTL = "+41223201919"
TEL = "tel:+41223201919"
MAIL = "info.cabinetmeyrin@gmail.com"
ADDRESS = "Place de la Diversité 1"
ZIP_CITY = "1217 Meyrin"
FLOOR = "1er étage, sans marche à franchir"
HOURS = "Lundi au vendredi, 8h à 18h30"
STOP = "Meyrin, Hôpital de la Tour"
TRAM = "Tram 18"
BUS = "Bus 56, 57, 68, 71 et A3"
BOOKING = "https://rdv.dentagest.ch/fr/"
MAPS = "https://www.google.com/maps/search/?api=1&query=Place+de+la+Diversit%C3%A9+1+1217+Meyrin"
MAPS_EMBED = "https://www.google.com/maps?q=Place+de+la+Diversit%C3%A9+1,+1217+Meyrin&output=embed&hl=fr"
UPDATED = "25 août 2026"

# ------------------------------------------------------------------ navigation
NAV = [
    ("Accueil", "/"),
    ("Soins", "/soins/"),
    ("Équipe", "/equipe/"),
    ("Première visite", "/premiere-visite/"),
    ("Le cabinet", "/cabinet/"),
    ("Urgences", "/urgences/"),
    ("Contact", "/contact/"),
]

# ------------------------------------------------------------------ people
# Languages and biographies come from the practice's official presentation
# (content-source.json). The two assistants have no published profile, so their
# languages stay a placeholder.
PEOPLE = [
    dict(slug="victor-palmen", name="Victor Palmen", role="Médecin-dentiste", img="victor-palmen.jpg",
         langs="Français, allemand, anglais", source="victor-palmen",
         areas="Soins généraux, prévention, soins des enfants",
         short="Omnipratique, prévention et soins des enfants."),
    dict(slug="edouard-di-donna", name="Edouard Di Donna", role="Chirurgien oral", img="edouard-di-donna.jpg",
         langs="Français, italien, anglais", source="edouard-di-donna",
         areas="Chirurgie orale, stomatologie, implantologie",
         short="Chirurgie orale, stomatologie et implantologie."),
    dict(slug="cilien-prieu", name="Cilien Prieu", role="Médecin-dentiste", img="cilien-prieu.jpg",
         langs="Français, anglais, espagnol", source="cilien-prieu",
         areas="Contrôles, caries, prévention, soins des enfants",
         short="Contrôles, traitement des caries, prévention et soins des enfants."),
    dict(slug="juliana", name="Juliana", role="Hygiéniste dentaire", img="juliana.jpg",
         langs="Français, portugais, espagnol", source="juliana-hygieniste",
         areas="Hygiène professionnelle, détartrage, gencives",
         short="Hygiène professionnelle et soins des gencives."),
    dict(slug="zainne", name="Zainne", role="Assistante dentaire", img="zainne.jpg",
         langs="[LANGUES À CONFIRMER]", source=None,
         areas="Accueil, préparation du matériel, assistance au fauteuil",
         short="Accueil, préparation du matériel et assistance au fauteuil."),
    dict(slug="luana", name="Luana", role="Assistante dentaire", img="luana.jpg",
         langs="[LANGUES À CONFIRMER]", source=None,
         areas="Accueil, préparation du matériel, suivi du rendez-vous",
         short="Accueil, préparation du matériel et suivi du rendez-vous."),
]
P = {p["slug"]: p for p in PEOPLE}


def bio(person):
    """The published biography paragraphs, without the source and link lines."""
    if not person["source"]:
        return ["Le cabinet n’a pas publié de présentation détaillée. [BIOGRAPHIE À CONFIRMER]"]
    src = SOURCE["equipe"][person["source"]]
    out = [src["lead"]]
    for s in src["sections"]:
        if s["h"].startswith("Prendre"):
            continue
        for p in s["p"]:
            if p.startswith("Présentation officielle") or len(p) < 40:
                continue
            out.append(p)
    return out


# ------------------------------------------------------------------ cares
CARE_SHORT = {
    "controle-dentaire-meyrin": "Contrôle dentaire",
    "carie-dentaire-meyrin": "Carie dentaire",
    "traitement-racine-meyrin": "Traitement de racine",
    "dentiste-enfant-meyrin": "Dentiste pour enfants",
    "urgence-dentaire-meyrin": "Urgence dentaire",
    "hygieniste-dentaire-meyrin": "Rendez-vous chez l’hygiéniste",
    "detartrage-meyrin": "Détartrage",
    "soins-gencives-meyrin": "Soins des gencives",
    "implant-dentaire-meyrin": "Implant dentaire",
    "chirurgie-orale-meyrin": "Chirurgie orale",
    "dents-sagesse-meyrin": "Dents de sagesse",
    "extraction-dentaire-meyrin": "Extraction dentaire",
    "implant-ou-bridge": "Implant ou bridge",
    "dent-manquante": "Une dent manquante",
    "remplacer-plusieurs-dents": "Remplacer plusieurs dents",
    "couronne-dentaire-meyrin": "Couronne dentaire",
    "facettes-dentaires-meyrin": "Facettes dentaires",
    "blanchiment-dentaire-meyrin": "Blanchiment dentaire",
    "esthetique-dentaire-meyrin": "Blanchiment ou facettes",
}

CARE_IMG = {
    "controle-dentaire-meyrin": "stock/jeune-homme-sourire.jpg",
    "carie-dentaire-meyrin": "stock/examen-dentiste.jpg",
    "traitement-racine-meyrin": "stock/examen-proche.jpg",
    "dentiste-enfant-meyrin": "stock/enfant-examen.jpg",
    "urgence-dentaire-meyrin": "stock/examen-proche.jpg",
    "hygieniste-dentaire-meyrin": "stock/hygiene-jeune-homme.jpg",
    "detartrage-meyrin": "stock/hygiene-jeune-homme.jpg",
    "soins-gencives-meyrin": "stock/examen-dentiste.jpg",
    "implant-dentaire-meyrin": "stock/examen-proche.jpg",
    "chirurgie-orale-meyrin": "stock/hygiene-jeune-homme.jpg",
    "dents-sagesse-meyrin": "stock/jeune-homme-sourire.jpg",
    "extraction-dentaire-meyrin": "stock/examen-dentiste.jpg",
    "implant-ou-bridge": "stock/patiente-fauteuil.jpg",
    "dent-manquante": "stock/patiente-sourire.jpg",
    "remplacer-plusieurs-dents": "stock/patiente-fauteuil.jpg",
    "couronne-dentaire-meyrin": "stock/examen-proche.jpg",
    "facettes-dentaires-meyrin": "stock/patiente-sourire.jpg",
    "blanchiment-dentaire-meyrin": "stock/patiente-fauteuil.jpg",
    "esthetique-dentaire-meyrin": "stock/patiente-sourire.jpg",
}

# Treatments organised around what the patient needs, not around specialities.
FAMILIES = [
    dict(slug="prevenir", name="Prévenir", tone="mint", ill="toothbrush",
         line="Contrôles, hygiène et santé des gencives.",
         intro="Le contrôle repère ce qui ne fait pas encore mal, le rendez-vous d’hygiène retire ce que le brossage ne retire pas, et le suivi des gencives évite qu’une inflammation s’installe. Les enfants sont reçus pour un premier contrôle à leur rythme.",
         cares=["controle-dentaire-meyrin", "hygieniste-dentaire-meyrin", "detartrage-meyrin", "soins-gencives-meyrin", "dentiste-enfant-meyrin"],
         who=["victor-palmen", "cilien-prieu", "juliana"], img="stock/enfant-controle.jpg", alt="Enfant pendant un contrôle, rassuré par la dentiste"),
    dict(slug="soigner", name="Soigner", tone="turquoise", ill="tooth",
         line="Caries, traitements de racine et soins conservateurs.",
         intro="Une dent atteinte est examinée avant d’être traitée. Selon ce que montre l’examen, le soin va de l’obturation au traitement de racine, et la chirurgie orale prend le relais pour une extraction ou une dent de sagesse. Une douleur qui ne peut pas attendre est reçue en urgence.",
         cares=["carie-dentaire-meyrin", "traitement-racine-meyrin", "extraction-dentaire-meyrin", "dents-sagesse-meyrin", "chirurgie-orale-meyrin", "urgence-dentaire-meyrin"],
         who=["victor-palmen", "cilien-prieu", "edouard-di-donna"], img="stock/examen-dentiste.jpg", alt="Examen d’une patiente par la dentiste"),
    dict(slug="restaurer", name="Restaurer", tone="cobalt", ill="implant",
         line="Couronnes, prothèses et implants.",
         intro="Une dent très abîmée peut être protégée par une couronne, une dent manquante remplacée par un implant ou un bridge. Le chirurgien oral du cabinet pose les implants sur place, et le choix entre les solutions est expliqué avant de décider.",
         cares=["couronne-dentaire-meyrin", "implant-dentaire-meyrin", "implant-ou-bridge", "dent-manquante", "remplacer-plusieurs-dents"],
         who=["edouard-di-donna", "victor-palmen", "cilien-prieu"], img="stock/examen-proche.jpg", alt="Examen au miroir, gros plan"),
    dict(slug="harmoniser", name="Harmoniser", tone="pink", ill="braces",
         line="Esthétique dentaire, blanchiment et facettes.",
         intro="Le blanchiment agit sur la teinte des dents naturelles, les facettes corrigent une forme ou une couleur. Un bilan des dents et des gencives précède toujours la décision, parce que le résultat dépend de ce que l’examen montre.",
         cares=["blanchiment-dentaire-meyrin", "facettes-dentaires-meyrin", "esthetique-dentaire-meyrin"],
         who=["victor-palmen", "cilien-prieu"], img="stock/patiente-sourire.jpg", alt="Patiente souriante en fin de rendez-vous"),
]
FAM = {f["slug"]: f for f in FAMILIES}
FAM_OF = {}
for _f in FAMILIES:
    for _c in _f["cares"]:
        FAM_OF[_c] = _f

ORTHO_NOTE = "L’orthodontie n’apparaît pas dans cette liste : le cabinet n’a pas confirmé la prise en charge de ce domaine. [ORTHODONTIE À CONFIRMER]"


def care(slug):
    """A treatment page's content, cleaned of the old site's link labels and CTA stubs."""
    src = SOURCE["soins"][slug]
    sections = []
    for s in src["sections"]:
        if s["h"] in ("Lire aussi", "Comprendre la suite possible"):
            continue
        paras = [p for p in s["p"] if len(p) > 60]
        if not paras:
            continue
        sections.append(dict(h=s["h"], p=paras))
    return dict(
        slug=slug, name=CARE_SHORT[slug], title=src["title"], desc=src["desc"],
        h1=src["h1"], lead=src["lead"], sections=sections, faq=src["faq"],
        notes=[n for n in src["notes"]], img=CARE_IMG[slug], family=FAM_OF[slug],
    )


ALL_CARES = list(CARE_SHORT.keys())

# ------------------------------------------------------------------ first visit
HOME_STEPS = [
    ("Vous arrivez et nous faisons connaissance", "Le motif de votre visite, vos antécédents, ce qui vous inquiète ou vous gêne. Rien n’est décidé à ce stade."),
    ("On examine avant de traiter", "Les dents, les gencives, les anciennes restaurations. Les radiographies sont proposées seulement si elles apportent une information nécessaire."),
    ("On vous explique ce qui a été observé", "Avec des mots simples et, quand c’est utile, les images de votre bouche. Vous pouvez poser toutes vos questions."),
    ("On discute des différentes possibilités", "Quand plusieurs solutions existent, chacune est présentée avec ses étapes, sa durée et ses limites."),
    ("Vous décidez de la suite", "Avec toutes les informations nécessaires, et un devis écrit sur demande lorsqu’un traitement est proposé."),
]

VISIT_STEPS = [
    dict(k="Prise de rendez-vous", t="En ligne ou par téléphone",
         p="Réservez dans l’agenda en ligne à toute heure, ou appelez le cabinet du lundi au vendredi, de 8h à 18h30. Vous n’avez pas besoin de connaître le nom du soin, dites simplement ce qui vous amène et l’équipe vous oriente vers la bonne personne."),
    dict(k="Arrivée", t="Au premier étage, sans marche",
         p="Le cabinet se trouve Place de la Diversité 1, à Meyrin, au premier étage d’un immeuble sans marche à franchir. L’arrêt « Meyrin, Hôpital de la Tour » est à côté, et le parking des Sports se trouve sous le bâtiment."),
    dict(k="Documents à apporter", t="Ce qui aide vraiment",
         p="Une pièce d’identité, la liste de vos médicaments si vous en prenez, vos radiographies récentes si vous en avez, et le nom de votre assurance complémentaire dentaire si vous en avez une. Si vous n’avez rien de tout cela, venez quand même."),
    dict(k="Discussion initiale", t="On commence par vous écouter",
         p="Le praticien vous demande ce qui vous amène, depuis quand, et ce que vous avez déjà remarqué. Vos antécédents de santé et vos éventuelles craintes font partie de la conversation, parce qu’ils changent la façon de conduire le rendez-vous."),
    dict(k="Examen", t="Dents, gencives, restaurations",
         p="Le praticien examine les dents, les anciennes restaurations, les gencives, les dépôts et, lorsque cela concerne votre situation, la façon dont les dents se rencontrent. Un contrôle peut repérer une modification avant qu’elle ne provoque une gêne."),
    dict(k="Radiographies", t="Quand elles sont utiles",
         p="Les radiographies ne sont pas systématiques. Elles sont proposées lorsqu’elles montrent quelque chose que l’examen seul ne peut pas voir, par exemple entre deux dents ou sous une ancienne réparation. La raison de l’examen vous est expliquée."),
    dict(k="Diagnostic", t="Ce qui a été trouvé",
         p="Le praticien vous dit ce qu’il a observé, ce qui va bien et ce qui demande un soin ou une surveillance. Il peut aussi conclure qu’aucun soin n’est nécessaire, et c’est un résultat comme un autre."),
    dict(k="Explication", t="Avec des mots simples",
         p="Chaque observation est expliquée avant qu’un geste soit proposé. Si vous ne comprenez pas un terme, demandez, la réponse fait partie du rendez-vous."),
    dict(k="Options de traitement", t="Quand plusieurs solutions existent",
         p="Lorsqu’un soin peut être fait de plusieurs manières, chaque possibilité est présentée avec ses étapes, sa durée, ses limites et son suivi. Vous n’avez pas à choisir sur le moment."),
    dict(k="Devis", t="Avant de vous engager",
         p="Lorsqu’un traitement est proposé, vous pouvez demander un devis écrit avant de commencer. Il détaille les actes prévus et vous laisse le temps de décider."),
    dict(k="La suite", t="Vous décidez",
         p="Selon le cas, le rendez-vous se termine sans soin, avec une surveillance, avec un rendez-vous d’hygiène ou avec un traitement à planifier. La suite est fixée avec vous, jamais à votre place."),
]

# ------------------------------------------------------------------ trust
TRUST = [
    ("Expliquer avant d’intervenir", "Chaque observation est expliquée et chaque geste est annoncé. Vous savez ce qui va être fait avant que cela commence."),
    ("Une seule équipe, du contrôle à l’implant", "Médecine dentaire générale, chirurgie orale, implantologie et hygiène dentaire sont pratiquées sur place, par l’équipe du cabinet, chaque fois que cela est possible."),
    ("Des radiographies quand elles sont utiles", "Elles sont proposées lorsqu’elles apportent une information que l’examen seul ne donne pas, et la raison vous est expliquée."),
    ("Un accès sans marche", "Le cabinet est au premier étage, sans marche à franchir. Si vous avez un besoin précis, appelez avant le rendez-vous."),
    ("Six langues parlées", "Français, anglais, allemand, italien, espagnol et portugais, selon la personne qui vous reçoit."),
    ("Les urgences pendant les heures d’ouverture", "Appelez le " + PHONE + " et décrivez ce qui se passe. L’équipe vous dit quand venir."),
]

# ------------------------------------------------------------------ practice page
PRACTICE = dict(
    philosophy=[
        "On commence par regarder, comprendre et expliquer. Le traitement vient ensuite, et seulement quand vous l’avez accepté.",
        "Cette façon de travailler tient en trois habitudes : examiner avant de proposer, expliquer avant d’intervenir, et laisser la décision à la personne qui est dans le fauteuil.",
    ],
    spaces=[
        dict(img="photos/cabinet-hero.jpg", alt="Salle de soins avec le fauteuil et la lumière naturelle", cap="La salle de soins principale"),
        dict(img="photos/cabinet-room.jpg", alt="Fauteuil et instruments préparés", cap="Le fauteuil, préparé avant chaque rendez-vous"),
        dict(img="photos/cabinet-room-alt.jpg", alt="Deuxième salle de soins", cap="La deuxième salle de soins"),
        dict(img="photos/cabinet-sterilisation.jpg", alt="Salle de stérilisation des instruments", cap="La salle de stérilisation"),
    ],
    equipment="Le cabinet n’a pas publié la liste de son équipement. Les radiographies sont proposées lorsqu’elles apportent une information nécessaire au diagnostic. [ÉQUIPEMENT À CONFIRMER]",
    hygiene="Les instruments passent par une salle de stérilisation dédiée entre deux patients. Le cabinet n’a pas publié le détail de ses protocoles. [PROTOCOLE D’HYGIÈNE À CONFIRMER]",
    access="Le cabinet se trouve au premier étage d’un immeuble lié à l’imad, sans marche à franchir. Le site du cabinet indique que l’accès des personnes à mobilité réduite y est facilité. Le parking des Sports est situé sous le cabinet, avec une entrée par l’avenue Louis-Rendu, et le parking des Vergers se trouve à quelques minutes à pied.",
)

# ------------------------------------------------------------------ emergencies
EMERGENCY = dict(
    when=[
        "Une douleur qui devient difficile à supporter",
        "Une dent qui se casse ou qui bouge après un choc",
        "Un gonflement de la gencive, de la joue ou du visage",
        "Un saignement qui ne s’arrête pas après une intervention",
        "Une dent sortie de son emplacement",
    ],
    meanwhile=[
        "N’appliquez aucun produit directement sur la dent ou la gencive sans conseil professionnel.",
        "Après une intervention ou un choc, suivez les consignes reçues du cabinet.",
        "Pour un traumatisme, notez quand le choc a eu lieu et si une dent a bougé, s’est cassée ou est sortie.",
        "Si les symptômes changent ou s’aggravent, rappelez pour que la situation soit réévaluée.",
    ],
    vital="Une difficulté à respirer, une perte de connaissance ou un saignement incontrôlable relèvent des secours. En Suisse, appelez immédiatement le 144.",
    after="En dehors des heures d’ouverture, consultez les indications du répondeur du cabinet ou le service de garde de la SSO Genève. [NUMÉRO DU SERVICE DE GARDE À CONFIRMER]",
)

CONTACT_FAQ = [
    ("Dois-je connaître le nom du soin pour réserver ?", "Non. Dites ce qui vous amène, l’équipe vous oriente vers la personne qui pratique ce soin."),
    ("Puis-je réserver pour quelqu’un d’autre ?", "Oui. Indiquez le nom de la personne qui viendra et un numéro où la joindre."),
    ("Que se passe-t-il si j’ai mal aujourd’hui ?", "Appelez le " + PHONE + " et décrivez la situation. L’équipe vous dit quand venir. En cas d’urgence vitale, appelez le 144."),
    ("Le formulaire est-il fait pour une urgence ?", "Non. Pour une urgence, appelez. Le formulaire sert aux questions qui peuvent attendre une réponse par courriel."),
]

# ------------------------------------------------------------------ seo
META = dict(
    home=("Dentiste à Meyrin | Cabinet Dentaire Meyrin", "Cabinet dentaire à Meyrin, Place de la Diversité 1. Contrôles, hygiène, soins, implants et esthétique par une seule équipe. Rendez-vous en ligne ou au 022 320 19 19."),
    soins=("Soins dentaires à Meyrin | Prévenir, soigner, restaurer, harmoniser", "Tous les soins du Cabinet Dentaire Meyrin, organisés selon votre besoin : contrôle, hygiène, caries, traitements de racine, implants, couronnes, blanchiment et urgences."),
    equipe=("L’équipe du Cabinet Dentaire Meyrin", "Deux médecins-dentistes, un chirurgien oral, une hygiéniste dentaire et deux assistantes. Chaque profil dit ce que la personne pratique et dans quelles langues."),
    visite=("Comment se passe un premier rendez-vous | Cabinet Dentaire Meyrin", "De la prise de rendez-vous à la décision : arrivée, documents, examen, radiographies si nécessaires, explication, options et devis. Ce qui vous attend, étape par étape."),
    cabinet=("Le cabinet | Cabinet Dentaire Meyrin", "Les salles de soins, la stérilisation, l’accès sans marche et la façon de travailler du Cabinet Dentaire Meyrin, Place de la Diversité 1."),
    urgences=("Urgence dentaire à Meyrin | Cabinet Dentaire Meyrin", "Douleur, dent cassée, gonflement ou traumatisme : appelez le 022 320 19 19 du lundi au vendredi, 8h à 18h30. Que faire en attendant et quand appeler le 144."),
    contact=("Contact et accès | Cabinet Dentaire Meyrin", "Place de la Diversité 1, 1217 Meyrin, 1er étage sans marche. Tram 18, bus 56, 57, 68, 71 et A3, arrêt Meyrin, Hôpital de la Tour. Téléphone 022 320 19 19."),
)


def schema_dentist(base):
    return {
        "@context": "https://schema.org", "@type": "Dentist", "name": NAME,
        "telephone": PHONE_INTL, "email": MAIL, "url": base + "/",
        "image": base + "/assets/photos/cabinet-hero.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS, "postalCode": "1217", "addressLocality": "Meyrin", "addressRegion": "GE", "addressCountry": "CH"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:30"}],
        "availableLanguage": ["fr", "en", "de", "it", "es", "pt"],
        "employee": [{"@type": "Person", "name": p["name"], "jobTitle": p["role"]} for p in PEOPLE if p["source"]],
    }


def schema_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


# ------------------------------------------------------------------ locations
# Meyrin is verified. Nyon has been announced by the practice but nothing about
# it has been confirmed: every field stays a bracketed placeholder.
LOCATIONS = [
    dict(slug="meyrin", name="Meyrin", verified=True,
         address=ADDRESS, zip_city=ZIP_CITY, floor=FLOOR, hours=HOURS, phone=PHONE, tel=TEL, mail=MAIL,
         stop=STOP, tram=TRAM, bus=BUS, maps=MAPS, embed=MAPS_EMBED, booking=BOOKING,
         img="photos/cabinet-hero.jpg", alt="Salle de soins du cabinet de Meyrin",
         short="Entre l’Hôpital de La Tour et l’école des Vergers, au premier étage, sans marche.",
         parking="Parking des Sports sous le bâtiment, entrée par l’avenue Louis-Rendu. Parking des Vergers à quelques minutes à pied.",
         team=[p["slug"] for p in PEOPLE]),
    dict(slug="nyon", name="Nyon", verified=False,
         address="[ADRESSE À CONFIRMER]", zip_city="[NPA] Nyon", floor="[ÉTAGE ET ACCÈS À CONFIRMER]", hours="[HORAIRES À CONFIRMER]",
         phone=PHONE, tel=TEL, mail=MAIL, stop="[ARRÊT À CONFIRMER]", tram="", bus="[LIGNES À CONFIRMER]",
         maps="https://www.google.com/maps/search/?api=1&query=Nyon", embed=None, booking=BOOKING,
         img="stock/salle-turquoise.jpg", alt="Salle de soins, photo d’illustration en attendant celles de Nyon", short="Le second cabinet du groupe. Les informations pratiques seront publiées dès que le cabinet les aura confirmées.",
         parking="[STATIONNEMENT À CONFIRMER]", team=[]),
]
LOC = {l["slug"]: l for l in LOCATIONS}
NAV = [
    ("Accueil", "/"),
    ("Soins", "/soins/"),
    ("Cabinets", "/cabinets/"),
    ("Équipe", "/equipe/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact/"),
]
BLOG = json.load(open(HERE / "content" / "blog-fr.json", encoding="utf-8"))
PRACTICAL = dict(
    h="En pratique",
    items=[
        ("Rendez-vous", "Réservez en ligne ou au " + PHONE + ". Vous n’avez pas besoin de connaître le nom du soin, dites ce qui vous amène. Durée du rendez-vous : [DURÉE À CONFIRMER]."),
        ("Devis et financement", "En Suisse, la plupart des soins dentaires ne sont pas pris en charge par l’assurance de base (LAMal). Lorsqu’un traitement est proposé, un devis écrit vous est remis avant de commencer. [MODALITÉS DE PAIEMENT ET DE FACTURATION À CONFIRMER]"),
        ("Accident", "Si le soin fait suite à un accident, il est annoncé à votre assurance accident (LAA) ou à votre assurance maladie. Signalez-le à la réservation, l’équipe vous explique la déclaration."),
        ("Où", "Le soin est pratiqué au cabinet de Meyrin. Pour Nyon, les soins pris en charge restent à confirmer. [À CONFIRMER]"),
    ],
)
META["blog"] = ("Le blog du cabinet | Comprendre les soins dentaires", "Articles du Cabinet Dentaire Meyrin et Nyon pour comprendre les soins dentaires : prévention, dents de sagesse, blanchiment, enfants. Sans jargon, sans promesse.")
META["cabinets"] = ("Nos cabinets, Meyrin et Nyon | Cabinet Dentaire", "Deux cabinets, une seule équipe. Meyrin, Place de la Diversité 1, et Nyon. Adresse, horaires, accès et prise de rendez-vous pour chaque cabinet.")
META["meyrin"] = ("Cabinet Dentaire Meyrin, Place de la Diversité 1", "Le cabinet de Meyrin : adresse, horaires, accès en tram 18 et bus, parking des Sports, équipe et prise de rendez-vous. 1er étage sans marche.")
META["nyon"] = ("Cabinet Dentaire Nyon | Informations à venir", "Le cabinet de Nyon. Les informations pratiques seront publiées dès que le cabinet les aura confirmées. Rendez-vous en ligne ou au 022 320 19 19.")
META["formulaire"] = ("Formulaire patient | Cabinet Dentaire", "Remplissez vos informations avant votre premier rendez-vous, à votre rythme : identité, assurance, coordonnées. Facultatif, conservé sur votre appareil jusqu’à l’envoi ou l’impression.")
