import xmltodict

from PetriNet import PetriNet


def merge_elements(old_net, new_net):
    old_net.model_dict['document']['transition'] += new_net.model_dict['document']['transition']
    old_net.model_dict['document']['place'] += new_net.model_dict['document']['place']
    old_net.model_dict['document']['arc'] += new_net.model_dict['document']['arc']


def merge_petri_nets(xml1, xml2, how='horizontally'):
    old_net = PetriNet(xml1, 0, 0)
    old_net.parse()
    if how == 'horizontally':
        x_max = old_net.bounding_box['x_max']
        y_max = 0
    elif how == 'vertically':
        x_max = 0
        y_max = old_net.bounding_box['y_max']
    else:
        raise ValueError('Invalid merge direction')

    # move and rename elements in new net
    new_net = PetriNet(xml2, x_max, y_max)
    new_net.parse(rename=True, max_ids=old_net.max_ids)

    # merge nets
    merge_elements(old_net, new_net)

    merged_net_raw = xmltodict.unparse(old_net.model_dict, pretty=True)

    return merged_net_raw
