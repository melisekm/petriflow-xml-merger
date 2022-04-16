import re

import xmltodict

# x 10k
# y 5k max
MATCH_PATTERN = re.compile(r"\b([tpa][0-9]+)\b")
# TRANSITION_PATTERN = re.compile(r"\b(t[0-9]+)\b")
# PLACE_PATTERN = re.compile(r"\b(p[0-9]+)\b")
# ARC_PATTERN = re.compile(r"\b(a[0-9]+)\b")

SPLIT_PATTERN = re.compile("([a-zA-Z]+)([0-9]+)")

_min = float('inf')
_max = float('-inf')
ALLOWED_KEYS = ('id', 'destinationId', 'sourceId')


def parse_xml(xml_file, increment_x, increment_y):
    with open(xml_file, 'r', encoding='utf-8') as xml:
        model_dict = xmltodict.parse(xml.read())

    bounding_box = {
        'x_min': _min,
        'x_max': _max,
        'y_min': _min,
        'y_max': _max,
    }

    elements = {
        't': set(),
        'p': set(),
        'a': set(),
    }

    max_ids = {
        't': _max,
        'p': _max,
        'a': _max,
    }

    def get_all_keys(d):
        for key, value in list(d.items()):
            # yield key
            if key in ('x', 'y'):
                value = int(value)
            if key == "x":
                d[key] = value + increment_x
            elif key == "y":
                d[key] = value + increment_y
            if key in ("x", "y"):
                bounding_box[key + '_min'] = min(bounding_box[key + '_min'], d[key])
                bounding_box[key + '_max'] = max(bounding_box[key + '_max'], d[key])
            elif key in ALLOWED_KEYS and MATCH_PATTERN.match(value):
                match = SPLIT_PATTERN.match(value)
                name = match.group(1)
                idx = int(match.group(2))
                max_ids[name] = max(max_ids[name], idx)
                elements[name].add(idx)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        get_all_keys(item)
            elif isinstance(value, dict):
                get_all_keys(value)

    get_all_keys(model_dict)

    return bounding_box, model_dict, elements, max_ids




bbox, bp12res, _, max_ids = parse_xml('TEST.xml', 0, 0)
bp12 = xmltodict.unparse(bp12res, pretty=True)

# print(elements)
# for transition in elements['t']:
#     # split string and digit in transition name
#     match = SPLIT_PATTERN.match(transition)
#     idx = int(match.group(2))
#     max_ids['t'] = max(max_ids['t'], idx)
# print(max_ids['t'])
max_ids['t'] += 1
max_ids['a'] += 1
max_ids['p'] += 1

bbox, bp3res, elements, _ = parse_xml('Proces_5.xml', bbox['x_max'], 0)
bp3 = xmltodict.unparse(bp3res, pretty=True)

for element_type, values in elements.items():
    # split string and digit in transition name
    for value in values:
        # match = SPLIT_PATTERN.match(value)
        # name = match.group(1)
        # idx = int(match.group(2))
        new_value = max_ids[element_type] + value
        # max_ids['t'] = max(max_ids['t'], idx)
        bp3 = re.sub(rf"\b{element_type}{value}\b", f"{element_type}{new_value}", bp3)
        print(value, new_value)
# print(max_ids['t'])
# max_ids['t'] += 1
# print(bp3)

edited_bp3 = bp3
edited_bp3_dict = xmltodict.parse(edited_bp3)
edited_t = edited_bp3_dict['document']['transition']
edited_p = edited_bp3_dict['document']['place']
edited_a = edited_bp3_dict['document']['arc']
bp12res['document']['transition'] += edited_t
bp12res['document']['place'] += edited_p
bp12res['document']['arc'] += edited_a

with open('TEST.xml', 'w', encoding='utf-8') as f:
    f.write(xmltodict.unparse(bp12res, pretty=True))
