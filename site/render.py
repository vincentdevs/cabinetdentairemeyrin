"""One site, two practices, two languages, rendered in two brand identities.

Routes, structure and facts are identical across themes and languages. Each
theme carries its own stylesheet; each language carries its own content module
(content.py, content_en.py) and its own set of interface strings below.
"""
import json
import re
import shutil
import pathlib

import content as FR
import content_en as EN

# French typography: a normal space before ? ! : ; lets the browser wrap right
# before the punctuation, stranding it alone on the next line. A non-breaking
# space keeps the last word and its punctuation together.
FR_PUNCT = re.compile(r" ([?!:;])")


def fr_typo(html):
    return FR_PUNCT.sub(" \\1", html)

HERE = pathlib.Path(__file__).parent

THEMES = {
    # single delivery: the elegant blues theme, at the site root
    "a1": dict(prefix="", css="a", color="#0F607B", preload=["Newsreader-normal-500.woff2", "InstrumentSans-normal-400.woff2"],
               hero=("photo", "stock/cabinet-hero-b.jpg"), label="Cabinet Dentaire Meyrin [PLACEHOLDER photo, à remplacer par une photo du cabinet de Meyrin]"),
}
LANGS = {"fr": FR, "en": EN}

S = {
    "fr": dict(
        nav_all="Tous les soins", nav_cabs="Les deux cabinets", contact_loc="Contacter le cabinet de", form_loc="Formulaire pour ce cabinet",
        about_k="Le cabinet", about_h="Un cabinet qui explique avant d’agir", about_p="Médecine dentaire générale, chirurgie orale, implantologie et hygiène dentaire, réunies dans une seule équipe. Chaque soin est précédé d’un examen, expliqué avec des mots simples, et décidé par la personne dans le fauteuil.",
        about_team="L’équipe en résumé", about_diff="Ce qui nous distingue", about_more="Découvrir l’équipe",
        team_home_label="L’équipe", team_home_h="Nous sommes là pour vous accueillir", team_home_p="Deux médecins-dentistes, un chirurgien oral, une hygiéniste et deux assistantes. Une équipe stable, que vous retrouvez d’un rendez-vous à l’autre.", team_home_more="Voir toute l’équipe",
        hero_people="Victor et Edouard vous reçoivent",
        soins_home_h="Nos soins", soins_home_p="Chaque famille de soins a sa section ci-dessous, avec la liste de ce que nous pratiquons. Chaque soin a ensuite sa page, avec le déroulement, les questions fréquentes et les informations pratiques.",
        all_of="Voir la famille", blog_h="Le blog", blog_p="Des articles pour comprendre les soins dentaires avant de venir, sans jargon et sans promesse.", blog_all="Tous les articles", blog_read="Lire l’article",
        blog_lead="Ce que nous expliquons au fauteuil, écrit pour être lu chez vous : prévention, dents de sagesse, blanchiment, enfants. Les articles s’ajouteront au fil des questions que vous nous posez.",
        cab_soins="Les soins pratiqués à", cab_contact="Contacter le cabinet de", cab_contact_p="Par téléphone pendant les heures d’ouverture, par courriel pour ce qui peut attendre, ou en ligne pour réserver.",
        f_cab_opt="Cabinet (facultatif)", f_cab_none="Je ne sais pas encore",
        lang="fr-CH", other="en", other_label="English", book="Prendre rendez-vous", book_online="Prendre rendez-vous en ligne", call="Appeler le cabinet",
        call_n="Appeler le", directions="Ouvrir l’itinéraire", route="Itinéraire", learn="En savoir plus", discover="Découvrir", search="Rechercher",
        search_ph="Un soin, une personne, une page…", search_none="Aucun résultat. Essayez « implant », « enfant » ou « horaires ».",
        search_hint="Tapez pour chercher dans les soins, l’équipe et les pages.", skip="Aller au contenu", menu_open="Ouvrir le menu", menu_close="Fermer",
        quick="Accès rapides", call_short="Appeler", choose="Choisir un cabinet", form="Formulaire patient", emergency="Urgences", see_loc="Voir le cabinet de",
        home="Accueil", crumbs="Fil d’Ariane", who_cares="Qui pratique ce soin", who_cares_pl="Qui pratique ces soins", same_family="Dans la même famille",
        others="Les autres familles de soins", faq="Questions fréquentes", team_intro="Deux médecins-dentistes, un chirurgien oral, une hygiéniste dentaire et deux assistantes. Chaque profil dit ce que la personne pratique et dans quelles langues.",
        team_h="Les personnes qui vous reçoivent", team_lead="Deux médecins-dentistes, un chirurgien oral, une hygiéniste dentaire et deux assistantes. Vous n’avez pas à choisir vous-même : indiquez le motif du rendez-vous et l’équipe vous oriente vers la personne qui pratique ce soin.",
        areas="Domaines", langs="Langues", practice="Cabinet", cares_of="Les soins pratiqués", source="Source : présentation officielle du cabinet, mise à jour le",
        visit_h="Comment se passe un premier rendez-vous", visit_lead="Beaucoup de personnes repoussent un rendez-vous parce qu’elles ne savent pas ce qui les attend. Voici la visite, étape par étape, de la réservation à la décision. Rien n’est décidé à votre place.",
        bring="À apporter", bring_items=["Une pièce d’identité", "La liste de vos médicaments, si vous en prenez", "Vos radiographies récentes, si vous en avez", "Le nom de votre assurance complémentaire dentaire, si vous en avez une"],
        bring_note="Si vous n’avez rien de tout cela, venez quand même.", fill_form="Gagnez du temps à l’accueil : remplissez le formulaire patient en ligne, à votre rythme.",
        calm="Vous pouvez demander une pause, une explication ou un temps de réflexion à n’importe quel moment.", calm_p="Une appréhension se dit au téléphone ou en arrivant, sans justification. Le rendez-vous avance à votre rythme, et un premier contrôle peut très bien se terminer sans aucun soin.",
        all_steps="Toutes les étapes, de la réservation au devis", meet="Rencontrer l’équipe",
        hero_kicker="Cabinet dentaire, Meyrin et Nyon", hero_a="Des soins précis, des explications simples", hero_b="Prendre soin de vos dents, simplement",
        hero_lead="Contrôles, hygiène, caries, implants ou esthétique dentaire : une seule équipe s’occupe de vous, dans nos deux cabinets. Nous commençons toujours par regarder et expliquer, puis c’est vous qui décidez de la suite.",
        hero_alt="Victor Palmen et Edouard Di Donna, les deux médecins du cabinet",
        locs_h="Deux cabinets, une seule équipe", locs_p="Choisissez le cabinet le plus proche de chez vous. Chaque cabinet a sa page avec son adresse, ses horaires, son accès et son équipe.",
        illus="Photo d’illustration", philo="On commence par regarder, comprendre et expliquer. Le traitement vient ensuite.",
        philo_p="Cette façon de travailler tient en trois habitudes : examiner avant de proposer, expliquer avant d’intervenir, et laisser la décision à la personne qui est dans le fauteuil. Elle vaut pour un contrôle comme pour un implant.",
        soins_h="Les soins, organisés selon votre besoin", soins_p="Quatre familles plutôt qu’une liste de spécialités. Chaque page dit ce que le praticien vérifie, comment le soin se déroule et ce que vous pourrez décider après l’examen.",
        cont_h="Une seule équipe couvre toute la gamme", cont_p="Du contrôle annuel à la pose d’implant, les soins sont réalisés par l’équipe du cabinet chaque fois que cela est possible. Vous n’êtes pas envoyé à une seconde adresse en cours de traitement, et la personne qui vous a examiné sait ce qui a été fait.",
        trust_h="Ce que vous pouvez attendre du cabinet", close_h="Besoin d’un rendez-vous ?", close_p="Réservez en ligne à toute heure ou appelez pendant les heures d’ouverture. Vous n’avez pas besoin de connaître le nom du soin, dites simplement ce qui vous amène.",
        close_care_h="Vous avez une question sur ce soin ?", close_care_p="Le rendez-vous sert à examiner votre situation et à vous expliquer ce qui est possible. Vous décidez ensuite.",
        close_person_h="Prendre rendez-vous", close_person_p="Lors de la réservation, dites-nous simplement ce qui vous amène. L’équipe vous oriente vers la personne qui pratique ce soin.",
        soins_lead="Chaque page dit ce que le praticien vérifie, comment le soin se déroule et ce que vous pourrez décider après l’examen. Vous n’avez pas besoin de connaître le nom du soin pour prendre rendez-vous.",
        soins_title="Les soins, expliqués avant d’être décidés", by="Pratiqué par", pending_team="Le cabinet n’a pas encore précisé qui consulte à Nyon ni les soins qui y sont pris en charge. [ÉQUIPE DE NYON À CONFIRMER]",
        cabinets_h="Nos cabinets", cabinets_lead="Deux adresses, une seule façon de travailler. Choisissez le cabinet le plus proche, la prise de rendez-vous et le téléphone sont communs.",
        cmp_h="Les deux cabinets en un coup d’œil", cmp_note="Les champs entre crochets seront remplis dès que le cabinet aura confirmé les informations de Nyon. Rien n’est rempli au jugé.",
        cmp_rows=[("Adresse", "address"), ("Localité", "zip_city"), ("Accès", "floor"), ("Horaires", "hours"), ("Téléphone", "phone"), ("Arrêt", "stop"), ("Lignes", "bus"), ("Stationnement", "parking")],
        loc_of="Le cabinet de", come="Venir au cabinet", who_at="Qui vous reçoit à", spaces="Les espaces", know="Ce qu’il faut savoir avant de venir",
        facts=[("Adresse", "address"), ("Accès", "floor"), ("Horaires", "hours"), ("Téléphone", "phone"), ("Courriel", "mail"), ("Transports", "transport"), ("Voiture", "parking")],
        f_access="Accès", f_diag="Diagnostic", f_diag_p="Le praticien examine d’abord, puis propose une radiographie seulement lorsqu’elle apporte une information que l’examen seul ne donne pas. La raison de l’examen vous est expliquée.",
        f_hyg="Hygiène", f_equip="Équipement", f_langs="Langues", f_langs_p="Français, anglais, allemand, italien, espagnol et portugais, selon la personne qui vous reçoit.", f_stop="Arrêt",
        urg_h="Une douleur qui ne peut pas attendre", urg_lead="Appelez le cabinet et décrivez ce qui se passe, depuis quand et comment cela évolue. L’équipe vous dit quand venir. Le degré d’urgence ne se détermine pas depuis une page web.",
        urg_open="Pendant les heures d’ouverture", urg_when="Quand appeler", urg_wait="En attendant le rendez-vous", urg_vital="Urgence vitale", urg_after="En dehors des heures d’ouverture",
        urg_how="Comment se déroule une consultation urgente", urg_how_p1="Le médecin-dentiste commence par identifier la source probable du problème et vérifier les tissus concernés. Le premier objectif peut être de soulager, de stabiliser la situation ou de protéger la dent. Si un traitement complémentaire est nécessaire, les options et la suite sont expliquées avant de continuer.",
        urg_how_p2="Une urgence ne conduit donc pas toujours à un traitement complet le jour même. La conduite dépend de l’examen et de ce qui peut être fait dans de bonnes conditions.", urg_link="La page du soin détaille ce qui est vérifié.",
        contact_h="Nous contacter", contact_lead="Pour un rendez-vous, l’agenda en ligne et le téléphone sont les plus rapides. Le formulaire sert aux questions qui peuvent attendre une réponse par courriel.",
        write_h="Écrire au cabinet", write_p="Pas de formulaire pour une urgence : appelez le {phone}. Ne décrivez pas ici votre état de santé, cela se fait au cabinet.",
        f_name="Prénom et nom", f_email="Adresse e-mail", f_phone="Téléphone", f_cab="Cabinet", f_any="Indifférent", f_reason="Motif de votre demande",
        f_reasons=["Question sur un rendez-vous", "Question sur un soin", "Documents ou facture", "Autre"], f_msg="Message", f_send="Envoyer le message", f_ok="Merci, votre message est prêt à partir depuis votre messagerie.",
        map="Plan d’accès", legal="Informations légales", legal_p="Cette page reste à compléter par le cabinet.", nf="Cette page n’existe pas", nf_p="L’adresse a peut-être changé. Les soins, l’équipe, les cabinets et le contact sont accessibles depuis le menu.",
        foot_about="Médecine dentaire générale, chirurgie orale, implantologie et hygiène dentaire, par une seule équipe.", foot_soins="Soins", foot_cab="Le cabinet", foot_team="L’équipe", foot_visit="Première visite",
        foot_legal="Les informations de ce site aident à préparer un rendez-vous, seul un examen permet de savoir quel soin vous convient.",
        video_k="Vidéo courte", video_t="Une explication en image de ce soin", video_p="Le cabinet prévoit de courtes vidéos pour expliquer les principaux soins. Celle-ci sera ajoutée dès qu’elle aura été tournée. [VIDÉO À CONFIRMER]",
        chooser_k="Cabinet dentaire", chooser_h="Choisissez votre cabinet", chooser_p="Même équipe, même façon de travailler, deux adresses.", chooser_go="Entrer", chooser_all="Voir le site sans choisir",
        quick_items=[],
        form_h="Votre formulaire patient", form_lead="Remplissez vos informations avant votre premier rendez-vous, à votre rythme. C’est facultatif : tout peut aussi se faire à l’accueil. Rien ne quitte votre appareil tant que vous n’avez pas choisi d’envoyer ou d’imprimer.",
        form_steps=["Cabinet et motif", "Identité", "Coordonnées", "Assurance", "Santé", "Récapitulatif"], prev="Précédent", next="Suivant", print="Imprimer ou enregistrer en PDF", send="Envoyer par courriel", clear="Effacer le brouillon",
        f_lang="Langue souhaitée pour le rendez-vous", f_birth="Date de naissance", f_sex="Titre", f_sexes=["Madame", "Monsieur", "Autre ou non précisé"], f_first="Prénom", f_last="Nom", f_street="Rue et numéro", f_zip="NPA", f_city="Localité",
        f_avs="Numéro AVS", f_avs_hint="13 chiffres, commence par 756. Il figure sur votre carte d’assurance maladie. Facultatif.", f_avs_bad="Ce numéro ne semble pas valide : vérifiez les 13 chiffres.", f_avs_ok="Numéro valide.",
        f_insurer="Assurance maladie de base (LAMal)", f_insurer_hint="Le nom de votre assureur. La plupart des soins dentaires ne sont pas couverts par la LAMal, cette information sert en cas d’accident ou de maladie grave.",
        f_card="Numéro de carte d’assuré", f_card_hint="Les 20 chiffres au recto de la carte. Facultatif.", f_compl="Assurance complémentaire dentaire", f_compl_hint="Si vous en avez une, son nom et votre numéro de police. Facultatif.",
        f_accident="Il s’agit d’un accident", f_accident_hint="En Suisse, un accident dentaire est annoncé à votre assurance accident ou à votre assurance maladie. Cochez si c’est le cas, l’équipe vous expliquera la déclaration.",
        f_health_note="Ces questions sont facultatives et vous pouvez y répondre au cabinet. Elles aident le praticien à préparer votre rendez-vous.", f_doctor="Médecin traitant", f_meds="Médicaments pris actuellement", f_allergies="Allergies connues",
        f_conditions="Maladies ou antécédents à signaler", f_pregnant="Grossesse en cours ou envisagée", f_fear="Une appréhension à signaler", f_notes="Ce qui vous amène, en quelques mots", yes="Oui", no="Non",
        f_consent="J’ai lu la note d’information et j’accepte que le cabinet traite ces données pour organiser mon rendez-vous et mon dossier patient.",
        f_consent_note="Note d’information (nLPD). Ces données sont traitées par le cabinet uniquement pour votre prise en charge et la gestion de votre dossier, conformément à la loi fédérale sur la protection des données. Elles ne sont ni vendues ni transmises à des tiers hors des besoins du traitement (laboratoire, assurance avec votre accord). Vous pouvez demander l’accès, la rectification ou la suppression de vos données au cabinet. Ce formulaire ne stocke rien sur un serveur : il reste dans votre navigateur jusqu’à ce que vous l’imprimiez, l’envoyiez ou l’effaciez.",
        f_send_note="L’envoi par courriel passe par votre messagerie et n’est pas chiffré de bout en bout. Pour les informations de santé, préférez l’impression ou l’envoi depuis une messagerie de confiance, ou remettez le formulaire à l’accueil.",
        f_sig="Signature", f_sig_hint="Tapez votre nom pour signer.", f_date="Date", f_recap="Vérifiez vos réponses", f_empty="Non renseigné", f_saved="Brouillon enregistré sur cet appareil.",
        f_required="Ce champ est nécessaire.", f_email_bad="Cette adresse ne semble pas valide.", f_step="Étape", f_of="sur",
        publisher="Éditeur du site", pub_manager="Responsable de la publication", hosting="Hébergement", data="Données personnelles", credits="Crédits photographiques",
        credits_p="Photographies du cabinet et portraits : Cabinet Dentaire Meyrin. Photographies d’illustration : Unsplash.",
    ),
    "en": dict(
        nav_all="All treatments", nav_cabs="Both practices", contact_loc="Contact the practice in", form_loc="Form for this practice",
        about_k="The practice", about_h="A practice that explains before it acts", about_p="General dentistry, oral surgery, implantology and dental hygiene, brought together in one team. Every treatment comes after an examination, is explained in plain words, and is decided by the person in the chair.",
        about_team="The team in brief", about_diff="What sets us apart", about_more="Meet the team",
        team_home_label="The team", team_home_h="We are here to welcome you", team_home_p="Two dentists, an oral surgeon, a dental hygienist and two assistants. A stable team, the same faces from one appointment to the next.", team_home_more="Meet the whole team",
        hero_people="Victor and Edouard welcome you",
        soins_home_h="Our treatments", soins_home_p="Each family of treatments has its section below, with the list of what we provide. Each treatment then has its own page, with how it unfolds, frequent questions and practical details.",
        all_of="See the family", blog_h="The blog", blog_p="Articles to understand dental care before you come, without jargon and without promises.", blog_all="All articles", blog_read="Read the article",
        blog_lead="What we explain at the chair, written to be read at home: prevention, wisdom teeth, whitening, children. Articles will be added as your questions come in.",
        cab_soins="Treatments provided in", cab_contact="Contact the practice in", cab_contact_p="By phone during opening hours, by email for what can wait, or online to book.",
        f_cab_opt="Practice (optional)", f_cab_none="I do not know yet",
        lang="en", other="fr", other_label="Français", book="Book an appointment", book_online="Book online", call="Call the practice", call_n="Call",
        directions="Open directions", route="Directions", learn="Find out more", discover="Discover", search="Search", search_ph="A treatment, a person, a page…",
        search_none="No result. Try “implant”, “child” or “hours”.", search_hint="Type to search treatments, the team and pages.", skip="Skip to content", menu_open="Open menu", menu_close="Close",
        quick="Quick actions", call_short="Call", choose="Choose a practice", form="Patient form", emergency="Emergencies", see_loc="See the practice in",
        home="Home", crumbs="Breadcrumb", who_cares="Who provides this treatment", who_cares_pl="Who provides these treatments", same_family="In the same family",
        others="The other treatment families", faq="Frequently asked questions", team_intro="Two dentists, an oral surgeon, a dental hygienist and two assistants. Each profile says what the person does and in which languages.",
        team_h="The people who receive you", team_lead="Two dentists, an oral surgeon, a dental hygienist and two assistants. You do not have to choose yourself: say what the appointment is for and the team directs you to the person who provides that care.",
        areas="Areas", langs="Languages", practice="Practice", cares_of="Treatments provided", source="Source: the practice's official presentation, updated on",
        visit_h="What happens at a first appointment", visit_lead="Many people put off an appointment because they do not know what to expect. Here is the visit, step by step, from booking to decision. Nothing is decided for you.",
        bring="What to bring", bring_items=["An identity document", "The list of your medicines, if you take any", "Your recent X-rays, if you have some", "The name of your supplementary dental insurance, if you hold one"],
        bring_note="If you have none of these, come anyway.", fill_form="Save time at reception: fill in the patient form online, at your own pace.",
        calm="You can ask for a pause, an explanation or time to think at any moment.", calm_p="A worry can be mentioned on the phone or on arrival, with no need to justify it. The appointment goes at your pace, and a first check-up can very well end with no treatment at all.",
        all_steps="All the steps, from booking to estimate", meet="Meet the team",
        hero_kicker="Dental practice, Meyrin and Nyon", hero_a="Precise care, plain explanations", hero_b="Taking care of your teeth, simply",
        hero_lead="Check-ups, hygiene, cavities, implants, or cosmetic dentistry: one team looks after you, across our two practices. We always start by looking and explaining, then you decide what comes next.",
        hero_alt="Victor Palmen and Edouard Di Donna, the practice's two doctors",
        locs_h="Two practices, one team", locs_p="Choose the practice closest to you. Each practice has its own page with its address, hours, access and team.",
        illus="Illustration photo", philo="We start by looking, understanding and explaining. Treatment comes next.",
        philo_p="This way of working comes down to three habits: examine before proposing, explain before acting, and leave the decision to the person in the chair. It applies to a check-up as much as to an implant.",
        soins_h="Treatments, organised around your need", soins_p="Four families rather than a list of specialities. Each page says what the practitioner checks, how the treatment unfolds and what you will be able to decide after the examination.",
        cont_h="One team covers the whole range", cont_p="From the yearly check-up to implant placement, treatments are carried out by the practice team whenever possible. You are not sent to a second address mid-treatment, and the person who examined you knows what was done.",
        trust_h="What you can expect from the practice", close_h="Need an appointment?", close_p="Book online at any hour or call during opening hours. You do not need to know the name of the treatment, just say what brings you.",
        close_care_h="Do you have a question about this treatment?", close_care_p="The appointment is there to examine your situation and explain what is possible. You decide afterwards.",
        close_person_h="Book an appointment", close_person_p="When booking, just tell us what brings you. The team directs you to the person who provides that care.",
        soins_lead="Each page says what the practitioner checks, how the treatment unfolds and what you will be able to decide after the examination. You do not need to know the name of the treatment to book.",
        soins_title="Treatments, explained before they are decided", by="Provided by", pending_team="The practice has not yet said who consults in Nyon nor which treatments are offered there. [NYON TEAM TO BE CONFIRMED]",
        cabinets_h="Our practices", cabinets_lead="Two addresses, one way of working. Choose the closest practice, booking and the phone number are shared.",
        cmp_h="The two practices at a glance", cmp_note="Bracketed fields will be filled in as soon as the practice confirms the Nyon details. Nothing is guessed.",
        cmp_rows=[("Address", "address"), ("Town", "zip_city"), ("Access", "floor"), ("Hours", "hours"), ("Phone", "phone"), ("Stop", "stop"), ("Lines", "bus"), ("Parking", "parking")],
        loc_of="The practice in", come="Getting there", who_at="Who receives you in", spaces="The rooms", know="What to know before you come",
        facts=[("Address", "address"), ("Access", "floor"), ("Hours", "hours"), ("Phone", "phone"), ("Email", "mail"), ("Public transport", "transport"), ("By car", "parking")],
        f_access="Access", f_diag="Diagnosis", f_diag_p="The practitioner examines first, then suggests an X-ray only when it adds information the examination alone does not give. The reason for the examination is explained to you.",
        f_hyg="Hygiene", f_equip="Equipment", f_langs="Languages", f_langs_p="French, English, German, Italian, Spanish and Portuguese, depending on who receives you.", f_stop="Stop",
        urg_h="Pain that cannot wait", urg_lead="Call the practice and describe what is happening, since when and how it is evolving. The team tells you when to come. The degree of urgency cannot be determined from a web page.",
        urg_open="During opening hours", urg_when="When to call", urg_wait="While waiting for the appointment", urg_vital="Life-threatening emergency", urg_after="Outside opening hours",
        urg_how="How an emergency consultation goes", urg_how_p1="The dentist starts by identifying the likely source of the problem and checking the tissues concerned. The first aim may be to relieve, stabilise the situation or protect the tooth. If further treatment is needed, the options and next steps are explained before continuing.",
        urg_how_p2="An emergency therefore does not always lead to a complete treatment the same day. What is done depends on the examination and on what can be done in good conditions.", urg_link="The treatment page details what is checked.",
        contact_h="Get in touch", contact_lead="For an appointment, the online diary and the phone are the quickest. The form is for questions that can wait for an answer by email.",
        write_h="Write to the practice", write_p="No form for an emergency: call {phone}. Do not describe your health here, that is done at the practice.",
        f_name="First and last name", f_email="Email address", f_phone="Phone", f_cab="Practice", f_any="Either", f_reason="Reason for your request",
        f_reasons=["Question about an appointment", "Question about a treatment", "Documents or invoice", "Other"], f_msg="Message", f_send="Send the message", f_ok="Thank you, your message is ready to send from your email app.",
        map="Map", legal="Legal notice", legal_p="This page is still to be completed by the practice.", nf="This page does not exist", nf_p="The address may have changed. Treatments, team, practices and contact are available from the menu.",
        foot_about="General dentistry, oral surgery, implantology and dental hygiene, by one team.", foot_soins="Treatments", foot_cab="The practice", foot_team="The team", foot_visit="First visit",
        foot_legal="The information on this site helps you prepare an appointment, only an examination can tell which treatment suits you.",
        video_k="Short video", video_t="This treatment explained on screen", video_p="The practice plans short videos to explain the main treatments. This one will be added once it has been filmed. [VIDEO TO BE CONFIRMED]",
        chooser_k="Dental practice", chooser_h="Choose your practice", chooser_p="Same team, same way of working, two addresses.", chooser_go="Enter", chooser_all="Browse the site without choosing",
        quick_items=[],
        form_h="Your patient form", form_lead="Fill in your details before your first appointment, at your own pace. It is optional: everything can also be done at reception. Nothing leaves your device until you choose to send or print.",
        form_steps=["Practice and reason", "Identity", "Contact details", "Insurance", "Health", "Summary"], prev="Back", next="Next", print="Print or save as PDF", send="Send by email", clear="Clear the draft",
        f_lang="Preferred language for the appointment", f_birth="Date of birth", f_sex="Title", f_sexes=["Ms", "Mr", "Other or not stated"], f_first="First name", f_last="Last name", f_street="Street and number", f_zip="Postcode", f_city="Town",
        f_avs="AHV/AVS number", f_avs_hint="13 digits, starts with 756. It is printed on your health insurance card. Optional.", f_avs_bad="This number does not look valid: check the 13 digits.", f_avs_ok="Valid number.",
        f_insurer="Basic health insurance (LAMal/KVG)", f_insurer_hint="The name of your insurer. Most dental care is not covered by basic insurance, this is used in case of accident or serious illness.",
        f_card="Insurance card number", f_card_hint="The 20 digits on the front of the card. Optional.", f_compl="Supplementary dental insurance", f_compl_hint="If you hold one, its name and your policy number. Optional.",
        f_accident="This is an accident", f_accident_hint="In Switzerland, a dental accident is reported to your accident insurance or your health insurer. Tick if this is the case, the team will explain the declaration.",
        f_health_note="These questions are optional and can be answered at the practice. They help the practitioner prepare your appointment.", f_doctor="Family doctor", f_meds="Current medicines", f_allergies="Known allergies",
        f_conditions="Conditions or history to report", f_pregnant="Pregnancy, current or planned", f_fear="A worry you would like to mention", f_notes="What brings you, in a few words", yes="Yes", no="No",
        f_consent="I have read the information notice and agree that the practice processes these details to organise my appointment and my patient file.",
        f_consent_note="Information notice (Swiss FADP). These details are processed by the practice solely for your care and the management of your file, in line with the Federal Act on Data Protection. They are neither sold nor passed on to third parties beyond what the treatment requires (laboratory, insurer with your consent). You can ask the practice to access, correct or delete your data. This form stores nothing on a server: it stays in your browser until you print, send or clear it.",
        f_send_note="Sending by email goes through your own email app and is not end-to-end encrypted. For health details, prefer printing, a trusted email service, or handing the form in at reception.",
        f_sig="Signature", f_sig_hint="Type your name to sign.", f_date="Date", f_recap="Check your answers", f_empty="Not provided", f_saved="Draft saved on this device.",
        f_required="This field is needed.", f_email_bad="This address does not look valid.", f_step="Step", f_of="of",
        publisher="Site publisher", pub_manager="Publishing manager", hosting="Hosting", data="Personal data", credits="Photo credits",
        credits_p="Practice photographs and portraits: Cabinet Dentaire Meyrin. Illustration photographs: Unsplash.",
    ),
}


# ------------------------------------------------------------------ chrome
def nav_items(px, C, T, active, mobile=False):
    out = ""
    for label, href in C.NAV:
        cur = ' aria-current="page"' if href == active else ""
        sub = None
        if href == "/soins/":
            sub = [(f["name"], f"/soins/{f['slug']}/") for f in C.FAMILIES] + [(T["nav_all"], "/soins/")]
        elif href == "/cabinets/":
            sub = [(L["name"], f"/cabinets/{L['slug']}/") for L in C.LOCATIONS] + [(T["nav_cabs"], "/cabinets/")]
        if sub:
            subs = "".join(f'<li><a href="{px}{h}">{t}</a></li>' for t, h in sub)
            out += (f'<li class="has-sub"><a href="{px}{href}"{cur}>{label}</a><button type="button" class="sub-btn" aria-expanded="false" aria-label="{label}"></button>'
                    f'<ul class="sub">{subs}</ul></li>')
        else:
            out += f'<li><a href="{px}{href}"{cur}>{label}</a></li>'
    return out


def header(px, C, T, active, other_url, css_prefix, theme="a"):
    items = nav_items(px, C, T, active)
    cur = "en" if T["other"] == "fr" else "fr"
    lang_block = (
        f'<div class="lang-switch" aria-label="Langue / Language">'
        f'<span class="lang-cur" aria-current="true">{cur.upper()}</span>'
        f'<span class="lang-sep" aria-hidden="true">/</span>'
        f'<a class="lang-other" href="{other_url}" hreflang="{T["other"]}" lang="{T["other"]}">{T["other"].upper()}</a>'
        f'</div>'
        if theme == "a" else
        f'<a class="lang" href="{other_url}" hreflang="{T["other"]}" lang="{T["other"]}">{T["other_label"]}</a>'
    )
    return f"""
<header class="top" id="top">
  <div class="wrap top-in">
    <a class="mark" href="{px}/" aria-label="Cabinet Dentaire, {T['home']}"><img src="/assets/brand/logo-cdm-long.svg" alt="Cabinet Dentaire Meyrin" width="150" height="56"></a>
    <nav class="nav" aria-label="Navigation"><ul>{items}</ul></nav>
    <div class="top-cta">
      <button class="search-btn" type="button" aria-label="{T['search']}" data-open-search><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
      {lang_block}
      <a class="btn btn-line btn-urg" href="{px}/urgences/">{T['emergency']}</a>
      <a class="btn" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a>
    </div>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="{T['menu_open']}"><span></span><span></span></button>
  </div>
  <div class="menu" id="menu" hidden>
    <div class="wrap menu-in">
      <nav aria-label="Navigation"><ul>{items}</ul></nav>
      <div class="menu-acts">
        <a class="btn" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a>
        <a class="btn btn-line btn-urg" href="{px}/urgences/">{T['emergency']}</a>
      </div>
      <p class="menu-links"><a href="{px}/formulaire/">{T['form']}</a><a href="{C.TEL}">{T['call_n']} {C.PHONE}</a><a href="{other_url}" hreflang="{T['other']}" lang="{T['other']}">{T['other_label']}</a></p>
      <p class="menu-info">{C.ADDRESS}, {C.ZIP_CITY}<br>{C.HOURS}</p>
    </div>
  </div>
  <div class="search" id="search" hidden>
    <div class="wrap search-in">
      <label for="q" class="search-label">{T['search']}</label>
      <div class="search-row"><input id="q" type="search" placeholder="{T['search_ph']}" autocomplete="off" data-index="{px}/search.json"><button type="button" class="search-close" data-close-search aria-label="{T['menu_close']}">×</button></div>
      <p class="search-hint">{T['search_hint']}</p>
      <ul class="search-results" id="search-results" data-none="{T['search_none']}"></ul>
    </div>
  </div>
</header>
<nav class="dock" aria-label="{T['quick']}">
  <a href="{C.TEL}">{T['call_short']}</a>
  <a class="dock-main" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a>
  <a href="{px}/cabinets/">{T['route']}</a>
</nav>
<main id="contenu">
"""


def footer(px, C, T, css_prefix):
    soins = "".join(f'<li><a href="{px}/soins/{f["slug"]}/">{f["name"]}</a></li>' for f in C.FAMILIES)
    return f"""
</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <img class="foot-logo" src="/assets/brand/logo-cdm-blanc.png" alt="Cabinet Dentaire Meyrin" width="200" height="71" loading="lazy">
        <p>{T['foot_about']}</p>
      </div>
      <div><h2 class="foot-h">{T['foot_soins']}</h2><ul>{soins}<li><a href="{px}/urgences/">{T['emergency']}</a></li></ul></div>
      <div><h2 class="foot-h">{T['foot_cab']}</h2><ul>
        <li><a href="{px}/equipe/">{T['foot_team']}</a></li>
        <li><a href="{px}/premiere-visite/">{T['foot_visit']}</a></li>
        <li><a href="{px}/cabinets/meyrin/">Meyrin</a></li>
        <li><a href="{px}/cabinets/nyon/">Nyon</a></li>
        <li><a href="{px}/formulaire/">{T['form']}</a></li>
        <li><a href="{px}/blog/">Blog</a></li>
        <li><a href="{px}/contact/">Contact</a></li></ul></div>
      <div><h2 class="foot-h">Meyrin</h2><ul>
        <li>{C.ADDRESS}, {C.ZIP_CITY}</li>
        <li>{C.HOURS}</li>
        <li><a href="{C.TEL}">{C.PHONE}</a></li>
        <li><a href="mailto:{C.MAIL}">{C.MAIL}</a></li></ul></div>
    </div>
    <div class="foot-legal"><p>Cabinet Dentaire Meyrin. {T['foot_legal']} <a href="{px}/mentions-legales/">{T['legal']}</a></p></div>
  </div>
</footer>
<script src="{css_prefix}/script.js" defer></script>
</body>
</html>
"""


def crumbs(T, items):
    return f'<nav class="crumbs" aria-label="{T["crumbs"]}"><ol>' + "".join(
        f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for t, h in items) + "</ol></nav>"


def phero(T, C, title, lead, crumb, img=None, cta=True, cls="", side=None, banner=None):
    """Interior opener: a large heading and lead on the left, a photo or a small side visual on the right.
    banner= replaces the side-by-side layout with a full-width strip below the title, for a wide group image."""
    if banner:
        return f"""
<header class="phero phero-banner {cls}">
  <div class="wrap">
    <div class="phero-txt">
      {crumbs(T, crumb)}
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
      {'<div class="acts"><a class="btn" href="' + C.BOOKING + '" target="_blank" rel="noopener">' + T['book'] + '</a><a class="btn btn-line" href="' + C.TEL + '">' + T['call'] + '</a></div>' if cta else ''}
    </div>
    <div class="phero-banner-pic mask">{banner}</div>
  </div>
</header>
"""
    return f"""
<header class="phero{' phero-img' if img else ''}{' phero-side' if side else ''} {cls}">
  <div class="wrap phero-in">
    <div class="phero-txt">
      {crumbs(T, crumb)}
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
      {'<div class="acts"><a class="btn" href="' + C.BOOKING + '" target="_blank" rel="noopener">' + T['book'] + '</a><a class="btn btn-line" href="' + C.TEL + '">' + T['call'] + '</a></div>' if cta else ''}
    </div>
    {'<div class="phero-pic mask">' + img + '</div>' if img else ''}
    {'<div class="phero-aside" aria-hidden="true">' + side + '</div>' if side else ''}
  </div>
</header>
"""


def closing(T, C, title=None, text=None):
    return f"""
<section class="close" aria-labelledby="close-h">
  <div class="wrap close-in">
    <div><h2 id="close-h">{title or T['close_h']}</h2><p>{text or T['close_p']}</p></div>
    <div class="acts">
      <a class="btn btn-big" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book_online']}</a>
      <a class="btn btn-line btn-big" href="{C.TEL}">{T['call_n']} {C.PHONE}</a>
      <p class="acts-note">{C.HOURS}</p>
    </div>
  </div>
</section>
"""


def faq_block(T, faq, hid="faq"):
    if not faq:
        return ""
    items = "".join(f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faq)
    return f'<section class="faq" aria-labelledby="{hid}"><div class="wrap faq-in"><h2 id="{hid}">{T["faq"]}</h2><div class="faq-list">{items}</div></div></section>'


def location_cards(px, C, T, picture):
    out = ""
    for L in C.LOCATIONS:
        pic = picture(L["img"], L["alt"], "(max-width: 900px) 100vw, 48vw")
        if not L["verified"]:
            pic += f'<span class="loc-tag">{T["illus"]}</span>'
        out += f"""
<article class="loc">
  <a class="loc-link" href="{px}/cabinets/{L['slug']}/" data-choose="{L['slug']}">
    <span class="loc-pic">{pic}</span>
    <span class="loc-body"><span class="loc-name">{L["name"]}</span><span class="loc-addr">{L["address"]}, {L["zip_city"]}</span><span class="loc-hours">{L["hours"]}</span><span class="loc-go">{T['see_loc']} {L['name']}</span></span>
  </a>
  <div class="acts loc-acts">
    <a class="btn" href="{px}/cabinets/{L['slug']}/#contact">{T['contact_loc']} {L['name']}</a>
    <a class="btn btn-line" href="{px}/formulaire/?cabinet={L['slug']}">{T['form_loc']}</a>
  </div>
</article>"""
    return out


def video_slot(T, picture, img):
    return f"""
<div class="video-slot">
  {picture(img, "", "(max-width: 900px) 100vw, 60vw")}
  <div class="video-txt"><span class="video-k">{T['video_k']}</span><b>{T['video_t']}</b><p>{T['video_p']}</p></div>
  <span class="video-play" aria-hidden="true"></span>
</div>"""


def form_page(px, C, T):
    steps_nav = "".join(f'<li{" aria-current=" + chr(34) + "step" + chr(34) if i == 0 else ""}><span>{i+1}</span>{s}</li>' for i, s in enumerate(T["form_steps"]))
    sexes = "".join(f'<option>{s}</option>' for s in T["f_sexes"])
    return f"""
<section class="pform-sec" aria-label="{T['form']}">
  <div class="wrap form-wrap">
    <ol class="form-steps">{steps_nav}</ol>
    <form class="pform" id="pform" data-mail="{C.MAIL}" data-required="{T['f_required']}" data-email-bad="{T['f_email_bad']}" data-avs-bad="{T['f_avs_bad']}" data-avs-ok="{T['f_avs_ok']}" data-empty="{T['f_empty']}" data-saved="{T['f_saved']}" data-step="{T['f_step']}" data-of="{T['f_of']}" novalidate>
      <p class="form-progress" aria-live="polite"></p>

      <fieldset class="fstep" data-step="1"><legend>{T['form_steps'][0]}</legend>
        <div class="field"><span class="field-label">{T['f_cab']}</span>
          <div class="choice"><label><input type="radio" name="cabinet" value="Meyrin" checked><span>Meyrin</span></label><label><input type="radio" name="cabinet" value="Nyon"><span>Nyon</span></label><label><input type="radio" name="cabinet" value="{T['f_any']}"><span>{T['f_any']}</span></label></div></div>
        <div class="field"><label for="p-reason">{T['f_reason']}</label><select id="p-reason" name="motif">{''.join(f'<option>{r}</option>' for r in T['f_reasons'])}</select></div>
        <div class="field"><label for="p-notes">{T['f_notes']}</label><textarea id="p-notes" name="notes" rows="3"></textarea></div>
        <div class="field"><label for="p-lang">{T['f_lang']}</label><select id="p-lang" name="langue"><option>Français</option><option>English</option><option>Deutsch</option><option>Italiano</option><option>Español</option><option>Português</option></select></div>
      </fieldset>

      <fieldset class="fstep" data-step="2" hidden><legend>{T['form_steps'][1]}</legend>
        <div class="grid2">
          <div class="field"><label for="p-sex">{T['f_sex']}</label><select id="p-sex" name="titre">{sexes}</select></div>
          <div class="field"><label for="p-birth">{T['f_birth']}</label><input id="p-birth" name="naissance" type="date" required></div>
          <div class="field"><label for="p-first">{T['f_first']}</label><input id="p-first" name="prenom" type="text" autocomplete="given-name" required></div>
          <div class="field"><label for="p-last">{T['f_last']}</label><input id="p-last" name="nom" type="text" autocomplete="family-name" required></div>
        </div>
      </fieldset>

      <fieldset class="fstep" data-step="3" hidden><legend>{T['form_steps'][2]}</legend>
        <div class="grid2">
          <div class="field span2"><label for="p-street">{T['f_street']}</label><input id="p-street" name="rue" type="text" autocomplete="street-address"></div>
          <div class="field"><label for="p-zip">{T['f_zip']}</label><input id="p-zip" name="npa" type="text" inputmode="numeric" autocomplete="postal-code"></div>
          <div class="field"><label for="p-city">{T['f_city']}</label><input id="p-city" name="localite" type="text" autocomplete="address-level2"></div>
          <div class="field"><label for="p-phone">{T['f_phone']}</label><input id="p-phone" name="telephone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="p-email">{T['f_email']}</label><input id="p-email" name="email" type="email" autocomplete="email" required></div>
        </div>
      </fieldset>

      <fieldset class="fstep" data-step="4" hidden><legend>{T['form_steps'][3]}</legend>
        <div class="field"><label for="p-avs">{T['f_avs']}</label><input id="p-avs" name="avs" type="text" inputmode="numeric" placeholder="756.1234.5678.97" data-avs><p class="hint">{T['f_avs_hint']}</p><p class="avs-check" aria-live="polite"></p></div>
        <div class="grid2">
          <div class="field"><label for="p-insurer">{T['f_insurer']}</label><input id="p-insurer" name="assureur" type="text"><p class="hint">{T['f_insurer_hint']}</p></div>
          <div class="field"><label for="p-card">{T['f_card']}</label><input id="p-card" name="carte" type="text" inputmode="numeric" maxlength="24"><p class="hint">{T['f_card_hint']}</p></div>
          <div class="field span2"><label for="p-compl">{T['f_compl']}</label><input id="p-compl" name="complementaire" type="text"><p class="hint">{T['f_compl_hint']}</p></div>
        </div>
        <div class="field"><label class="chk"><input type="checkbox" name="accident" value="{T['yes']}"><span>{T['f_accident']}</span></label><p class="hint">{T['f_accident_hint']}</p></div>
      </fieldset>

      <fieldset class="fstep" data-step="5" hidden><legend>{T['form_steps'][4]}</legend>
        <p class="note">{T['f_health_note']}</p>
        <div class="grid2">
          <div class="field"><label for="p-doctor">{T['f_doctor']}</label><input id="p-doctor" name="medecin" type="text"></div>
          <div class="field"><label for="p-preg">{T['f_pregnant']}</label><select id="p-preg" name="grossesse"><option></option><option>{T['no']}</option><option>{T['yes']}</option></select></div>
          <div class="field span2"><label for="p-meds">{T['f_meds']}</label><textarea id="p-meds" name="medicaments" rows="2"></textarea></div>
          <div class="field span2"><label for="p-allerg">{T['f_allergies']}</label><textarea id="p-allerg" name="allergies" rows="2"></textarea></div>
          <div class="field span2"><label for="p-cond">{T['f_conditions']}</label><textarea id="p-cond" name="antecedents" rows="2"></textarea></div>
          <div class="field span2"><label for="p-fear">{T['f_fear']}</label><textarea id="p-fear" name="apprehension" rows="2"></textarea></div>
        </div>
      </fieldset>

      <fieldset class="fstep" data-step="6" hidden><legend>{T['f_recap']}</legend>
        <dl class="recap" id="recap"></dl>
        <div class="consent">
          <p class="hint">{T['f_consent_note']}</p>
          <label class="chk"><input type="checkbox" name="consent" required><span>{T['f_consent']}</span></label>
          <div class="grid2"><div class="field"><label for="p-sig">{T['f_sig']}</label><input id="p-sig" name="signature" type="text" required><p class="hint">{T['f_sig_hint']}</p></div><div class="field"><label for="p-date">{T['f_date']}</label><input id="p-date" name="date" type="date" required></div></div>
        </div>
        <p class="hint">{T['f_send_note']}</p>
      </fieldset>

      <div class="form-nav">
        <button type="button" class="btn btn-line" data-prev hidden>{T['prev']}</button>
        <button type="button" class="btn" data-next>{T['next']}</button>
        <button type="button" class="btn" data-print hidden>{T['print']}</button>
        <button type="button" class="btn btn-line" data-send hidden>{T['send']}</button>
        <button type="button" class="link-btn" data-clear>{T['clear']}</button>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""


# ------------------------------------------------------------------ pages
def build(theme, picture, head, write, ld):
    TH = THEMES[theme]
    out = HERE.parent / "dist" / TH["prefix"].strip("/")
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / TH["css"] / "styles.css", out / "styles.css")
    shutil.copy(HERE / "shared" / "script.js", out / "script.js")
    shutil.copy(HERE / TH["css"] / "favicon.svg", out / "favicon.svg")
    urls = []
    for lang, C in LANGS.items():
        urls += render_lang(theme, lang, C, S[lang], picture, head, write)
    return urls


def render_lang(theme_key, lang, C, T, picture, head, write):
    TH = THEMES[theme_key]
    theme = TH["css"]
    px = TH["prefix"] + ("" if lang == "fr" else "/en")
    other_px = TH["prefix"] + ("/en" if lang == "fr" else "")
    base = FR.DOMAIN + px
    urls, index = [], []
    CUR = {"path": "/"}

    def H(title, desc, path, ldobjs=(), og="photos/cabinet-hero.jpg"):
        extra = "".join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in TH["preload"])
        extra += f'<link rel="alternate" hreflang="fr" href="{FR.DOMAIN}{TH["prefix"]}{path}"><link rel="alternate" hreflang="en" href="{FR.DOMAIN}{TH["prefix"]}/en{path}">'
        index.append(dict(t=title.split(" | ")[0], d=desc, u=px + path))
        return head(title, desc, path, px, "styles.css", TH["color"], ldobjs, og, extra, T["lang"], T["skip"])

    def page(path, title, desc, active, body_fn, ldobjs=(), og="photos/cabinet-hero.jpg", closing_args=None):
        CUR["path"] = path
        html = H(title, desc, path, ldobjs, og) + header(px, C, T, active, other_px + path, TH["prefix"], theme) + body_fn()
        if closing_args is not None:
            html += closing(T, C, *closing_args)
        html += footer(px, C, T, TH["prefix"])
        if lang == "fr":
            html = fr_typo(html)
        urls.append(write(px, path, html))

    def portrait(p, sizes="(max-width: 700px) 45vw, 18vw"):
        return (f'<li class="person"><a href="{px}/equipe/{p["slug"]}/"><span class="disc">'
                + picture("team/" + p["slug"] + ".png", f'{p["name"]}, {p["role"].lower()}', sizes)
                + f'</span><span class="person-name">{p["name"]}</span><span class="person-role">{p["role"]}</span></a></li>')

    def cares_of(p):
        if p["slug"] == "juliana":
            return ["hygieniste-dentaire-meyrin", "detartrage-meyrin", "soins-gencives-meyrin"]
        if p["slug"] == "edouard-di-donna":
            return ["chirurgie-orale-meyrin", "implant-dentaire-meyrin", "dents-sagesse-meyrin", "extraction-dentaire-meyrin", "implant-ou-bridge", "dent-manquante", "remplacer-plusieurs-dents"]
        if p["slug"] in ("victor-palmen", "cilien-prieu"):
            return ["controle-dentaire-meyrin", "carie-dentaire-meyrin", "dentiste-enfant-meyrin", "traitement-racine-meyrin", "couronne-dentaire-meyrin", "blanchiment-dentaire-meyrin", "facettes-dentaires-meyrin"]
        return []

    def side(photo, icon):
        """A small elegant visual next to a page title: a square photo in the classic theme, a line icon on a tinted panel in the modern one."""
        if theme == "a":
            return picture(photo, "", "(max-width: 900px) 40vw, 300px")
        return f'<span class="icon-panel"><img src="/assets/illustrations/{icon}-flat.svg" alt="" width="160" height="160"></span>'

    practices_label = "Cabinets" if lang == "fr" else "Practices"

    # ---------------------------------------------------------- home
    def home():
        steps = "".join(f'<li><span class="num" aria-hidden="true">0{i}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(C.HOME_STEPS, 1))
        diff = "".join(f'<div class="trust-item"><dt>{a}</dt><dd>{b}</dd></div>' for a, b in C.TRUST[:4])
        fam_secs = ""
        for i, f in enumerate(C.FAMILIES):
            cares = "".join(f'<li><a href="{px}/soins/{c}/"><div class="cl-n">{C.CARE_SHORT[c]}</div><div class="cl-q">{C.care(c)["h1"]}</div></a></li>' for c in f["cares"])
            visual = picture(f["img"], f["alt"], "(max-width: 900px) 100vw, 40vw") if theme == "a" else f'<img src="/assets/illustrations/{f["ill"]}-flat.svg" alt="" width="220" height="220" loading="lazy">'
            fam_secs += f"""
<section class="hfam{' hfam-flip' if i % 2 else ''}{' band-tint' if i % 2 else ''}" aria-labelledby="hfam-{f['slug']}">
  <div class="wrap hfam-in">
    <div class="hfam-visual">{visual}</div>
    <div class="hfam-txt"><span class="hfam-n" aria-hidden="true">0{i+1}</span><h2 id="hfam-{f['slug']}">{f["name"]}</h2><p class="fam-line">{f["line"]}</p><p>{f["intro"]}</p>
      <ul class="care-list">{cares}</ul><a class="btn btn-line" href="{px}/soins/{f['slug']}/">{T['all_of']} {f['name']}</a></div>
  </div>
</section>"""
        posts = "".join(f"""
<li class="post"><a href="{px}/blog/{b['slug']}/">{picture(b["img"], "", "(max-width: 900px) 100vw, 30vw")}<span class="post-k">{b["kicker"]}</span><h3>{b["title"]}</h3><p>{b["desc"]}</p><span class="link">{T['blog_read']}</span></a></li>""" for b in C.BLOG[:3])
        team_home_cards = "".join(
            f'<li class="thc"><a href="{px}/equipe/{p["slug"]}/"><span class="thc-pic">'
            + picture("team/" + p["slug"] + ".png", f'{p["name"]}, {p["role"].lower()}', "(max-width: 700px) 45vw, 30vw")
            + f'</span><span class="thc-txt"><span class="thc-name">{p["name"]}</span><span class="thc-role">{p["role"]}</span></span></a></li>'
            for p in C.PEOPLE
        )
        links = {"book": C.BOOKING, "urg": px + "/urgences/", "form": px + "/formulaire/"}
        quick = "".join(f'<li><a class="quick-{k}" href="{links[k]}"{" target=_blank rel=noopener" if k == "book" else ""}><span>{lbl}</span></a></li>' for lbl, k in T["quick_items"])
        kind, img = TH["hero"]
        if kind == "photo" and img != "stock/cabinet-hero-b.jpg":
            alt = "Salle de soins du cabinet de Meyrin" if lang == "fr" else "Treatment room of the Meyrin practice"
        elif kind == "photo":
            alt = "Salle de soins dentaire [PHOTO PROVISOIRE, À REMPLACER]" if lang == "fr" else "Dental treatment room [PLACEHOLDER PHOTO, TO REPLACE]"
        else:
            alt = "Illustration de la salle de soins" if lang == "fr" else "Illustration of the treatment room"
        illus = picture(img, alt, "(max-width: 900px) 100vw, 46vw", eager=True, fetchpriority="high")
        return f"""
<div class="hero hero-full">
  <div class="wrap hero-in">
    <div class="hero-txt">
      <div class="hero-head"><h1>{T['hero_a'] if theme == 'a' else T['hero_b']}</h1><p class="lead">{T['hero_lead']}</p></div>
      <div class="acts">
        <a class="btn btn-big" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a>
        <a class="btn btn-line btn-big" href="{px}/soins/">{C.NAV[1][0]}</a>
      </div>
      {'<ul class="quick-list" aria-label="' + T['quick'] + '">' + quick + '</ul>' if quick else ''}
    </div>
    <div class="hero-art mask">{illus}</div>
  </div>
</div>
<section class="about" aria-labelledby="about-h">
  <div class="wrap about-in about-solo">
    <div class="about-txt"><h2 id="about-h">{T['about_h']}</h2><p class="lead">{T['about_p']}</p>
      <div class="statement">{T['philo']}</div></div>
  </div>
  <div class="wrap"><h3 class="about-diff-h">{T['about_diff']}</h3><dl class="trust-grid">{diff}</dl></div>
</section>
<section class="team-home" aria-labelledby="team-home-h"><div class="wrap"><div class="sec-head sec-head-split"><div><p class="team-home-label">{T['team_home_label']}</p><h2 id="team-home-h">{T['team_home_h']}</h2></div><p>{T['team_home_p']}</p></div><ul class="thc-grid">{team_home_cards}</ul><p class="more"><a class="link" href="{px}/equipe/">{T['team_home_more']}</a></p></div></section>
{('<section class="philo" aria-label="' + T['philo'][:30] + '"><div class="wrap philo-in"><div class="philo-txt"><div class="statement">' + T['philo'] + '</div><p>' + T['philo_p'] + '</p></div><div class="philo-pic mask">' + picture("stock/patiente-sourire.jpg", "", "(max-width: 900px) 100vw, 36vw") + '</div></div></section>') if theme == "a" else ''}
<section class="locs" aria-labelledby="locs-h">
  <div class="wrap">
    <div class="sec-head sec-head-split"><h2 id="locs-h">{T['locs_h']}</h2><p>{T['locs_p']}</p></div>
    <div class="loc-grid">{location_cards(px, C, T, picture)}</div>
  </div>
</section>
<div class="soins-head"><div class="wrap sec-head sec-head-split"><h2 id="soins-h">{T['soins_home_h']}</h2><p>{T['soins_home_p']}</p></div></div>
{fam_secs}
<section class="visite" aria-labelledby="visite-h">
  <div class="wrap visite-in">
    <div class="visite-pic mask">{picture("photos/cabinet-room-alt.jpg", "", "(max-width: 900px) 100vw, 40vw")}</div>
    <div class="visite-txt"><h2 id="visite-h">{T['visit_h']}</h2><ol class="steps">{steps}</ol><a class="link" href="{px}/premiere-visite/">{T['all_steps']}</a></div>
  </div>
</section>
<section class="blog-sec band-tint" aria-labelledby="blog-h">
  <div class="wrap"><div class="sec-head sec-head-split"><h2 id="blog-h">{T['blog_h']}</h2><p>{T['blog_p']}</p></div>
    <ul class="posts">{posts}</ul><p class="more"><a class="link" href="{px}/blog/">{T['blog_all']}</a></p></div>
</section>
"""
    page("/", *C.META["home"], "/", home, [C.schema_dentist(base)], og=TH["hero"][1], closing_args=())

    # ---------------------------------------------------------- cabinets
    def cabinets():
        rows = "".join(f'<tr><th scope="row">{k}</th><td>{C.LOC["meyrin"][f]}</td><td>{C.LOC["nyon"][f]}</td></tr>' for k, f in T["cmp_rows"])
        return phero(T, C, T["cabinets_h"], T["cabinets_lead"], [(T["home"], px + "/"), (practices_label, None)], cta=False, side=side("photos/cabinet-room-alt.jpg", "tooth")) + f"""
<section class="locs" aria-label="{T['choose']}"><div class="wrap"><div class="loc-grid">{location_cards(px, C, T, picture)}</div></div></section>
<section class="compare" aria-labelledby="cmp-h">
  <div class="wrap"><h2 id="cmp-h">{T['cmp_h']}</h2>
    <div class="table-wrap"><table class="cmp"><thead><tr><th scope="col"></th><th scope="col">Meyrin</th><th scope="col">Nyon</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p class="note">{T['cmp_note']}</p></div>
</section>"""
    page("/cabinets/", *C.META["cabinets"], "/cabinets/", cabinets, [C.schema_dentist(base)], closing_args=())

    for L in C.LOCATIONS:
        def loc_page(L=L):
            vals = dict(address=f'{L["address"]}<br>{L["zip_city"]}', floor=L["floor"], hours=L["hours"], phone=f'<a href="{L["tel"]}">{L["phone"]}</a>',
                        mail=f'<a href="mailto:{L["mail"]}">{L["mail"]}</a>', transport=(L["tram"] + ", " if L["tram"] else "") + L["bus"] + f'<br><span class="muted">{T["f_stop"]} {L["stop"]}</span>', parking=L["parking"])
            facts = "".join(f'<div><dt>{k}</dt><dd>{vals[f]}</dd></div>' for k, f in T["facts"])
            team_block = (f'<ul class="portraits">{"".join(portrait(C.P[s]) for s in L["team"])}</ul>' if L["team"] else f'<p class="note">{T["pending_team"]}</p>')
            gallery = ""
            if L["slug"] == "meyrin":
                sp = C.PRACTICE["spaces"]
                gallery = f"""
<section class="gallery-sec" aria-labelledby="spaces-h"><div class="wrap"><h2 id="spaces-h">{T['spaces']}</h2>
  <div class="gallery">{''.join(f'<figure class="g{i+1} mask">{picture(s["img"], s["alt"], "(max-width: 900px) 100vw, 50vw")}<figcaption>{s["cap"]}</figcaption></figure>' for i, s in enumerate(sp))}</div></div></section>
<section class="practice-facts" aria-labelledby="facts-h"><div class="wrap"><h2 id="facts-h">{T['know']}</h2>
  <dl class="facts">
    <div><dt>{T['f_access']}</dt><dd>{C.PRACTICE["access"]}</dd></div>
    <div><dt>{T['f_diag']}</dt><dd>{T['f_diag_p']}</dd></div>
    <div><dt>{T['f_hyg']}</dt><dd>{C.PRACTICE["hygiene"]}</dd></div>
    <div><dt>{T['f_equip']}</dt><dd>{C.PRACTICE["equipment"]}</dd></div>
    <div><dt>{T['f_langs']}</dt><dd>{T['f_langs_p']}</dd></div>
  </dl></div></section>"""
            mapblock = f'<div class="map-sec" aria-label="{T["map"]}"><div class="wrap"><div class="map"><iframe title="{T["map"]}, {L["name"]}" src="{L["embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></div>' if L["embed"] else ""
            return phero(T, C, f"{T['loc_of']} {L['name']}", L["short"], [(T["home"], px + "/"), (practices_label, px + "/cabinets/"), (L["name"], None)],
                         picture(L["img"], L["alt"], "(max-width: 900px) 100vw, 40vw", eager=True)) + f"""
<section class="loc-facts" aria-label="{T['know']}">
  <div class="wrap loc-facts-in">
    <dl class="facts facts-tight">{facts}</dl>
    <aside class="side"><h2 class="side-h">{T['come']}</h2><p>{L["short"]}</p>
      <a class="btn" href="{L['booking']}" target="_blank" rel="noopener">{T['book']}</a>
      <a class="btn btn-line" href="{L['maps']}" target="_blank" rel="noopener">{T['directions']}</a>
      <a class="btn btn-line" href="{px}/formulaire/">{T['form']}</a></aside>
  </div>
</section>
{mapblock}{gallery}
<section class="cab-soins" aria-labelledby="cs-h"><div class="wrap"><h2 id="cs-h">{T['cab_soins']} {L['name']}</h2>
  {('<ul class="fam-list">' + ''.join(f'<li><a href="' + px + '/soins/' + f['slug'] + '/"><b>' + f['name'] + '</b><span>' + f['line'] + '</span></a></li>' for f in C.FAMILIES) + '</ul>') if L['verified'] else '<p class="note">' + T['pending_team'] + '</p>'}
</div></section>
<section class="cab-contact band-tint" id="contact" aria-labelledby="cc-h"><div class="wrap cab-contact-in">
  <div><h2 id="cc-h">{T['cab_contact']} {L['name']}</h2><p>{T['cab_contact_p']}</p></div>
  <dl class="facts facts-tight">
    <div><dt>{T['facts'][3][0]}</dt><dd><a href="{L['tel']}">{L['phone']}</a><br><span class="muted">{L['hours']}</span></dd></div>
    <div><dt>{T['facts'][4][0]}</dt><dd><a href="mailto:{L['mail']}">{L['mail']}</a></dd></div>
    <div><dt>{T['facts'][0][0]}</dt><dd>{L['address']}, {L['zip_city']}</dd></div>
  </dl>
  <div class="acts"><a class="btn" href="{L['booking']}" target="_blank" rel="noopener">{T['book']}</a><a class="btn btn-line" href="{px}/formulaire/?cabinet={L['slug']}">{T['form_loc']}</a><a class="btn btn-line" href="{px}/contact/">Contact</a></div>
</div></section>
<section class="team" aria-labelledby="lteam-h"><div class="wrap"><div class="sec-head"><h2 id="lteam-h">{T['who_at']} {L['name']}</h2></div>{team_block}</div></section>
"""
        page(f"/cabinets/{L['slug']}/", *C.META[L["slug"]], "/cabinets/", loc_page, [C.schema_dentist(base)] if L["verified"] else (), closing_args=())

    # ---------------------------------------------------------- soins
    def soins():
        fams = ""
        for i, f in enumerate(C.FAMILIES):
            cares = "".join(f'<li><a href="{px}/soins/{c}/"><div class="cl-n">{C.CARE_SHORT[c]}</div><div class="cl-q">{C.care(c)["h1"]}</div></a></li>' for c in f["cares"])
            who = ", ".join(C.P[w]["name"] for w in f["who"])
            fams += f"""
<section class="fam{' fam-flip' if i % 2 else ''}{' band-tint' if i % 2 else ''}" aria-labelledby="fam-{f['slug']}">
  <div class="wrap fam-in">
    <div class="fam-pic">{picture(f["img"], f["alt"], "(max-width: 900px) 100vw, 38vw")}</div>
    <div class="fam-txt"><h2 id="fam-{f['slug']}"><a href="{px}/soins/{f['slug']}/">{f["name"]}</a></h2><p class="fam-line">{f["line"]}</p><p>{f["intro"]}</p>
      <ul class="care-list">{cares}</ul><p class="muted">{T['by']} {who}.</p></div>
  </div>
</section>"""
        return phero(T, C, T["soins_title"], T["soins_lead"], [(T["home"], px + "/"), (C.NAV[1][0], None)], side=side("stock/examen-dentiste.jpg", "tooth")) + fams + f'<div class="note-sec"><div class="wrap"><p class="note">{C.ORTHO_NOTE}</p></div></div>'
    page("/soins/", *C.META["soins"], "/soins/", soins, closing_args=())

    for f in C.FAMILIES:
        def fam_page(f=f):
            cares = "".join(f'<li class="care-row"><a href="{px}/soins/{c}/"><h2>{C.care(c)["name"]}</h2><p>{C.care(c)["h1"]}</p><span class="muted">{C.care(c)["desc"]}</span></a></li>' for c in f["cares"])
            who = "".join(portrait(C.P[w], "(max-width: 700px) 45vw, 150px") for w in f["who"])
            others = "".join(f'<li><a href="{px}/soins/{o["slug"]}/">{o["name"]}</a><span>{o["line"]}</span></li>' for o in C.FAMILIES if o is not f)
            return phero(T, C, f["name"], f["intro"], [(T["home"], px + "/"), (C.NAV[1][0], px + "/soins/"), (f["name"], None)],
                         picture(f["img"], f["alt"], "(max-width: 900px) 100vw, 36vw", eager=True)) + f"""
<section class="care-sec" aria-label="{f['name']}">
  <div class="wrap care-sec-in"><ul class="care-rows">{cares}</ul>
    <aside class="side"><h2 class="side-h">{T['who_cares_pl']}</h2><ul class="portraits portraits-side">{who}</ul><a class="btn" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a></aside></div>
</section>
<section class="others band-tint" aria-labelledby="others-h"><div class="wrap"><h2 id="others-h">{T['others']}</h2><ul class="others-list">{others}</ul></div></section>"""
        page(f"/soins/{f['slug']}/", f"{f['name']} | Cabinet Dentaire", f["line"] + " " + f["intro"][:120], "/soins/", fam_page,
             [{"@context": "https://schema.org", "@type": "CollectionPage", "name": f["name"], "url": base + f"/soins/{f['slug']}/", "inLanguage": T["lang"]}], f["img"], closing_args=())

    for c in C.ALL_CARES:
        cc = C.care(c)
        f = cc["family"]

        def care_page(cc=cc, f=f, c=c):
            secs = "".join(f'<h2>{s["h"]}</h2>' + "".join(f"<p>{p}</p>" for p in s["p"]) for s in cc["sections"])
            who = "".join(portrait(C.P[w], "(max-width: 700px) 45vw, 150px") for w in f["who"])
            rel = "".join(f'<li><a href="{px}/soins/{o}/">{C.CARE_SHORT[o]}</a></li>' for o in f["cares"] if o != c)
            opener = dict(img=picture(cc["img"], cc["name"], "(max-width: 900px) 100vw, 36vw", eager=True)) if theme == "a" else dict(side=side(cc["img"], f["ill"]))
            return phero(T, C, cc["h1"], cc["lead"], [(T["home"], px + "/"), (C.NAV[1][0], px + "/soins/"), (f["name"], px + f"/soins/{f['slug']}/"), (cc["name"], None)],
                         **opener) + f"""
<section class="article" aria-label="{cc['name']}">
  <div class="wrap article-in">
    <article class="prose">{secs}{video_slot(T, picture, cc["img"])}
      <h2>{C.PRACTICAL['h']}</h2>
      <dl class="practical">{''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in C.PRACTICAL['items'])}</dl>
      <p class="note">{' '.join(cc["notes"])}</p></article>
    <aside class="side"><h2 class="side-h">{T['who_cares']}</h2><ul class="portraits portraits-side">{who}</ul>
      <h2 class="side-h">{T['same_family']}</h2><ul class="side-links">{rel}</ul>
      <a class="btn" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a></aside>
  </div>
</section>
""" + faq_block(T, cc["faq"])
        ldobjs = [{"@context": "https://schema.org", "@type": "MedicalWebPage", "name": cc["h1"], "url": base + f"/soins/{c}/", "inLanguage": T["lang"], "about": {"@type": "MedicalProcedure", "name": cc["name"]}}]
        if cc["faq"]:
            ldobjs.append(C.schema_faq(cc["faq"]))
        page(f"/soins/{c}/", cc["title"], cc["desc"], "/soins/", care_page, ldobjs, cc["img"], closing_args=(T["close_care_h"], T["close_care_p"]))

    # ---------------------------------------------------------- team
    def team():
        rows = "".join(f"""
<li class="team-row">
  <a class="team-pic" href="{px}/equipe/{p['slug']}/"><span class="disc">{picture("team/" + p["slug"] + ".png", f'{p["name"]}, {p["role"].lower()}', "(max-width: 700px) 40vw, 240px")}</span></a>
  <div class="team-txt"><h2><a href="{px}/equipe/{p['slug']}/">{p["name"]}</a></h2><p class="team-role">{p["role"]}</p><p>{p["short"]}</p>
    <dl class="team-meta"><div><dt>{T['areas']}</dt><dd>{p["areas"]}</dd></div><div><dt>{T['langs']}</dt><dd>{p["langs"]}</dd></div></dl></div>
</li>""" for p in C.PEOPLE)
        team_banner = picture("stock/team-banner.jpg", "L’équipe du cabinet, ensemble" if lang == "fr" else "The practice team, together", "(max-width: 900px) 100vw, 1100px", eager=True)
        return phero(T, C, T["team_h"], T["team_lead"], [(T["home"], px + "/"), (dict((h, l) for l, h in C.NAV)["/equipe/"], None)], banner=team_banner) + f'<section class="team-sec" aria-label="{dict((h, l) for l, h in C.NAV)["/equipe/"]}"><div class="wrap"><ul class="team-rows">{rows}</ul></div></section>'
    page("/equipe/", *C.META["equipe"], "/equipe/", team, closing_args=())

    for p in C.PEOPLE:
        def person(p=p):
            clist = "".join(f'<li><a href="{px}/soins/{c}/">{C.CARE_SHORT[c]}</a></li>' for c in cares_of(p))
            paras = "".join(f"<p>{x}</p>" for x in C.bio(p))
            return f"""
<header class="phero">
  <div class="wrap profile">
    <div class="profile-pic"><span class="disc disc-big">{picture("team/" + p["slug"] + ".png", p["name"], "(max-width: 700px) 70vw, 380px", eager=True)}</span></div>
    <div class="profile-txt">
      {crumbs(T, [(T["home"], px + "/"), (dict((h, l) for l, h in C.NAV)["/equipe/"], px + "/equipe/"), (p["name"], None)])}
      <h1>{p["name"]}</h1><p class="team-role">{p["role"]}</p>
      <div class="prose">{paras}</div>
      <dl class="team-meta"><div><dt>{T['areas']}</dt><dd>{p["areas"]}</dd></div><div><dt>{T['langs']}</dt><dd>{p["langs"]}</dd></div><div><dt>{T['practice']}</dt><dd>Meyrin, {C.ADDRESS}<br><span class="muted">Nyon : [À CONFIRMER]</span></dd></div></dl>
      {'<h2 class="side-h">' + T['cares_of'] + '</h2><ul class="inline inline-big">' + clist + '</ul>' if clist else ''}
      <p class="muted small">{T['source']} {C.UPDATED}.</p>
    </div>
  </div>
</header>"""
        page(f"/equipe/{p['slug']}/", f"{p['name']}, {p['role'].lower()}", p["short"] + " " + p["areas"], "/equipe/", person,
             [{"@context": "https://schema.org", "@type": "Person", "name": p["name"], "jobTitle": p["role"], "worksFor": {"@type": "Dentist", "name": FR.NAME}, "url": base + f"/equipe/{p['slug']}/"}],
             closing_args=(T["close_person_h"], T["close_person_p"]))

    # ---------------------------------------------------------- first visit
    def visit():
        vsteps = "".join(f'<li class="vstep"><span class="num" aria-hidden="true">{i:02d}</span><div><p class="vstep-k">{s["k"]}</p><h2>{s["t"]}</h2><p>{s["p"]}</p></div></li>' for i, s in enumerate(C.VISIT_STEPS, 1))
        return phero(T, C, T["visit_h"], T["visit_lead"], [(T["home"], px + "/"), ((T["foot_visit"]), None)],
                     picture("photos/cabinet-room.jpg", "", "(max-width: 900px) 100vw, 36vw", eager=True)) + f"""
<section class="vsteps-sec" aria-label="{T['visit_h']}">
  <div class="wrap vsteps-in"><ol class="vsteps">{vsteps}</ol>
    <aside class="side"><h2 class="side-h">{T['bring']}</h2><ul class="side-list">{''.join(f'<li>{x}</li>' for x in T['bring_items'])}</ul><p class="muted">{T['bring_note']}</p>
      <p>{T['fill_form']}</p><a class="btn" href="{px}/formulaire/">{T['form']}</a><a class="btn btn-line" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a></aside></div>
</section>
<section class="philo band-tint" aria-label="{T['calm'][:30]}"><div class="wrap philo-in"><div class="philo-txt"><div class="statement">{T['calm']}</div><p>{T['calm_p']}</p></div><div class="philo-pic mask">{picture("stock/enfant-controle.jpg", "", "(max-width: 900px) 100vw, 36vw")}</div></div></section>"""
    page("/premiere-visite/", *C.META["visite"], "/premiere-visite/", visit, closing_args=())

    # ---------------------------------------------------------- patient form
    def formp():
        return phero(T, C, T["form_h"], T["form_lead"], [(T["home"], px + "/"), (T["form"], None)], cta=False, side=side("stock/patiente-fauteuil.jpg", "implant")) + form_page(px, C, T)
    page("/formulaire/", *C.META.get("formulaire", ("Formulaire patient | Cabinet Dentaire", "Remplissez vos informations avant votre premier rendez-vous, à votre rythme. Facultatif, conservé sur votre appareil jusqu’à l’envoi ou l’impression.")), "", formp)

    # ---------------------------------------------------------- emergencies
    def urg():
        E = C.EMERGENCY
        return f"""
<header class="phero phero-urg">
  <div class="wrap phero-in">
    <div class="phero-txt">{crumbs(T, [(T["home"], px + "/"), (T["emergency"], None)])}<h1>{T['urg_h']}</h1><p class="lead">{T['urg_lead']}</p></div>
    <div class="urg-tel"><p class="urg-k">{T['urg_open']}</p><a class="urg-num" href="{C.TEL}">{C.PHONE}</a><p>{C.HOURS}</p></div>
  </div>
</header>
<section class="urg" aria-labelledby="urg-when"><div class="wrap urg-in">
  <div><h2 id="urg-when">{T['urg_when']}</h2><ul class="check">{''.join(f'<li>{x}</li>' for x in E["when"])}</ul></div>
  <div><h2>{T['urg_wait']}</h2><ul class="check">{''.join(f'<li>{x}</li>' for x in E["meanwhile"])}</ul></div></div></section>
<section class="vital" aria-labelledby="vital-h"><div class="wrap vital-in"><div><h2 id="vital-h">{T['urg_vital']}</h2><p>{E["vital"]}</p></div><div><h2>{T['urg_after']}</h2><p>{E["after"]}</p></div></div></section>
<section class="article" aria-labelledby="how-h"><div class="wrap prose"><h2 id="how-h">{T['urg_how']}</h2><p>{T['urg_how_p1']}</p><p>{T['urg_how_p2']} <a href="{px}/soins/urgence-dentaire-meyrin/">{T['urg_link']}</a></p></div></section>
""" + faq_block(T, C.care("urgence-dentaire-meyrin")["faq"])
    page("/urgences/", *C.META["urgences"], "/urgences/", urg, [C.schema_faq(C.care("urgence-dentaire-meyrin")["faq"])])

    # ---------------------------------------------------------- contact
    def contact():
        cols = ""
        for L in C.LOCATIONS:
            cols += f"""
<div class="ccol"><h2>{L["name"]}</h2>
  <dl class="facts facts-tight">
    <div><dt>{T['facts'][0][0]}</dt><dd>{L["address"]}<br>{L["zip_city"]}<br><span class="muted">{L["floor"]}</span></dd></div>
    <div><dt>{T['facts'][3][0]}</dt><dd><a href="{L["tel"]}">{L["phone"]}</a></dd></div>
    <div><dt>{T['facts'][4][0]}</dt><dd><a href="mailto:{L["mail"]}">{L["mail"]}</a></dd></div>
    <div><dt>{T['facts'][2][0]}</dt><dd>{L["hours"]}</dd></div>
    <div><dt>{T['facts'][5][0]}</dt><dd>{(L["tram"] + ", ") if L["tram"] else ""}{L["bus"]}<br><span class="muted">{T['f_stop']} {L["stop"]}</span></dd></div>
  </dl>
  <div class="acts"><a class="btn" href="{L['booking']}" target="_blank" rel="noopener">{T['book']}</a><a class="btn btn-line" href="{L['maps']}" target="_blank" rel="noopener">{T['route']}</a></div>
</div>"""
        return phero(T, C, T["contact_h"], T["contact_lead"], [(T["home"], px + "/"), ("Contact", None)], cta=False, side=side("photos/cabinet-sterilisation.jpg", "toothbrush")) + f"""
<section class="contact" aria-label="Contact"><div class="wrap ccols">{cols}</div></section>
<section class="form-sec band-tint" aria-label="{T['write_h']}">
  <div class="wrap form-in">
    <div class="form-side"><h2>{T['write_h']}</h2><p>{T['write_p'].format(phone=C.PHONE)}</p><p><a class="link" href="{px}/formulaire/">{T['form']}</a></p></div>
    <form class="form" action="mailto:{C.MAIL}" method="post" enctype="text/plain" novalidate>
      <div class="field"><label for="nom">{T['f_name']}</label><input id="nom" name="nom" type="text" autocomplete="name" required></div>
      <div class="field"><label for="email">{T['f_email']}</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="tel">{T['f_phone']}</label><input id="tel" name="tel" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="cabinet">{T['f_cab_opt']}</label><select id="cabinet" name="cabinet"><option value="">{T['f_cab_none']}</option><option>Meyrin</option><option>Nyon</option></select></div>
      <div class="field"><label for="motif">{T['f_reason']}</label><select id="motif" name="motif">{''.join(f'<option>{r}</option>' for r in T['f_reasons'])}</select></div>
      <div class="field"><label for="msg">{T['f_msg']}</label><textarea id="msg" name="message" rows="5" required></textarea></div>
      <button class="btn" type="submit">{T['f_send']}</button>
      <p class="form-ok" hidden role="status">{T['f_ok']}</p>
    </form>
  </div>
</section>
<div class="map-sec" aria-label="{T['map']}"><div class="wrap"><div class="map"><iframe title="{T['map']}, Meyrin" src="{C.MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></div>
""" + faq_block(T, C.CONTACT_FAQ)
    page("/contact/", *C.META["contact"], "/contact/", contact, [C.schema_dentist(base), C.schema_faq(C.CONTACT_FAQ)])

    # ---------------------------------------------------------- blog
    def blog_index():
        posts = "".join(f"""
<li class="post"><a href="{px}/blog/{b['slug']}/">{picture(b["img"], "", "(max-width: 900px) 100vw, 30vw")}<span class="post-k">{b["kicker"]}</span><h2>{b["title"]}</h2><p>{b["desc"]}</p><span class="link">{T['blog_read']}</span></a></li>""" for b in C.BLOG)
        return phero(T, C, T["blog_h"], T["blog_lead"], [(T["home"], px + "/"), ("Blog", None)], cta=False, side=side("stock/jeune-homme-sourire.jpg", "braces")) + f'<section class="blog-list" aria-label="Blog"><div class="wrap"><ul class="posts posts-big">{posts}</ul></div></section>'
    page("/blog/", *C.META["blog"], "/blog/", blog_index)

    for b in C.BLOG:
        def post(b=b):
            others = "".join(f'<li><a href="{px}/blog/{o["slug"]}/">{o["title"]}</a><span>{o["kicker"]}</span></li>' for o in C.BLOG if o is not b)
            return phero(T, C, b["title"], b["desc"], [(T["home"], px + "/"), ("Blog", px + "/blog/"), (b["kicker"], None)], picture(b["img"], "", "(max-width: 900px) 100vw, 36vw", eager=True), cta=False) + f"""
<section class="article" aria-label="{b['title']}">
  <div class="wrap article-in">
    <article class="prose">{b["body"]}<p class="note">{b['date']}</p></article>
    <aside class="side"><h2 class="side-h">{T['blog_all']}</h2><ul class="side-links">{others}</ul><a class="btn" href="{C.BOOKING}" target="_blank" rel="noopener">{T['book']}</a></aside>
  </div>
</section>"""
        page(f"/blog/{b['slug']}/", b["title"] + " | Cabinet Dentaire", b["desc"], "/blog/", post,
             [{"@context": "https://schema.org", "@type": "Article", "headline": b["title"], "datePublished": b["date"], "inLanguage": T["lang"], "author": {"@type": "Organization", "name": FR.NAME}, "url": base + f"/blog/{b['slug']}/"}], b["img"], closing_args=())

    # ---------------------------------------------------------- legal, 404
    def legal():
        return phero(T, C, T["legal"], T["legal_p"], [(T["home"], px + "/"), (T["legal"], None)], cta=False) + f"""
<section class="article"><div class="wrap prose">
<h2>{T['publisher']}</h2><p>{FR.NAME}, {FR.ADDRESS}, {FR.ZIP_CITY}. [RAISON SOCIALE ET NUMÉRO IDE À CONFIRMER]</p>
<h2>{T['pub_manager']}</h2><p>[À CONFIRMER]</p>
<h2>{T['hosting']}</h2><p>[HÉBERGEUR À CONFIRMER]</p>
<h2>{T['data']}</h2><p>{T['f_consent_note']}</p>
<h2>{T['credits']}</h2><p>{T['credits_p']}</p>
</div></section>"""
    page("/mentions-legales/", T["legal"] + " | Cabinet Dentaire", T["legal_p"], "", legal)

    def nf():
        return phero(T, C, T["nf"], T["nf_p"], [(T["home"], px + "/"), (T["nf"], None)])
    page("/404.html", T["nf"] + " | Cabinet Dentaire", T["nf_p"], "", nf)

    out_dir = HERE.parent / "dist" / px.strip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    seen, uniq = set(), []
    for i in index:
        if i["u"].endswith(".html") or i["u"] == px + "/" or i["t"] in seen:
            continue
        seen.add(i["t"]); uniq.append(i)
    (out_dir / "search.json").write_text(json.dumps(uniq, ensure_ascii=False), encoding="utf-8")
    return urls
