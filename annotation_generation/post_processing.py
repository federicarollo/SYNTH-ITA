import json

from utils import (
                    preserve_tuples,
                    restore_tuples,
                    select_elements_from_collections,
                    clean_italian_span,
                    numbers_to_numeric_word,
                    numeric_word_to_numbers
)

datapath = 'data'

with open(f"{datapath}/company_objects.json") as f:
    company_to_objects = json.load(f)['categories']

with open(f"{datapath}/proper_names.json", encoding='utf-8') as f:
   proper_names = json.load(f)

with open(f"{datapath}/thefts_dynamics.json", encoding='utf-8') as f:
    dynamics = json.load(f)
    dynamics = restore_tuples(dynamics['dynamics'])

with open(f"{datapath}/regional_origin.json", encoding='utf-8') as f:
    regional_origin = json.load(f)

with open(f"{datapath}/provincial_origin.json", encoding='utf-8') as f:
    provincial_origin = json.load(f)

with open(f"{datapath}/nationalities.json", encoding='utf-8') as f:
    nationalities = json.load(f)

with open(f"{datapath}/municipalities_modena.json", encoding='utf-8') as f:
    municipalities = json.load(f)['municipalities']

with open(f"{datapath}/provinces.json", encoding='utf-8') as f:
    provinces = json.load(f)['provinces']

with open(f"{datapath}/nations.json", encoding='utf-8') as f:
    nations = json.load(f)['nations']

with open(f"{datapath}/regions.json", encoding='utf-8') as f:
    regions = json.load(f)['regions']

with open(f"{datapath}/towns.json", encoding='utf-8') as f:
    towns = json.load(f)['towns']

with open(f"{datapath}/parks.json", encoding='utf-8') as f:
    parks = json.load(f)

with open(f"{datapath}/streets.json", encoding='utf-8') as f:
    streets = json.load(f)

with open(f"{datapath}/regional_origin.json", encoding='utf-8') as f:
    regional_origin = json.load(f)


accents = {
            "\\u00e8": "è",
            "\\u00e0": "à",
            "\\u00ec": "ì",
            "\\u00f2": "ò",
            "\\u00ab": "",
            "Ã¨": "è",
            "Ã²": "ò",
            "Ã¹": "ù",
            "Ã¬": "ì",
            "Ã": "à",
}


objects = []

for company in company_to_objects:
    for el in company['objects']:
        if isinstance(el, tuple):
            objects.append(el[0])
            objects += el[1]
        else:
            objects.append(el)

for dynamic in dynamics:
    for el in dynamic['stolen_objects']:
        if isinstance(el, tuple):
            objects.append(el[0])
            objects += el[1]
        else:
            objects.append(el)


def add_country_names(nationalities):
    # Dictionary mapping nationality roots to country names
    country_mapping = {
                            "afghan": "dell'Afghanistan",
                            "albanese": "dell'Albania",
                            "algerin": "dell'Algeria",
                            "andorran": "dell'Andorra",
                            "angolan": "dell'Angola",
                            "argentin": "dell'Argentina",
                            "armen": "dell'Armenia",
                            "australian": "dell'Australia",
                            "austriac": "dell'Austria",
                            "azer": "dell'Azerbaigian",
                            "bahamense": "delle Bahamas",
                            "bahreinit": "del Bahrain",
                            "barbadian": "delle Barbados",
                            "belg": "del Belgio",
                            "bengalese": "del Bangladesh",
                            "beninese": "del Benin",
                            "bhutanese": "del Bhutan",
                            "bieloruss": "della Bielorussia",
                            "birman": "della Birmania",
                            "bolivian": "della Bolivia",
                            "bosniac": "della Bosnia ed Erzegovina",
                            "botswan": "del Botswana",
                            "brasilian": "del Brasile",
                            "britannic": "del Regno Unito",
                            "bruneian": "del Brunei",
                            "bulgar": "della Bulgaria",
                            "burundese": "del Burundi",
                            "cambogian": "della Cambogia",
                            "camerunense": "del Camerun",
                            "canadese": "del Canada",
                            "capoverdian": "di Capo Verde",
                            "cec": "della Repubblica Ceca",
                            "centrafrican": "della Repubblica Centrafricana",
                            "ciadian": "del Ciad",
                            "cilen": "del Cile",
                            "cinese": "della Cina",
                            "cingalese": "dello Sri Lanka",
                            "cipriot": "di Cipro",
                            "colombian": "della Colombia",
                            "comorian": "delle Comore",
                            "congolese": "del Congo",
                            "costarican": "della Costa Rica",
                            "croat": "della Croazia",
                            "cuban": "di Cuba",
                            "danese": "della Danimarca",
                            "dominican": "della Repubblica Dominicana",
                            "ecuadoregn": "dell'Ecuador",
                            "egizian": "dell'Egitto",
                            "emiratin": "degli Emirati Arabi Uniti",
                            "eritre": "dell'Eritrea",
                            "estone": "dell'Estonia",
                            "etiope": "dell'Etiopia",
                            "figian": "delle Figi",
                            "filippin": "delle Filippine",
                            "finlandese": "della Finlandia",
                            "francese": "della Francia",
                            "gabonese": "del Gabon",
                            "gambian": "del Gambia",
                            "georgian": "della Georgia",
                            "ghanese": "del Ghana",
                            "giamaic": "della Giamaica",
                            "giapponese": "del Giappone",
                            "gibuti": "del Gibuti",
                            "giordan": "della Giordania",
                            "grec": "della Grecia",
                            "grenadin": "di Grenada",
                            "guatemaltec": "del Guatemala",
                            "guinean": "della Guinea",
                            "guyanese": "della Guyana",
                            "haitian": "di Haiti",
                            "honduregn": "dell'Honduras",
                            "indian": "dell'India",
                            "indonesian": "dell'Indonesia",
                            "irachen": "dell'Iraq",
                            "iranian": "dell'Iran",
                            "irlandese": "dell'Irlanda",
                            "islandese": "dell'Islanda",
                            "israelian": "di Israele",
                            "italian": "dell'Italia",
                            "ivorian": "della Costa d'Avorio",
                            "kazak": "del Kazakistan",
                            "kenian": "del Kenya",
                            "kirghis": "del Kirghizistan",
                            "kosovar": "del Kosovo",
                            "kuatian": "del Kuwait",
                            "laotian": "del Laos",
                            "lesothian": "del Lesotho",
                            "lettone": "della Lettonia",
                            "libanese": "del Libano",
                            "liberian": "della Liberia",
                            "libic": "della Libia",
                            "liechtensteinian": "del Liechtenstein",
                            "lituan": "della Lituania",
                            "lussemburghese": "del Lussemburgo",
                            "macedone": "della Macedonia del Nord",
                            "malawian": "del Malawi",
                            "maldivian": "delle Maldive",
                            "malesian": "della Malesia",
                            "malgasci": "del Madagascar",
                            "malian": "del Mali",
                            "maltese": "di Malta",
                            "marocchi": "del Marocco",
                            "marshallese": "delle Isole Marshall",
                            "mauritan": "della Mauritania",
                            "maurizian": "delle Mauritius",
                            "messican": "del Messico",
                            "micronesian": "della Micronesia",
                            "moldav": "della Moldavia",
                            "monegasc": "del Principato di Monaco",
                            "mongol": "della Mongolia",
                            "montenegrin": "del Montenegro",
                            "mozambican": "del Mozambico",
                            "namibian": "della Namibia",
                            "nauruan": "di Nauru",
                            "neozelandese": "della Nuova Zelanda",
                            "nepalese": "del Nepal",
                            "nigerian": "della Nigeria",
                            "nigerin": "del Niger",
                            "nordcorean": "della Corea del Nord",
                            "norvegese": "della Norvegia",
                            "olandese": "dei Paesi Bassi",
                            "omanit": "dell'Oman",
                            "pachistan": "del Pakistan",
                            "palestinese": "della Palestina",
                            "panamense": "di Panama",
                            "papuan": "della Papua Nuova Guinea",
                            "paraguaian": "del Paraguay",
                            "peruvian": "del Perù",
                            "polacc": "della Polonia",
                            "portoghese": "del Portogallo",
                            "qatariot": "del Qatar",
                            "rumen": "della Romania",
                            "ruandese": "del Ruanda",
                            "russ": "della Russia",
                            "salvadoregn": "di El Salvador",
                            "samoan": "delle Samoa",
                            "sanmarinese": "di San Marino",
                            "saudit": "dell'Arabia Saudita",
                            "senegalese": "del Senegal",
                            "serb": "della Serbia",
                            "sierraleonese": "della Sierra Leone",
                            "singaporian": "di Singapore",
                            "sirian": "della Siria",
                            "slovacc": "della Slovacchia",
                            "sloven": "della Slovenia",
                            "somal": "della Somalia",
                            "spagnol": "della Spagna",
                            "statunitense": "degli Stati Uniti",
                            "sudafrican": "del Sudafrica",
                            "sudanese": "del Sudan",
                            "sudcorean": "della Corea del Sud",
                            "svedese": "della Svezia",
                            "svizzer": "della Svizzera",
                            "tailandese": "della Thailandia",
                            "taiwanese": "di Taiwan",
                            "tanzanian": "della Tanzania",
                            "tedesc": "della Germania",
                            "togolese": "del Togo",
                            "tongan": "di Tonga",
                            "tunisin": "della Tunisia",
                            "turc": "della Turchia",
                            "turkmen": "del Turkmenistan",
                            "ucrain": "dell'Ucraina",
                            "ugandese": "dell'Uganda",
                            "ungherese": "dell'Ungheria",
                            "uruguaian": "dell'Uruguay",
                            "uzbek": "dell'Uzbekistan",
                            "vanuatuan": "di Vanuatu",
                            "vatican": "del Vaticano",
                            "venezuelan": "del Venezuela",
                            "vietnamit": "del Vietnam",
                            "yemenit": "dello Yemen",
                            "zambese": "dello Zambia",
                            "zimbabwese": "dello Zimbawe"
                        }

    # Function to find the matching country name
    def find_country_name(nationality):
        for root, country in country_mapping.items():
            if nationality["male"].startswith(root):
                return country
        return "Unknown"

    # Add country_name to each nationality
    return [
        {**nationality, "place_name": find_country_name(nationality)}
        for nationality in nationalities
    ]


def get_capital(proper_name):

    components = proper_name.split()

    name = ""
    for component in components:
        name += component[0] + "."

    return name


capital_proper_names = [get_capital(proper_name) for proper_name in proper_names['male']+proper_names['female']]


def is_object(span):
    for el in objects:
        if el['singular'] == span or ('plural' in el and el['plural'] == span):
            return True
    return False


def search_object(span):
    for el in objects:

        if el['singular'] == span or ('plural' in el and el['plural'] == span):
            return el
    return {}


def is_province(span):
    last_part = span.split()[-1]
    if last_part in provinces:
        return True


def is_provincial(span):
    for el in provincial_origin:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural']:
            return True
    return {}


def search_provincial_origin(span):

    for el in provincial_origin:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural']:
            return el

    return {}


def is_regional(span):

    for el in regional_origin:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural']:
            return True
        else:
            span = span.split()[-1]
            if el['place_name'].endswith(span):
                return True
    return {}


def search_regional_origin(span):

    for el in regional_origin:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural']:
            return el

        else:
            span = span.split()[-1]
            if el['place_name'].endswith(span):
                return el

    return {}


def is_nation(span):
    last_part = span.split()[-1]

    for nation in nations:
        if nation.endswith(last_part):
            return True

    return False


def is_national(span):

    if span.startswith('originari'):
        span = span.split()[-1]

    for el in nationalities:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural'] or el['place_name'].endswith(span):
            return True
    return {}


def search_national_origin(span):

    if span.startswith('originari'):
        span = span.split()[-1]

    for el in nationalities:
        if span == el['male'] or span == el['female']:
            return el

        if span == el['male_plural'] or span == el['female_plural'] or el['place_name'].endswith(span):
            return el

    return {}


def correct_singular_age(text, span):

    new_span = ""

    if span.endswith("enne"):

        print(f"{span[:-4]}e")

        if span[:-4].isnumeric():
            if span[:-4] + " anni":
                new_span = span[:-4] + " anni"


        elif f"{span[:-4]}e" in numeric_word_to_numbers:
            correction = numeric_word_to_numbers[f"{span[:-4]}e"] + "enne"
            new_span = numeric_word_to_numbers[f"{span[:-4]}e"] + "enne"


        elif f"{span[:-4]}i" in numeric_word_to_numbers:
            new_span = numeric_word_to_numbers[f"{span[:-4]}i"] + "enne"


    elif span.endswith("t anni"):
        new_span = span[:-6]

    elif span.endswith("nta anni"):
        new_span = span[:-8] + "nt'anni"

    elif span.endswith(" anni") and span[:-5].isnumeric():
        print(span)
        if span[:-5] in numbers_to_numeric_word:
            if numbers_to_numeric_word[span[:-5]] + " anni" in text:
                new_span = numbers_to_numeric_word[span[:-5]] + " anni"

            elif numbers_to_numeric_word[span[:-5]][:-1] + "enne" in text:
                new_span = numbers_to_numeric_word[span[:-5]][:-1] + "enne"

            elif f"{span[:-5]}enne" in text:
                new_span = f"{span[:-5]}enne"

        elif span[:-5] + "enne":
            new_span = span[:-5] + "enne"

        elif span[:-5].isnumeric() in text:
            new_span = span[:-5].isnumeric()

    elif span.endswith(" anni") and span[:-5] in numeric_word_to_numbers:
        if numeric_word_to_numbers[span[:-5]] + " anni" in text:
            new_span = numeric_word_to_numbers[span[:-5]] + " anni"

    if new_span == "":
        return span

    return new_span


def correct_plural_age(text, span):

    new_span = ""

    if span.endswith("enni"):
        new_span = span[:-4] + " anni"

    elif span.endswith("t anni"):
        new_span = span[:-6]

    elif span.endswith("nta anni"):
        new_span = span[:-8] + "nt'anni"

    elif span.endswith(" anni") and span[:-5].isnumeric() and span[:-5] in numbers_to_numeric_word:

        if span[:-5] in numbers_to_numeric_word:
            if numbers_to_numeric_word[span[:-5]] + " anni" in text:
                new_span = numbers_to_numeric_word[span[:-5]] + " anni"

            elif numbers_to_numeric_word[span[:-5]][:-1] + "enni":
                new_span = numbers_to_numeric_word[span[:-5]][:-1] + "enni"

        elif span[:-5] + "enne":
            new_span = span[:-5] + "enne"

    elif span.endswith(" anni") and span[:-5] in numeric_word_to_numbers:
        if numeric_word_to_numbers[span[:-5]] + " anni" in text:
            new_span = numeric_word_to_numbers[span[:-5]] + " anni"

    if new_span == "":
        return span

    return new_span


def correct_singular_origin(text, span):

    new_span = ""

    if is_province(span):
        last_part = span.split()[-1]

        if f"originaria di {last_part}" in text:
            new_span = f"originaria di {last_part}"

        elif f"originaria della provincia di {last_part}" in text:
            new_span = f"originaria della provincia di {last_part}"

        if f"originario di {last_part}" in text:
            new_span = f"originario di {last_part}"

        elif f"originario della provincia di {last_part}" in text:
            new_span = f"originario della provincia di {last_part}"

    elif is_provincial(span):
        origin = search_provincial_origin(span)
        if origin['male'] == span and origin['female'] in text:
            new_span = origin['female']

        elif origin['female'] == span and origin['male'] in text:
            new_span = origin['male']

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"originario di {origin['place_name']}" in text:
            new_span = f"originario di {origin['place_name']}"

        elif f"originaria di {origin['place_name']}" in text:
            new_span = f"originaria di {origin['place_name']}"

        elif f"originario della provincia di {origin['place_name']}" in text:
            new_span = f"originario della provincia di {origin['place_name']}"

        elif f"originaria della provincia di {origin['place_name']}" in text:
            new_span = f"originaria della provincia di  {origin['place_name']}"

    elif is_regional(span):
        origin = search_regional_origin(span)

        if origin['male'] == span and origin['female'] in text:
            new_span = origin['female']

        elif origin['female'] == span and origin['male'] in text:
            new_span = origin['male']

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origini {origin['female_plural']}"

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"originario {origin['place_name']}" in text:
            new_span = f"originario {origin['place_name']}"

        elif f"originaria {origin['place_name']}" in text:
            new_span = f"originaria {origin['place_name']}"

        elif f"originario di {clean_italian_span(origin['place_name'])}" in text:
            new_span = f"originario di {clean_italian_span(origin['place_name'])}"

        elif f"originario di {clean_italian_span(origin['place_name'])}" in text:
            new_span = f"originario di {clean_italian_span(origin['place_name'])}"


    elif is_nation(span):
        if span.startswith(f"originaria") and f"originario {span[:10]}" in text:
            new_span = f"originario {span[:10]}"

        elif span.startswith(f"originario") and f"originaria {span[:10]}" in text:
            new_span = f"originaria {span[:10]}"

    elif is_national(span):
        origin = search_national_origin(span)

        if f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di nazionalità {origin['female']}" in text:
            new_span = f"di nazionalità {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"originaria {origin['place_name']}" in text:
            new_span = f"originaria {origin['place_name']}"

        elif f"originario {origin['place_name']}" in text:
            new_span = f"originario {origin['place_name']}"


    elif span.startswith("residente nel "):
        if span[:14] + span[14].upper() + span[15:] in text:
            new_span = span[:14] + span[14].upper() + span[15:]

        elif "originario del " + span.split()[-1] in text:
            new_span = "originario del " + span.split()[-1]

        elif "originari del " + span.split()[-1] in text:
            new_span = "originaria del " + span.split()[-1]

    if new_span == "":
        return span

    return new_span


def correct_plural_origin(text, span):

    new_span = ""

    if is_province(span):
        last_part = span.split()[-1]

        if f"originarie di {last_part}" in text:
            new_span = f"originarie di {last_part}"

        elif f"originari di {last_part}" in text:
            new_span = f"originari di {last_part}"

        elif f"originari della provincia di {last_part}" in text:
            new_span = f"originari della provincia di {last_part}"

    elif is_provincial(span):
        origin = search_provincial_origin(span)
        if origin['male_plural'] == span and origin['female_plural'] in text:
            new_span = origin['female_plural']

        elif origin['female_plural'] == span and origin['male_plural'] in text:
            new_span = origin['male_plural']

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"originarie di {origin['place_name']}" in text:
            new_span = f"originarie di {origin['place_name']}"

    elif is_regional(span):
        origin = search_regional_origin(span)

        if origin['male_plural'] == span and origin['female_plural'] in text:
            new_span = origin['female_plural']

        elif origin['female_plural'] == span and origin['male_plural'] in text:
            new_span = origin['male_plural']

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"originari {origin['place_name']}" in text:
            new_span = f"originari {origin['place_name']}"

        elif f"originario {origin['place_name']}" in text:
            new_span = f"originario {origin['place_name']}"

        elif f"originarie {origin['place_name']}" in text:
            new_span = f"originarie {origin['place_name']}"

        elif f"originari della regione {origin['female']}" in text:
            new_span = f"originari della regione {origin['female']}"

        elif f"originari di {clean_italian_span(origin['place_name'])}" in text:
            new_span = f"originari di {clean_italian_span(origin['place_name'])}"

        elif f"originarie di {clean_italian_span(origin['place_name'])}" in text:
            new_span = f"originarie di {clean_italian_span(origin['place_name'])}"

        elif f"originario di {clean_italian_span(origin['place_name'])}" in text:
            new_span = f"originario di {clean_italian_span(origin['place_name'])}"



    elif is_national(span):
        origin = search_national_origin(span)
        if origin['male_plural'] == span and origin['female_plural'] in text:
            new_span = origin['female_plural']

        elif origin['female_plural'] == span and origin['male_plural'] in text:
            new_span = origin['male_plural']

        elif origin['female_plural'] == span and origin['male'] in text:
            new_span = origin['male']

        elif f"di origine {origin['female']}" in text:
            new_span = f"di origine {origin['female']}"

        elif f"di nazionalità {origin['female']}" in text:
            new_span = f"di nazionalità {origin['female']}"

        elif f"di origini {origin['female_plural']}" in text:
            new_span = f"di origine {origin['female_plural']}"

        elif f"originari {origin['place_name']}" in text:
            new_span = f"originari {origin['place_name']}"

        elif f"originarie {origin['place_name']}" in text:
            new_span = f"originarie {origin['place_name']}"

        elif f"originario {origin['place_name']}" in text:
            new_span = f"originario {origin['place_name']}"


    elif span.startswith("residenti nel "):
        if span[:14] + span[14].upper() + span[15:] in text:
            new_span = span[:14] + span[14].upper() + span[15:]

        elif "originari del " + span.split()[-1] in text:
            new_span = "originari del " + span.split()[-1]

        elif "originarie del " + span.split()[-1] in text:
            new_span = "originarie del " + span.split()[-1]

        elif "originario del " + span.split()[-1] in text:
            new_span = "originario del " + span.split()[-1]

    elif span.startswith("residenti"):
        if f"{span[:8]}e{span[9:]}":
            new_span = span[:8] + "e" + span[9:]

    elif span.startswith("originari "):

        if f"{span[:9]}o{span[9:]}" in text:
            new_span = f"{span[:9]}o{span[9:]}"
        elif f"{span[:9]}e{span[9:]}" in text:
            new_span = f"{span[:9]}e{span[9:]}"

    elif span.startswith("originarie"):
        if f"{span}o{span[9:]}" in text:
            new_span = f"{span[:9]}o{span[9:]}"
        elif f"{span[:9]}{span[10:]}" in text:
            new_span = f"{span[:9]}{span[10:]}"

    if new_span == "":
        return span

    return new_span


def check_number_in_annotation(to_check, span_list=[]):

    if to_check.lower() in span_list:
        return True

    if to_check.capitalize() not in span_list:
        return True

    return False


def correct_annotation(annotation, text):

    to_delete = {
                    'OBJ': [[] for el in annotation['OBJ']],
                    'AUT': [[] for el in annotation['AUT']],
                    'AUTG': [],
                    'VIC': [[] for el in annotation['VIC']],
                    'VICG': [],
                    'PAR': [],
                    'LOC': []
    }

    for k, v in annotation.items():

        for i, el in enumerate(v):
            if isinstance(el, list):
                for j, s in enumerate(el):
                    if s not in text:

                        annotation[k][i][j] = annotation[k][i][j].strip()

                        for accent, correction in accents.items():
                            annotation[k][i][j] = annotation[k][i][j].replace(accent, correction)

                        if "dell' " in s:
                            annotation[k][i][j] = annotation[k][i][j].replace("dell' ", "dell'")

                        if k == 'AUT':
                            annotation[k][i][j] = correct_singular_origin(text, annotation[k][i][j])
                            annotation[k][i][j] = correct_singular_age(text, annotation[k][i][j])

                            if annotation[k][i][j] in proper_names['male']+proper_names['female'] or annotation[k][i][j] in capital_proper_names:
                                to_delete[k][i] = [j] + to_delete[k][i]


                            if annotation[k][i][j] == 'donna' or annotation[k][i][j] == 'uomo':
                                if annotation[k][i][j] not in flatten_nested_list(annotation['VIC']):
                                    to_delete[k][i] = [j] + to_delete[k][i]

                        if k == 'VIC':
                            annotation[k][i][j] = correct_singular_origin(text, annotation[k][i][j])
                            annotation[k][i][j] = correct_singular_age(text, annotation[k][i][j])

                            if annotation[k][i][j] in proper_names['male']+proper_names['female'] or annotation[k][i][j] in capital_proper_names:
                                to_delete[k][i] = [j] + to_delete[k][i]

                            if annotation[k][i][j] == 'donna' or annotation[k][i][j] == 'uomo':
                                if annotation[k][i][j] not in flatten_nested_list(annotation['AUT']):
                                    to_delete[k][i] = [j] + to_delete[k][i]

                        elif k == 'OBJ':
                            if is_object(annotation[k][i][j]):

                                stolen_object = search_object(annotation[k][i][j])

                                if 'plural' in stolen_object and annotation[k][i][j] == stolen_object['singular'] and stolen_object['plural'] in text:
                                    annotation[k][i][j] = stolen_object['plural']

                                elif 'plural' in stolen_object and annotation[k][i][j] == stolen_object['plural'] and stolen_object['singular'] in text:
                                    annotation[k][i][j] = stolen_object['singular']

                                elif annotation[k][i][j] == 'telefonino' or annotation[k][i][j] == 'telefonini':

                                    if 'telefono cellulare' in text:
                                        annotation[k][i][j] = 'telefono cellulare'

                                    elif 'telefoni cellulari' in text:
                                        annotation[k][i][j] = 'telefoni cellulari'

                                elif annotation[k][i][j] == 'chiavetta usb' or annotation[k][i][j] == 'chiavette usb':

                                    if 'chiavetta USB' in text:
                                        annotation[k][i][j] = 'chiavetta USB'

                                    elif 'chiavette USB' in text:
                                        annotation[k][i][j] = 'chiavette USB'

                                elif annotation[k][i][j] == 'IPhone':

                                    if 'iPhone' in text:
                                        annotation[k][i][j] = 'iPhone'

                                elif annotation[k][i][j] == 'airpods':

                                    if 'AirPods' in text:
                                        annotation[k][i][j] = 'AirPods'

                                elif annotation[k][i][j] == 'moca':

                                    if 'moka' in text:
                                        annotation[k][i][j] = 'moka'

                                elif annotation[k][i][j] == 'effetti personali':

                                    if 'oggetti personali' in text:
                                        annotation[k][i][j] = 'oggetti personali'

                                elif annotation[k][i][j] == 'borsetta' or annotation[k][i][j] == 'borsette':

                                    if 'borsa' in text:
                                        annotation[k][i][j] = 'borsa'

                                    elif 'borse' in text:
                                        annotation[k][i][j] = 'borse'

                                    else:
                                        to_delete[k][i] = [j] + to_delete[k][i]

                            elif annotation[k][i][j] in list(numbers_to_numeric_word.values()):
                                to_compare = annotation['AUTG'] + annotation['VICG']

                                if (annotation[k][i][j].capitalize() in text) and (not check_number_in_annotation(annotation[k][i][j].capitalize(), to_compare)):

                                    annotation[k][i][j] = annotation[k][i][j].capitalize()

                                elif (numeric_word_to_numbers[annotation[k][i][j]] in text) and (not check_number_in_annotation(numeric_word_to_numbers[annotation[k][i][j]], to_compare)):

                                    annotation[k][i][j] = numeric_word_to_numbers[annotation[k][i][j]]

                                elif annotation[k][i][j] not in to_compare:
                                    to_delete[k][i] = [j] + to_delete[k][i]

            else:

                annotation[k][i] = annotation[k][i].strip()
                if el not in text:
                    for accent, correction in accents.items():
                        annotation[k][i] = annotation[k][i].replace(accent, correction)

                    if "dell' " in el:
                        annotation[k][i] = annotation[k][i].replace("dell' ", "dell'")

                    if k == 'VICG':
                        annotation[k][i] = correct_plural_age(text, annotation[k][i])
                        annotation[k][i] = correct_plural_origin(text, annotation[k][i])

                        if annotation[k][i] == 'coniugi':
                            if 'coppia' in text:
                                annotation[k][i] = 'coppia'

                            elif 'coniuge' in text:
                                to_delete[k] = [i] + to_delete[k]


                        elif annotation[k][i] in list(numbers_to_numeric_word.values()):
                            to_compare = annotation['AUTG'] + flatten_nested_list(annotation['OBJ'])

                            if annotation[k][i].capitalize() in text and not check_number_in_annotation(annotation[k][i].capitalize(), to_compare):
                                annotation[k][i] = annotation[k][i].capitalize()

                            elif numeric_word_to_numbers[annotation[k][i]] in text and not check_number_in_annotation(numeric_word_to_numbers[annotation[k][i]], to_compare):
                                annotation[k][i] = numeric_word_to_numbers[annotation[k][i]]

                            elif annotation[k][i] not in to_compare:
                                to_delete[k] = [i] + to_delete[k]
                        else:
                            pass

                    if k == 'AUTG':

                        annotation[k][i] = correct_plural_age(text, annotation[k][i])
                        annotation[k][i] = correct_plural_origin(text, annotation[k][i])

                        if annotation[k][i] == 'coniugi':
                            if 'coppia' in text:
                                annotation[k][i] = 'coppia'

                            elif 'coniuge' in text:
                                to_delete[k] = [i] + to_delete[k]

                        elif annotation[k][i] in list(numbers_to_numeric_word.values()):
                            to_compare = annotation['VICG'] + flatten_nested_list(annotation['OBJ'])

                            if annotation[k][i].capitalize() in text and not check_number_in_annotation(annotation[k][i].capitalize(), to_compare):
                                annotation[k][i] = annotation[k][i].capitalize()

                            elif numeric_word_to_numbers[annotation[k][i]] in text and not check_number_in_annotation(numeric_word_to_numbers[annotation[k][i]], to_compare):
                                annotation[k][i] = numeric_word_to_numbers[annotation[k][i]]

                            elif annotation[k] not in to_compare:
                                to_delete[k] = [i] + to_delete[k]
                        else:
                            pass

                    if k == 'PAR':

                        if annotation[k][i].endswith(" Modena"):
                            to_correct = annotation[k][i][:-7]

                            for j, el in enumerate(annotation['LOC']):
                                if el == annotation[k][i]:
                                    annotation['LOC'][j] = to_correct

                            annotation[k][i] = to_correct

                        elif annotation[k][i] == 'MD':
                            to_delete[k] = [i] + to_delete[k]
                        else:
                            res = annotation[k][i][0].lower() + annotation[k][i][1:]

                            if annotation[k][i].title() in text:
                                annotation[k][i] = annotation[k][i].title()

                            elif res in text:
                                annotation[k][i] = res

                            elif annotation[k][i].capitalize() in text:
                                annotation[k][i] = annotation[k][i].capitalize()

                            else:
                                pass
                                # print(annotation[k][i], text)

                    if k == 'LOC':
                        if annotation[k][i].startswith("Via Cà"):
                            annotation[k][i] = "via Cà " + annotation[k][i][8:]

                        elif annotation[k][i].startswith("Località"):
                            annotation[k][i] = "località " + annotation[k][i][10:]

                        elif "D'" in annotation[k][i]:
                            annotation[k][i] = annotation[k][i].replace("D'", "d'")

                        elif annotation[k][i] in municipalities+provinces:
                            to_delete[k] = [i] + to_delete[k]
                        else:

                            res = annotation[k][i][0].lower() + annotation[k][i][1:]

                            if annotation[k][i].title() in text:
                                annotation[k][i] = annotation[k][i].title()
                            elif res in text:
                                annotation[k][i] = res

                            elif annotation[k][i].capitalize() in text:
                                annotation[k][i] = annotation[k][i].capitalize()
                            else:
                                pass
                                # print(annotation[k][i], text)

    for k, v in to_delete.items():
        if k in ('LOC', 'AUTG', 'VICG', 'PAR') and len(to_delete[k]) > 0:
            annotation[k] = [s for i, s in enumerate(annotation[k]) if i not in to_delete[k]]

        else:
            for i, index_list in enumerate(to_delete[k]):
                if len(index_list) > 0:
                    annotation[k][i] = [s for j, s in enumerate(annotation[k][i]) if j not in to_delete[k][i]]

            while [] in annotation[k]:
                annotation[k].remove([])

    return annotation


def extract_text(data):
    for el in data:
        index = el['completion'].rfind('<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n')
        start_index = index + len('<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n')
        end_index = len(el['completion']) - len('<|eot_id|>')
        el['text'] = el['text'][start_index:end_index]

        # correct accent formatting
        for accent, correction in accents.items():
            el['text'] = el['text'].replace(accent, correction)

    return data


def check_validity(annotation, text):
    is_in = True


    missing_count = {'OBJ': 0, 'AUT': 0, 'AUTG': 0, 'VIC': 0, 'VICG': 0, 'PAR': 0, 'LOC': 0}

    total_count = {'OBJ': 0, 'AUT': 0, 'AUTG': 0, 'VIC': 0, 'VICG': 0, 'PAR': 0, 'LOC': 0}

    for k, v in annotation.items():

        for el in v:
            if isinstance(el, list):
                for s in el:
                    total_count[k] += 1

                    is_in = is_in and s in text

                    if s not in text:
                        missing_count[k] += 1

            else:
                total_count[k] += 1
                is_in = is_in and el in text

                if el not in text:
                    missing_count[k] += 1

    return missing_count, total_count



if __name__ == "__main__":

    nationalities = add_country_names(nationalities)
    
    with open("generated_dataset.json", encoding='utf-8') as f:
        data = json.load(f)

    missing_counts = []
    total_counts = []

    sums_missing = {'OBJ': 0, 'AUT': 0, 'AUTG': 0, 'VIC': 0, 'VICG': 0, 'PAR': 0, 'LOC': 0}
    sums_counts = {'OBJ': 0, 'AUT': 0, 'AUTG': 0, 'VIC': 0, 'VICG': 0, 'PAR': 0, 'LOC': 0}

    valid = []
    not_valid = []

    for i, el in enumerate(data):

        print(i)

        missing_count, total_count = check_validity(data[i]['annotation'], data[i]['text'])
        sum_of_values = sum(list(missing_count.values()))

        if sum_of_values > 0:
            annotation = correct_annotation(data[i]['annotation'], data[i]['text'])

            print('CORRECTED')
            # print(data[i]['annotation'], annotation)
            data[i]['annotation'] = annotation

            missing_count, total_count = check_validity(data[i]['annotation'], data[i]['text'])


        missing_counts.append(missing_count)
        total_counts.append(total_count)

        for k, v in missing_count.items():
            sums_missing[k] += v

        for k, v in total_count.items():
            sums_counts[k] += v


        sum_of_values = sum(list(missing_count.values()))

        print(sum_of_values)

        if sum_of_values > 0:
            not_valid.append({'text': el['text'], 'annotation': el['annotation']})
        else:
            valid.append({'text': el['text'], 'annotation': el['annotation']})
