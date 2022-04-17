import glob

from merger import merge_petri_nets


def read_files(*files):
    return [open(f, encoding='utf-8').read() for f in files]


def merge_2_xmls(xmls, how="horizontally"):
    if len(xmls) != 2:
        raise Exception("Can only merge 2 xmls.")

    return merge_petri_nets(xmls[0], xmls[1], how)


def merge_3_or_less_xmls(xmls, how="horizontally"):
    res = merge_2_xmls([xmls[0], xmls[1]], how)
    if len(xmls) == 3:
        res = merge_2_xmls([res, xmls[2]], how)
    return res


def merge_4_xmls(xmls):
    first_fourth = merge_2_xmls([xmls[0], xmls[3]], "vertically")
    second_third = merge_2_xmls([xmls[1], xmls[2]], "vertically")
    return merge_2_xmls([first_fourth, second_third], "horizontally")


def merge_5_xmls(xmls):
    second_fifth = merge_2_xmls([xmls[1], xmls[4]], "vertically")
    third_fourth = merge_2_xmls([xmls[2], xmls[3]], "vertically")
    first_second_fifth = merge_2_xmls([xmls[0], second_fifth], "horizontally")
    return merge_2_xmls([first_second_fifth, third_fourth], "horizontally")


def merge_6_xmls(xmls):
    first_sixth = merge_2_xmls([xmls[0], xmls[5]], "vertically")
    second_fifth = merge_2_xmls([xmls[1], xmls[4]], "vertically")
    third_fourth = merge_2_xmls([xmls[2], xmls[3]], "vertically")
    first_sixth_second_fifth = merge_2_xmls([first_sixth, second_fifth], "horizontally")
    return merge_2_xmls([first_sixth_second_fifth, third_fourth], "horizontally")


def merge_xmls(folder=None, files=None, count=2, output="merged.xml", how="horizontally"):
    if not folder and not files:
        raise Exception("No files or folder given.")
    if folder:
        files = glob.glob(f"{folder}/*.xml")[:count]

    xmls = read_files(*files)
    if len(xmls) <= 3:
        res = merge_3_or_less_xmls(xmls, how)
    elif len(xmls) == 4:
        res = merge_4_xmls(xmls)
    elif len(xmls) == 5:
        res = merge_5_xmls(xmls)
    elif len(xmls) == 6:
        res = merge_6_xmls(xmls)
    else:
        raise Exception("Invalid number of xmls.")

    with open(output, "w", encoding='utf-8') as f:
        f.write(res)
