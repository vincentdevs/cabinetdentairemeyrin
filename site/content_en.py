"""English content. Same structures as content.py, same facts, translated copy.

Anything the practice has not confirmed stays a bracketed placeholder here too.
The treatment pages are translated in content/content-en.json.
"""
import copy
import json
import pathlib

import content as FR

HERE = pathlib.Path(__file__).parent
CARES_EN = json.load(open(HERE / "content" / "content-en.json", encoding="utf-8"))

# facts that do not change
DOMAIN, NAME, PHONE, PHONE_INTL, TEL, MAIL = FR.DOMAIN, FR.NAME, FR.PHONE, FR.PHONE_INTL, FR.TEL, FR.MAIL
ADDRESS, ZIP_CITY, BOOKING, MAPS, MAPS_EMBED = FR.ADDRESS, FR.ZIP_CITY, FR.BOOKING, FR.MAPS, FR.MAPS_EMBED
FLOOR = "1st floor, no steps"
HOURS = "Monday to Friday, 8am to 6.30pm"
STOP = "Meyrin, Hôpital de la Tour"
TRAM = "Tram 18"
BUS = "Buses 56, 57, 68, 71 and A3"
UPDATED = "25 August 2026"

NAV = [("Home", "/"), ("Treatments", "/soins/"), ("Practices", "/cabinets/"),
       ("Team", "/equipe/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
BLOG = json.load(open(HERE / "content" / "blog-en.json", encoding="utf-8"))
PRACTICAL = dict(
    h="In practice",
    items=[
        ("Appointments", "Book online or call " + PHONE + ". You do not need to know the name of the treatment, just say what brings you. Appointment length: [DURATION TO BE CONFIRMED]."),
        ("Estimate and funding", "In Switzerland, most dental care is not covered by basic health insurance (LAMal/KVG). When a treatment is proposed, a written estimate is given to you before starting. [PAYMENT AND INVOICING TERMS TO BE CONFIRMED]"),
        ("Accident", "If the treatment follows an accident, it is reported to your accident insurance (LAA/UVG) or your health insurer. Mention it when booking, the team explains the declaration."),
        ("Where", "The treatment is provided at the Meyrin practice. For Nyon, the treatments offered are still to be confirmed. [TO BE CONFIRMED]"),
    ],
)

PEOPLE = copy.deepcopy(FR.PEOPLE)
_EN_PEOPLE = {
    "victor-palmen": dict(role="Dentist", langs="French, German, English", areas="General dentistry, prevention, children's care", short="General practice, prevention and children's dentistry."),
    "edouard-di-donna": dict(role="Oral surgeon", langs="French, Italian, English", areas="Oral surgery, stomatology, implantology", short="Oral surgery, stomatology and implantology."),
    "cilien-prieu": dict(role="Dentist", langs="French, English, Spanish", areas="Check-ups, cavities, prevention, children's care", short="Check-ups, cavity treatment, prevention and children's dentistry."),
    "juliana": dict(role="Dental hygienist", langs="French, Portuguese, Spanish", areas="Professional cleaning, scaling, gums", short="Professional hygiene and gum care."),
    "zainne": dict(role="Dental assistant", langs="[LANGUAGES TO BE CONFIRMED]", areas="Reception, instrument preparation, chairside assistance", short="Reception, instrument preparation and chairside assistance."),
    "luana": dict(role="Dental assistant", langs="[LANGUAGES TO BE CONFIRMED]", areas="Reception, instrument preparation, appointment follow-up", short="Reception, instrument preparation and appointment follow-up."),
}
for _p in PEOPLE:
    _p.update(_EN_PEOPLE[_p["slug"]])
P = {p["slug"]: p for p in PEOPLE}

_BIO = {
    "victor-palmen": ["Victor Palmen practises as a dentist at Cabinet Dentaire Meyrin. His work covers general dentistry, prevention and children's care. He speaks French, German and English.",
                      "Victor Palmen graduated from the Faculty of Medicine of the University of Geneva. The practice states that he has worked since 2020 as an assistant dentist at the University Clinic of Dental Medicine in Geneva, in the paediatric dentistry division.",
                      "He works in general practice with particular attention to prevention and children's care. He also collaborates with the Hôpital de La Tour."],
    "edouard-di-donna": ["Edouard Di Donna practises at Cabinet Dentaire Meyrin in oral surgery, stomatology and implantology. He speaks French, Italian and English.",
                         "Edouard Di Donna graduated from the Faculty of Medicine of the University of Geneva. The practice states that he directed his work towards oral surgery and implantology within the department of oral and maxillofacial surgery of the Geneva University Hospitals.",
                         "He worked there as a resident dentist and then as chief resident until 2022. His work at the practice is dedicated to oral surgery and stomatology."],
    "cilien-prieu": ["Cilien Prieu practises as a dentist at Cabinet Dentaire Meyrin. His work covers check-ups, cavity treatment, prevention and children's care. He speaks French, English and Spanish.",
                     "Cilien Prieu graduated from the Faculty of Medicine of Valencia. At the practice he provides general care, from the oral check-up to the treatment of cavities.",
                     "His practice also gives a place to prevention and to children's dental care."],
    "juliana": ["Juliana provides hygiene care, scaling and gum treatment at Cabinet Dentaire Meyrin. She speaks French, Portuguese and Spanish.",
                "Juliana obtained her diploma from the Geneva School of Dental Hygienists in 2016.",
                "At the practice she looks after gum treatments and hygiene care. The appointment can include scaling, an examination of the gums and advice adapted to the areas that need more attention."],
}


def bio(person):
    if not person["source"]:
        return ["The practice has not published a detailed profile. [BIOGRAPHY TO BE CONFIRMED]"]
    return _BIO[person["slug"]]


CARE_SHORT = {
    "controle-dentaire-meyrin": "Dental check-up", "carie-dentaire-meyrin": "Cavities", "traitement-racine-meyrin": "Root canal treatment",
    "dentiste-enfant-meyrin": "Children's dentistry", "urgence-dentaire-meyrin": "Dental emergency", "hygieniste-dentaire-meyrin": "Hygienist appointment",
    "detartrage-meyrin": "Scaling", "soins-gencives-meyrin": "Gum care", "implant-dentaire-meyrin": "Dental implant",
    "chirurgie-orale-meyrin": "Oral surgery", "dents-sagesse-meyrin": "Wisdom teeth", "extraction-dentaire-meyrin": "Tooth extraction",
    "implant-ou-bridge": "Implant or bridge", "dent-manquante": "A missing tooth", "remplacer-plusieurs-dents": "Replacing several teeth",
    "couronne-dentaire-meyrin": "Dental crown", "facettes-dentaires-meyrin": "Veneers", "blanchiment-dentaire-meyrin": "Teeth whitening",
    "esthetique-dentaire-meyrin": "Whitening or veneers",
}
CARE_IMG = FR.CARE_IMG
ALL_CARES = FR.ALL_CARES

FAMILIES = copy.deepcopy(FR.FAMILIES)
_EN_FAM = {
    "prevenir": dict(name="Prevent", line="Check-ups, hygiene and gum health.",
                     intro="The check-up spots what does not hurt yet, the hygiene appointment removes what brushing cannot, and gum follow-up stops an inflammation from settling in. Children are seen for a first check-up at their own pace.",
                     alt="Child during a check-up, reassured by the dentist"),
    "soigner": dict(name="Treat", line="Cavities, root canal treatments and conservative care.",
                    intro="An affected tooth is examined before it is treated. Depending on what the examination shows, care ranges from a filling to a root canal treatment, and oral surgery takes over for an extraction or a wisdom tooth. Pain that cannot wait is seen as an emergency.",
                    alt="Examination of a patient by the dentist"),
    "restaurer": dict(name="Restore", line="Crowns, prostheses and implants.",
                      intro="A badly damaged tooth can be protected by a crown, a missing tooth replaced by an implant or a bridge. The practice's oral surgeon places implants on site, and the choice between solutions is explained before any decision.",
                      alt="Close-up of a mirror examination"),
    "harmoniser": dict(name="Enhance the smile", line="Cosmetic dentistry, whitening and veneers.",
                       intro="Whitening acts on the shade of natural teeth, veneers correct a shape or a colour. An assessment of the teeth and gums always comes before the decision, because the result depends on what the examination shows.",
                       alt="Smiling patient at the end of an appointment"),
}
for _f in FAMILIES:
    _f.update(_EN_FAM[_f["slug"]])
FAM = {f["slug"]: f for f in FAMILIES}
FAM_OF = {}
for _f in FAMILIES:
    for _c in _f["cares"]:
        FAM_OF[_c] = _f

ORTHO_NOTE = "Orthodontics does not appear in this list: the practice has not confirmed whether it covers this field. [ORTHODONTICS TO BE CONFIRMED]"


def care(slug):
    fr = FR.care(slug)
    en = CARES_EN[slug]
    return dict(slug=slug, name=CARE_SHORT[slug], title=en["title"], desc=en["desc"], h1=en["h1"], lead=en["lead"],
                sections=en["sections"], faq=en["faq"], notes=en.get("notes", []), img=fr["img"], family=FAM_OF[slug])


HOME_STEPS = [
    ("You arrive and we get to know each other", "The reason for your visit, your history, what worries or bothers you. Nothing is decided at this stage."),
    ("We examine before we treat", "Teeth, gums, old restorations. X-rays are only suggested when they add information that is needed."),
    ("We explain what we observed", "In plain words and, when useful, with the images of your own mouth. You can ask every question you have."),
    ("We go through the options", "When several solutions exist, each one is presented with its steps, its duration and its limits."),
    ("You decide what happens next", "With all the information you need, and a written estimate on request when a treatment is proposed."),
]

VISIT_STEPS = [
    dict(k="Booking", t="Online or by phone", p="Book in the online diary at any hour, or call the practice Monday to Friday, 8am to 6.30pm. You do not need to know the name of the treatment, just say what brings you and the team directs you to the right person."),
    dict(k="Arrival", t="First floor, no steps", p="The practice is at Place de la Diversité 1 in Meyrin, on the first floor of a building with no steps to climb. The « Meyrin, Hôpital de la Tour » stop is next door, and the Parking des Sports sits under the building."),
    dict(k="What to bring", t="What really helps", p="An identity document, the list of your medicines if you take any, your recent X-rays if you have some, and the name of your supplementary dental insurance if you hold one. If you have none of these, come anyway."),
    dict(k="First conversation", t="We start by listening", p="The practitioner asks what brings you, since when, and what you have already noticed. Your medical history and any worries are part of the conversation, because they change how the appointment is run."),
    dict(k="Examination", t="Teeth, gums, restorations", p="The practitioner examines the teeth, old restorations, gums, deposits and, when it concerns your situation, how the teeth meet. A check-up can spot a change before it causes discomfort."),
    dict(k="X-rays", t="Only when they are useful", p="X-rays are not systematic. They are suggested when they show something the examination alone cannot see, for instance between two teeth or under an old repair. The reason for the image is explained to you."),
    dict(k="Diagnosis", t="What was found", p="The practitioner tells you what was observed, what is fine and what needs care or monitoring. The conclusion can also be that no treatment is needed, and that is a result like any other."),
    dict(k="Explanation", t="In plain words", p="Every observation is explained before any procedure is proposed. If a term is unclear, ask, the answer is part of the appointment."),
    dict(k="Treatment options", t="When several solutions exist", p="When a treatment can be done in several ways, each option is presented with its steps, duration, limits and follow-up. You do not have to choose on the spot."),
    dict(k="Estimate", t="Before you commit", p="When a treatment is proposed, you can ask for a written estimate before starting. It lists the planned procedures and gives you time to decide."),
    dict(k="Next steps", t="You decide", p="Depending on the case, the appointment ends with no treatment, with monitoring, with a hygiene appointment or with a treatment to plan. What comes next is set with you, never for you."),
]

TRUST = [
    ("Explaining before acting", "Every observation is explained and every step is announced. You know what is going to be done before it starts."),
    ("One team, from check-up to implant", "General dentistry, oral surgery, implantology and dental hygiene are all carried out on site by the practice team whenever possible."),
    ("X-rays when they are useful", "They are suggested when they add information the examination alone does not give, and the reason is explained."),
    ("Access without steps", "The Meyrin practice is on the first floor with no steps to climb. If you have a specific need, call before your appointment."),
    ("Six languages spoken", "French, English, German, Italian, Spanish and Portuguese, depending on who receives you."),
    ("Emergencies during opening hours", "Call " + PHONE + " and describe what is happening. The team tells you when to come."),
]

PRACTICE = dict(
    philosophy=["We start by looking, understanding and explaining. Treatment comes next, and only once you have agreed to it.",
                "This way of working comes down to three habits: examine before proposing, explain before acting, and leave the decision to the person in the chair."],
    spaces=[dict(img="photos/cabinet-hero.jpg", alt="Treatment room with the chair and natural light", cap="The main treatment room"),
            dict(img="photos/cabinet-room.jpg", alt="Chair and instruments prepared", cap="The chair, prepared before each appointment"),
            dict(img="photos/cabinet-room-alt.jpg", alt="Second treatment room", cap="The second treatment room"),
            dict(img="photos/cabinet-sterilisation.jpg", alt="Instrument sterilisation room", cap="The sterilisation room")],
    equipment="The practice has not published its equipment list. X-rays are suggested when they add information needed for the diagnosis. [EQUIPMENT TO BE CONFIRMED]",
    hygiene="Instruments go through a dedicated sterilisation room between two patients. The practice has not published the detail of its protocols. [HYGIENE PROTOCOL TO BE CONFIRMED]",
    access="The practice is on the first floor of a building linked to imad, with no steps to climb. The practice's website states that access for people with reduced mobility is made easier. The Parking des Sports is located under the practice, with an entrance on Avenue Louis-Rendu, and the Parking des Vergers is a few minutes' walk away.",
)

EMERGENCY = dict(
    when=["Pain that becomes hard to bear", "A tooth that breaks or moves after a knock", "Swelling of the gum, cheek or face",
          "Bleeding that does not stop after a procedure", "A tooth knocked out of its socket"],
    meanwhile=["Do not apply any product directly on the tooth or gum without professional advice.",
               "After a procedure or a knock, follow the instructions given by the practice.",
               "For an injury, note when the knock happened and whether a tooth moved, broke or came out.",
               "If symptoms change or get worse, call again so the situation can be reassessed."],
    vital="Difficulty breathing, loss of consciousness or uncontrollable bleeding are matters for the emergency services. In Switzerland, call 144 immediately.",
    after="Outside opening hours, follow the instructions on the practice's answering machine or contact the on-call service of the SSO Geneva. [ON-CALL SERVICE NUMBER TO BE CONFIRMED]",
)

CONTACT_FAQ = [
    ("Do I need to know the name of the treatment to book?", "No. Say what brings you, the team directs you to the person who provides that care."),
    ("Can I book for someone else?", "Yes. Give the name of the person who will come and a number where they can be reached."),
    ("What if I am in pain today?", "Call " + PHONE + " and describe the situation. The team tells you when to come. In a life-threatening emergency, call 144."),
    ("Is the form meant for emergencies?", "No. For an emergency, call. The form is for questions that can wait for an answer by email."),
]

META = dict(
    home=("Dentist in Meyrin and Nyon | Cabinet Dentaire", "Dental practice in Meyrin, Place de la Diversité 1, and in Nyon. Check-ups, hygiene, treatments, implants and cosmetic dentistry by one team. Book online or call 022 320 19 19."),
    soins=("Dental treatments in Meyrin and Nyon | Prevent, treat, restore, enhance", "All the treatments of Cabinet Dentaire, organised around your need: check-up, hygiene, cavities, root canals, implants, crowns, whitening and emergencies."),
    equipe=("The team | Cabinet Dentaire Meyrin and Nyon", "Two dentists, an oral surgeon, a dental hygienist and two assistants. Each profile says what the person does and in which languages."),
    visite=("What happens at a first appointment | Cabinet Dentaire", "From booking to decision: arrival, documents, examination, X-rays if needed, explanation, options and estimate. What to expect, step by step."),
    cabinet=("The practice | Cabinet Dentaire Meyrin", "Treatment rooms, sterilisation, step-free access and the way of working at Cabinet Dentaire Meyrin, Place de la Diversité 1."),
    urgences=("Dental emergency in Meyrin | Cabinet Dentaire", "Pain, broken tooth, swelling or injury: call 022 320 19 19 Monday to Friday, 8am to 6.30pm. What to do while you wait and when to call 144."),
    contact=("Contact and access | Cabinet Dentaire Meyrin and Nyon", "Place de la Diversité 1, 1217 Meyrin, first floor with no steps. Tram 18, buses 56, 57, 68, 71 and A3, Meyrin, Hôpital de la Tour stop. Phone 022 320 19 19."),
    cabinets=("Our practices, Meyrin and Nyon | Cabinet Dentaire", "Two practices, one team. Meyrin, Place de la Diversité 1, and Nyon. Address, hours, access and booking for each practice."),
    meyrin=("Cabinet Dentaire Meyrin, Place de la Diversité 1", "The Meyrin practice: address, hours, access by tram 18 and bus, Parking des Sports, team and booking. First floor, no steps."),
    nyon=("Cabinet Dentaire Nyon | Details to come", "The Nyon practice. Practical details will be published as soon as the practice confirms them. Book online or call 022 320 19 19."),
    blog=("The practice blog | Understanding dental care", "Articles from Cabinet Dentaire Meyrin and Nyon to understand dental care: prevention, wisdom teeth, whitening, children. No jargon, no promises."),
    formulaire=("Patient form | Cabinet Dentaire", "Fill in your details before your first appointment, at your own pace: identity, insurance, contact. Optional, stored on your device only until you send or print it."),
)

LOCATIONS = copy.deepcopy(FR.LOCATIONS)
LOCATIONS[0].update(floor=FLOOR, hours=HOURS, stop=STOP, tram=TRAM, bus=BUS, alt="Treatment room of the Meyrin practice",
                    short="Between the Hôpital de La Tour and the Vergers school, on the first floor, with no steps.",
                    parking="Parking des Sports under the building, entrance on Avenue Louis-Rendu. Parking des Vergers a few minutes' walk away.")
LOCATIONS[1].update(address="[ADDRESS TO BE CONFIRMED]", zip_city="[POSTCODE] Nyon", floor="[FLOOR AND ACCESS TO BE CONFIRMED]", hours="[HOURS TO BE CONFIRMED]",
                    stop="[STOP TO BE CONFIRMED]", bus="[LINES TO BE CONFIRMED]", alt="Treatment room, illustration photo while waiting for those of Nyon",
                    short="The group's second practice. Practical details will be published as soon as the practice confirms them.",
                    parking="[PARKING TO BE CONFIRMED]")
LOC = {l["slug"]: l for l in LOCATIONS}

schema_dentist = FR.schema_dentist
schema_faq = FR.schema_faq
