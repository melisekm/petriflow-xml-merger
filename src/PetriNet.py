import re

import xmltodict

MATCH_PATTERN = re.compile(r"\b([tpa][0-9]+)\b")

SPLIT_PATTERN = re.compile("([a-zA-Z]+)([0-9]+)")

_min = float('inf')
_max = float('-inf')
ALLOWED_ELEMENT_KEYS = ('id', 'destinationId', 'sourceId', 'reference')


class PetriNet:
    def __init__(self, xml=None, increment_x=0, increment_y=0):
        self.bounding_box = {'x_min': _min, 'x_max': _max, 'y_min': _min, 'y_max': _max}
        self.elements = {'t': set(), 'p': set(), 'a': set()}
        self.max_ids = {'t': _max, 'p': _max, 'a': _max}
        self.increment_dict = {
            'x': increment_x,
            'y': increment_y
        }
        self.net_raw_xml = xml
        self.model_dict = xmltodict.parse(self.net_raw_xml)

    def parse(self, rename=False, max_ids=None):
        if rename and not max_ids:
            raise ValueError("max_ids must be specified if rename is True")

        self.parse_keys(self.model_dict, rename, max_ids)
        self.net_raw_xml = xmltodict.unparse(self.model_dict, pretty=True)

        # increment ids so they are ready to be written to next net
        self.max_ids['t'] += 1
        self.max_ids['a'] += 1
        self.max_ids['p'] += 1

    def parse_keys(self, model_dict, rename, max_ids):
        for key, value in list(model_dict.items()):
            if key in ('x', 'y'):
                value = int(value)
                model_dict[key] = value + self.increment_dict[key]
                self.bounding_box[key + '_min'] = min(self.bounding_box[key + '_min'], model_dict[key])
                self.bounding_box[key + '_max'] = max(self.bounding_box[key + '_max'], model_dict[key])
            elif key in ALLOWED_ELEMENT_KEYS and MATCH_PATTERN.match(value):
                match = SPLIT_PATTERN.match(value)
                name = match.group(1)
                idx = int(match.group(2))
                if rename:
                    new_value = max_ids[name] + idx
                    model_dict[key] = name + str(new_value)
                else:
                    self.max_ids[name] = max(self.max_ids[name], idx)
                    self.elements[name].add(idx)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.parse_keys(item, rename, max_ids)
            elif isinstance(value, dict):
                self.parse_keys(value, rename, max_ids)
