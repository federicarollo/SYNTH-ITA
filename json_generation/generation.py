import ast
import json
import copy


from random import randint
from datetime import datetime, timedelta

from utils import preserve_tuples, restore_tuples, select_elements_from_collections, clean_italian_span


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

numbers_to_numeric_word = {
                                '1': 'uno',
                                '2': 'due',
                                '3': 'tre',
                                '4': 'quattro',
                                '5': 'cinque',
                                '6': 'sei',
                                '7': 'sette',
                                '8': 'otto',
                                '9': 'nove',
                                '10': 'dieci',
                                '11': 'undici',
                                '12': 'dodici',
                                '13': 'tredici',
                                '14': 'quattordici',
                                '15': 'quindici',
                                '16': 'sedici',
                                '17': 'diciassette',
                                '18': 'diciotto',
                                '19': 'diciannove',
                                '20': 'venti',
                                '25': 'venticinque',
                                '30': 'trenta',
                                '35': 'trentacinque',
                                '40': 'quaranta',
                                '45': 'quarantacinque',
                                '50': 'cinquanta',
                                '55': 'cinquantacinque',
                                '60': 'sessanta',
                                '65': 'sessantacinque',
                                '70': 'settanta',
                                '75': 'settantacinque',
                                '80': 'ottanta',
                                '85': 'ottantacinque',
                                '90': 'novanta',
                                '100': 'cento',
                                '200': 'duecento',
                                '300': 'trecento',
                                '400': 'quattrocento',
                                '500': 'cinquecento',
                                '600': 'seicento',
                                '700': 'settecento',
                                '800': 'ottocento',
                                '900': 'novecento',
                                '1000': 'mille',
                                '2000': 'duemila',
                                '3000': 'tremila',
                                '4000': 'quattromila',
                                '5000': 'cinquemila',
                                '6000': 'seimila',
                                '7000': 'settemila',
                                '8000': 'ottomila',
                                '9000': 'novemila'
}

numeric_word_to_numbers = {v: k for k, v in numbers_to_numeric_word.items()}


gender_terms = {
                    "male": {
                                "singular": {
                                                "adult": ("uomo", "l'", "un"),
                                                "young1": ("ragazzo", "il", "un"),
                                                "young2": ("giovane", "il", "un"),
                                                "old": ("anziano", "l'", "un"),
                                                "son": ("figlio", "il", "un"),
                                                "parent": ("padre", "il", "un"),
                                                "thief1": ("ladro", "il", "un"),
                                                "thief2": ("malvivente", "il", "un"),
                                                "origin": "originario"
                                },
                                "plural": {
                                            "adult": ("uomini", "gli", "degli"),
                                            "young1": ("ragazzi", "i", "dei"),
                                            "young2": ("giovani", "i", "dei"),
                                            "old": ("anziani", "gli", "degli"),
                                            "son": ("figli", "i", "dei"),
                                            "parent": ("padri", "i", "dei"),
                                            "thief1": ("ladri", "i", "dei"),
                                            "thief2": ("malviventi", "i", "dei"),
                                            "origin": "originari"
                                }
                    },
                    "female": {
                                "singular": {
                                                "adult": ("donna", "la", "una"),
                                                "young1": ("ragazza", "la", "una"),
                                                "young2": ("giovane", "la", "una"),
                                                "old": ("anziana", "l'", "un'"),
                                                "son": ("figlia", "la", "una"),
                                                "parent": ("madre", "la", "una"),
                                                "thief1": ("ladra", "la", "una"),
                                                "thief2": ("malvivente", "la", "una"),
                                                "origin": "originaria"

                                },
                                "plural": {
                                            "adult": ("donne", "le", "delle"),
                                            "young1": ("ragazze", "le", "delle"),
                                            "young2": ("giovani", "le", "delle"),
                                            "old": ("anziane", "le", "delle"),
                                            "son": ("figlie", "le", "delle"),
                                            "parent": ("madri", "le", "delle"),
                                            "thief1": ("ladre", "le", "delle"),
                                            "thief2": ("malviventi", "le", "delle"),
                                            "origin": "originarie"
                                }
                    }
    }


vowel = 'aeiou'




def generate_cash_of_the_day():

    voc = ["registratore di cassa", "incasso", "fondo cassa"]
    word_index = randint(0, len(voc) - 1)

    annotation = [[voc[word_index]]]

    is_numbered = randint(0, 20) > 10
    if is_numbered:
        cash_number = randint(1, 30) * 100

        if randint(0, 20) > 10 and str(cash_number) in numbers_to_numeric_word:
            if annotation == [["registratore di cassa"]]:
                annotation.append([numbers_to_numeric_word[str(cash_number)] + ' euro'])
            else:
                annotation = [[numbers_to_numeric_word[str(cash_number)] + ' euro']]
        else:
            if annotation == [["registratore di cassa"]]:
                annotation.append([str(cash_number) + ' euro'])
            else:
                annotation = [[str(cash_number) + ' euro']]


    return annotation


def select_objects(object_options):
    selected_objects = select_elements_from_collections(object_options)

    object_list = []
    for obj in selected_objects:
        if isinstance(obj, tuple):
            index = randint(0, len(obj) - 1)
            if isinstance(obj[index], list):
                object_list += select_elements_from_collections(obj[index])
            else:
                object_list.append(obj[index])
        else:
            object_list.append(obj)

    final_list = []

    for el in object_list:
        if 'singular' in el and 'plural' in el:
            if el['singular'] == 'incasso':
                cash_annotation = generate_cash_of_the_day()
                final_list += cash_annotation

            else:
                if randint(0, 20) > 10:

                    final_list.append([clean_italian_span(el['singular'])])
                elif randint(0, 20) > 10:

                    final_list.append([el['plural']])
                else:
                    num = randint(2, 5)
                    final_list.append([numbers_to_numeric_word[str(num)], el['plural']])

        else:
            final_list.append([clean_italian_span(el['singular'])])

    return final_list


def select_town():
    town_index = randint(0, len(towns) - 1)
    return towns[town_index]


def select_street_by_town(town='Modena'):
    index = randint(0, len(streets[town]) - 1)
    return streets[town][index]


def select_park_by_town(town='Modena'):
    filtered_parks = [park for park in parks if park['town'] == town]
    index = randint(0, len(filtered_parks) - 1)
    return filtered_parks[index]


def select_company():

    company_info = {}

    index_type = randint(0, len(company_to_objects) - 1)
    company_type = company_to_objects[index_type]['company_type']
    expressions = company_to_objects[index_type]['expressions']
    expression = expressions[randint(0, len(expressions) - 1)]

    with open(f"{datapath}/{company_type}.json") as f:
        companies = json.load(f)


    index = randint(0, len(companies) - 1)

    company_info['LOC'] = []
    company_info['PAR'] = []

    if randint(0, 20) > 10:
        expr_index = randint(0, len(company_to_objects[index_type]['expressions']) - 1)
        company_info['LOC'].append(company_to_objects[index_type]['expressions'][expr_index])
        company_info['PAR'].append(company_to_objects[index_type]['expressions'][expr_index])
    else:
        company_info['LOC'].append(companies[index]['name'])
        company_info['PAR'].append(companies[index]['name'])

    company_info['LOC'].append(companies[index]['town'])

    if randint(0, 20) > 10:
        company_info['LOC'].append(companies[index]['street'])


    return company_info, company_type



def choose_origin_type():
    origin_types = ['provincial', 'regional', 'nationality']

    return origin_types[randint(0, len(origin_types) - 1)]



def get_single_origin(origin_type='provincial', gender='male', adjective=False, plural=False):
    assert origin_type in ('provincial', 'regional', 'nationality')
    assert gender in ('male', 'female')

    if adjective:
        if origin_type == 'provincial':
            options = provincial_origin
        elif origin_type == 'regional':
            options = regional_origin
        else:
            options = nationalities

        field = gender + '_plural' if plural else gender

        return options[randint(0, len(options) - 1)][field]

    else:
        number = 'plural' if plural else 'singular'

        if origin_type == 'provincial':
            origin_string = gender_terms[gender][number]['origin']
            if randint(0, 20) > 10:
                origin_string += ' della provincia di'
            else:
                origin_string += ' di'
            options = provinces
        elif origin_type == 'regional':
            options = regions
            origin_string = gender_terms[gender][number]['origin']
        else:
            options = nations
            origin_string = gender_terms[gender][number]['origin']

        return origin_string + ' ' + options[randint(0, len(options) - 1)]



def get_multiple_origin(total_num, origin_type='provincial'):
    assert origin_type in ('provincial', 'regional', 'nationality')

    origin_count = {}

    if origin_type == 'provincial':
        options = provincial_origin
    elif origin_type == 'regional':
        options = regional_origin
    else:
        options = nationalities

    while sum(origin_count.values()) < total_num:
        num = randint(0, total_num - sum(origin_count.values()))
        if num > 0:
            origin_count[randint(0, len(options) - 1)] = num
    return origin_count



def get_residency(plural=True):

    residency_string = "residenti" if plural else "residente"

    residence_num = randint(0, 20)

    if residence_num < 10:
        adjectives = [origin['male'] for origin in provincial_origin[0:12]]
        residency_string += ' nel ' + adjectives[randint(0, len(adjectives) - 1)]
    else:
        residency_string += ' a ' + municipalities[randint(0, len(municipalities) - 1)]

    return residency_string


def get_age(plural=False, adjective=False, min_age=18, max_age=60):
    assert max_age >= min_age
    age = randint(min_age, max_age)

    if adjective:
        if age < 18 and randint(0, 20) > 10:
            root = 'minorenni' if plural else 'minorenne'
        else:
            if str(age) in numbers_to_numeric_word and randint(0, 20) > 10:
                root = numbers_to_numeric_word[str(age)][:-1]
            else:
                root = str(age)

            if plural:
                root += 'enni'
            else:
                root += 'enne'

    else:
        if str(age) in numbers_to_numeric_word and randint(0, 20) > 10:
            root = numbers_to_numeric_word[str(age)] + ' anni'
        else:
            root = str(age) + ' anni'

        label = 'di ' + root

    return root


def get_mention_sequence(exclude=[]):
    mention_types = ('name', 'gender', 'age', 'origin', 'thief', 'residency')

    for el in exclude:
        assert el in mention_types

    available_mentions = [el for el in mention_types if el not in exclude]

    mentions_list = []
    num = randint(0, len(available_mentions)*10 - 1)

    i = num//10
    mentions_list.append(available_mentions[i])

    for el in ['thief', 'gender']:
        if el in available_mentions:
            available_mentions.remove(el)

    if 'residency' not in exclude:
        available_mentions.append('residency')

    for _ in range(0, 2):
        num = randint(0, (len(available_mentions))*10)
        i = num//10
        if i < len(available_mentions) and available_mentions[i] not in mentions_list:
            mentions_list.append(available_mentions[i])

    if 'name' in available_mentions:
        available_mentions.remove('name')

    num = randint(0, (len(available_mentions))*10)
    i = num//10
    if i < len(available_mentions) and available_mentions[i] not in mentions_list:
        mentions_list.append(available_mentions[i])

    if 'residency' in mentions_list and 'origin' in mentions_list:
        r_index = mentions_list.index('residency')
        o_index = mentions_list.index('origin')

        if r_index < o_index:
            mentions_list[r_index] = 'origin'
            mentions_list[o_index] = 'residency'

    return mentions_list


def get_parent_with_son():
    info = []

    parent_info = []
    mentions_list = get_mention_sequence(exclude=['name', 'thief', 'residency'])
    gender = 'male' if randint(0, 20) > 10  else 'female'
    origin = None
    min_age = 35
    max_age = 50

    for i, mention in enumerate(mentions_list):
        if mention == "name":
            proper_name, origin = get_proper_name(gender=gender, origin=origin)
            parent_info.append(proper_name)

        elif mention == "gender":
            parent_info.append(gender_terms[gender]['singular']['adult'][0])

        elif mention == "age":
            adjective = (i == 0 or randint(0, 20) > 10)
            age = get_age(adjective=adjective, min_age=min_age, max_age=max_age)
            parent_info.append(age)

        else:
            adjective = (i == 0 or randint(0, 20) > 10)

            if origin is not None:
                if origin.startswith('italian'):
                    origin_type = 'regional' if randint(0, 20) > 10 else 'provincial'
                    origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective, plural=False)
            else:
                origin_type = choose_origin_type()
                origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective, plural=False)

            parent_info.append(origin)

    info.append(parent_info)


    ### son info
    son_info = []
    gender = 'male' if randint(0, 20) > 10  else 'female'

    age = get_age(min_age=2, max_age=20)
    son_info.append(age)

    info.append(son_info)

    return info


def get_son_with_parent():
    formulation = ""
    info = []

    ### son info
    son_info = []
    mentions_list = get_mention_sequence(exclude=['thief', 'residency'])
    gender = 'male' if randint(0, 20) > 10  else 'female'
    origin = None
    min_age = 20
    max_age = 50

    for i, mention in enumerate(mentions_list):
        if mention == "gender":
            adult_number = randint(0, 30)
            if adult_number < 10:
                son_info.append(gender_terms[gender]['singular']['adult'][0])
                if 'age' in mentions_list and mentions_list.index('age') > i:
                    min_age = 30
                    max_age = 50
            elif adult_number < 20:
                if 'age' in mentions_list and mentions_list.index('age') > i:
                    min_age = 20
                    max_age = 29
            else:
                son_info.append(gender_terms[gender]['singular']['young2'][0])
                if 'age' in mentions_list and mentions_list.index('age') > i:
                    min_age = 20
                    max_age = 29

        elif mention == "age":
            adjective = (i == 0 or randint(0, 20) > 10)
            age = get_age(adjective=adjective, min_age=min_age, max_age=max_age)

            son_info.append(age)

        else:
            adjective = (i == 0 or randint(0, 20) > 10)

            if origin is not None:
                if origin.startswith('italian'):
                    origin_type = 'regional' if randint(0, 20) > 10 else 'provincial'
                    origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective, plural=False)
            else:
                origin_type = choose_origin_type()
                origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective, plural=False)

            son_info.append(origin)

    info.append(son_info)

    ### parent info
    parent_info = []
    gender = 'male' if randint(0, 20) > 10  else 'female'

    if randint(0, 20) > 10:
        age = get_age(adjective=randint(0, 20) > 10, min_age=40, max_age=65)
        parent_info.append(age)
    else:
        parent_info.append(gender_terms[gender]['singular']['old'][0])

    info.append(parent_info)

    return info



def get_couple(old=False, residency=False, origin=False):
    num = randint(0, 20)
    info = {'group': [], 'single': []}

    formulation = ""

    if num < 10:
        info['group'] += ['due', 'coniugi']

        old_num = randint(0, 40)
        if old_num < 10 and old:

            info['group'].append('anziani')
        elif old_num < 20:
            age_to_get = randint(7, 11)*5
            age= get_age(plural=True, adjective=randint(0, 20)>10, min_age=age_to_get, max_age=age_to_get)

            info['group'].append(age)
        elif old_num < 30:
            first_age = randint(25, 55)
            second_age = randint(25, 55)

            if first_age == second_age:
                second_age += 1

            info['single'].append([str(first_age)])
            info['single'].append([str(second_age) + " anni"])

        gender = 'male'
    else:
        info['group'].append('coppia')

        gender = 'male' if randint(0, 20) > 10  else 'female'

        adult_term = ""
        adult_num = randint(0, 30)
        if adult_num < 10:
            adult_term = 'young1'
            max_n = 6
            min_n = 4
        elif adult_num < 20:
            adult_term = 'adult'
            max_n = 11
            min_n = 5
        else:
            adult_term = 'young2'
            max_n = 6
            min_n = 4

        info['group'].append(gender_terms[gender]['plural'][adult_term][0])

        age_num = randint(0, 30)
        if age_num < 10:
            age_to_get = randint(min_n, max_n)*5
            age = get_age(plural=True, adjective=randint(0, 20)>10, min_age=age_to_get, max_age=age_to_get)

            info['group'].append(str(age))
        elif age_num < 20:
            first_age = randint(min_n*5, max_n*5)
            second_age = randint(min_n*5, max_n*5)

            info['single'].append([str(first_age)])
            info['single'].append([str(second_age) + " anni"])

    if origin:
        origin_type = choose_origin_type()
        origin = origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=randint(0, 20) >10, plural=True)
        info['group'].append(origin)

    if residency:
        residency = get_residency(plural=True)
        info['group'].append(residency)

    return info



def get_proper_name(gender='male', capital=False):

    name_index = randint(0, len(proper_names[gender]) - 1)
    name = proper_names[gender][name_index]

    if capital:
        components = name.split()

        name = ""
        for component in components:
            name += component[0] + "."


    return name



def generate_authors(num_authors=0, max_num=7, all_identified=False):

    if num_authors == 0:
        num_identified_thiefs = randint(0, max_num)
    else:
        num_identified_thiefs = num_authors

    authors = {
                'identified_num': num_identified_thiefs,
                'not_identified_authors': 0,
                'AUT': [],
                'AUTG': []
    }


    if not all_identified and randint(0, 20) > 11:
        authors['not_identified_authors']  = randint(1, 2)

    if num_identified_thiefs > 0:
        if num_identified_thiefs == 1:

            mentions_list = get_mention_sequence()
            gender = 'male' if randint(0, 20) > 10 else 'female'

            author_info = []
            for i, mention in enumerate(mentions_list):
                if mention == "thief":
                    key = 'thief1' if randint(0, 20) > 10 else 'thief2'
                elif mention == "name":
                    proper_name = get_proper_name(gender=gender, capital=randint(0, 20) > 10)
                    author_info.append(proper_name)

                elif mention == "gender":
                    key = 'adult'
                    author_info.append(gender_terms[gender]['singular'][key][0])
                elif mention == "age":
                    age = get_age(plural=False, adjective=randint(0, 20) > 10, min_age=25, max_age=55)
                    author_info.append(age)

                elif mention == "origin":
                    origin = get_single_origin(origin_type=choose_origin_type(), gender=gender, adjective=randint(0, 20) > 10, plural=False)
                    author_info.append(origin)
                else:
                    residency = get_residency(plural=False)
                    author_info.append(residency)

            authors['AUT'].append(author_info)

        elif num_identified_thiefs == 2 and randint(0, 20) > 10:
            couple_info = get_couple(residency=randint(0, 20) > 10, origin=randint(0, 20) > 10)
            authors['AUT'] += couple_info['single']
            authors['AUTG'] += couple_info['group']
        else:
            gender_nums = {}
            gender_nums['male'] = randint(0, num_identified_thiefs)
            gender_nums['female'] = num_identified_thiefs - gender_nums['male']

            to_exclude = ['name']
            if num_identified_thiefs > 3:
                to_exclude.append('age')

            mentions_list = get_mention_sequence(exclude=to_exclude)

            for i, mention in enumerate(mentions_list):
                if mention == "thief":
                    key = 'thief1' if randint(0, 20) > 10 else 'thief2'
                    authors['AUTG'].append(numbers_to_numeric_word[str(num_identified_thiefs)])

                elif mention == "gender":
                    if gender_nums['male'] >= 1 and gender_nums['female'] >= 1:
                        authors['AUTG'].append(numbers_to_numeric_word[str(num_identified_thiefs)])

                    for j, gender in enumerate(['male', 'female']):
                        if gender_nums[gender] == 1:
                            authors['AUT'].append([gender_terms[gender]['singular']['adult'][0]])

                        elif gender_nums[gender] > 1:
                            if gender_nums[gender] == num_identified_thiefs:
                                if 'thief' not in mentions_list:
                                    authors['AUTG'].append(numbers_to_numeric_word[str(num_identified_thiefs)])
                                authors['AUTG'].append(gender_terms[gender]['plural']['adult'][0])

                elif mention == "age":
                    age_num = randint(0, 30)
                    if age_num < 10 and num_identified_thiefs > 2:

                        max_age = randint(6, 11)*5
                        age_range = randint(3, 6) if randint(0, 20) > 10 else 10
                        authors['AUTG'].append("tra i " + str(max_age - age_range) + " e i " + str(max_age) + " anni")
                    else:
                        macro_age = randint(3, 5) * 10
                        age = get_age(plural=True, adjective=True, min_age=macro_age, max_age=macro_age)
                        authors['AUTG'].append(str(age))

                elif mention == "origin":

                    adjective = True if i == 0 else (randint(0, 20) > 10)
                    if i == 0:
                        authors['AUTG'].append(numbers_to_numeric_word[str(num_identified_thiefs)])

                    gender = 'male'
                    if gender_nums['male'] == 0:
                        gender = 'female'

                    origin = get_single_origin(origin_type=choose_origin_type(), gender=gender, adjective=adjective, plural=True)
                    authors['AUTG'].append(origin)

                else:
                    residency = get_residency(plural=True)
                    authors['AUTG'].append(residency)

    return authors



def generate_victims(max_num=4):
    vict_annotation = []
    vict_group_annotation = []

    num_identified_victims = randint(1, max_num)

    victims = {
                'identified_num': num_identified_victims,
                'VIC': [],
                'VICG': []
    }

    if num_identified_victims == 1:
        mentions_list = get_mention_sequence(exclude=['thief', 'residency'])
        gender = 'male' if randint(0, 20) > 10 else 'female'
        origin = None

        vic_info = []
        for i, mention in enumerate(mentions_list):
            if mention == "name":
                proper_name = get_proper_name(gender=gender)
                vic_info.append(proper_name)

            elif mention == "gender":
                key = 'adult'
                vic_info.append(gender_terms[gender]['singular'][key][0])

            elif mention == "age":
                adjective = True if i==0 else randint(0, 20) > 10
                age = get_age(plural=False, adjective=adjective, min_age=25, max_age=55)
                vic_info.append(age)

            elif mention == "origin":
                if i==0:
                    adjective = True
                else:
                    adjective = randint(0, 20) > 10

                if origin is not None:
                    if origin.startswith('italian'):
                        origin_type = 'regional' if randint(0, 20) > 10 else 'provincial'
                        origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective,
                                                   plural=False)
                else:
                    origin_type = choose_origin_type()
                    origin = get_single_origin(origin_type=origin_type, gender=gender, adjective=adjective, plural=False)

                vic_info.append(origin)
            else:
                residency = get_residency(plural=False)
                vic_info.append(residency)

        victims['VIC'].append(vic_info)

    elif num_identified_victims == 2:

        num = randint(0, 30)
        if num < 10:
            ps_info = get_parent_with_son()
            victims['VIC'] += ps_info
        elif num < 20:
            sp_info = get_son_with_parent()
            victims['VIC'] += sp_info
        else:
            couple_info= get_couple()

            victims['VIC'] += couple_info['single']
            victims['VICG'] += couple_info['group']

    else:
        pass

    return victims



def generate_annotation():

    is_person = randint(0, 20) > 10

    words_num = randint(1, 30) * 50

    information = {}
    if not is_person:
        # theft against an injured party

        company_info, company_type = select_company()
        information.update(company_info)

        index_type = 0
        for i, el in enumerate(company_to_objects):
            if el['company_type'] == company_type:
                index_type = i
                break

        selected_objects = select_objects(company_to_objects[index_type]['objects'])
        information['OBJ'] = selected_objects

        authors = generate_authors(max_num=7)

        information['AUT'] = authors['AUT']
        information['AUTG'] = authors['AUTG']

        information['VIC'] = []
        information['VICG'] = []

    else:
        # theft against physic victims
        dynamics_index = randint(0, len(dynamics) - 1)
        victims = generate_victims(max_num = dynamics[dynamics_index]['num_max'])

        information['VIC'] = victims['VIC']
        information['VICG'] = victims['VICG']

        selected_objects = select_objects(dynamics[dynamics_index]['stolen_objects'])
        information['OBJ'] = selected_objects

        authors = generate_authors(max_num=3)
        information['AUT'] = authors['AUT']
        information['AUTG'] = authors['AUTG']

        town = select_town()

        information['LOC'] = []
        information['LOC'] = [town]

        if dynamics[dynamics_index]['num_max'] == ['parco']:
            # theft in a park
            if randint(0, 20) > 10:
                information['LOC'].append('parco')
            else:
                park = select_park_by_town(town=town)
                information['LOC'].append(park['name'])
        else:
            street = select_street_by_town(town=town)
            information['LOC'].append(street)

            if len(dynamics[dynamics_index]['formulations']) > 0:
                formulation_index = randint(0, len(dynamics[dynamics_index]['formulations']) - 1)
                information['LOC'].append(dynamics[dynamics_index]['formulations'][formulation_index])


        information['PAR'] = []


    return information


if __name__ == "__main__":
    for i in range(3):
        print(generate_annotation())
