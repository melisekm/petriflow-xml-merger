import glob

import pandas as pd

from merger import merge_petri_nets


def read_files(*files):
    return [open(f, encoding='utf-8').read() for f in files]


def read_xmls(folder=None, files=None, count=None):
    if not folder and not files:
        raise Exception("No files or folder given.")
    if folder:
        files = glob.glob(f"{folder}/*.xml")
    if count is None:
        count = len(files)

    xmls = read_files(*files[:count])
    if len(xmls) < 2:
        raise Exception("Can only merge 2 or more xmls.")
    return xmls


def merge_2_xmls(*xmls, how="horizontally"):
    if len(xmls) != 2:
        raise Exception("Can only merge 2 xmls.")

    if xmls[1] is None or xmls[1] == -1:
        return xmls[0]
    if xmls[0] is None or xmls[0] == -1:
        return xmls[1]

    return merge_petri_nets(xmls[0], xmls[1], how)


def merge_3_or_less_xmls(xmls, how="horizontally"):
    res = merge_2_xmls([xmls[0], xmls[1]], how)
    if len(xmls) == 3:
        res = merge_2_xmls([res, xmls[2]], how)
    return res


def merge_4_xmls(xmls):
    first_fourth = merge_2_xmls(xmls[0], xmls[3], how="vertically")
    second_third = merge_2_xmls(xmls[1], xmls[2], how="vertically")
    return merge_2_xmls(first_fourth, second_third, how="horizontally")


def merge_5_xmls(xmls):
    second_fifth = merge_2_xmls([xmls[1], xmls[4]], how="vertically")
    third_fourth = merge_2_xmls([xmls[2], xmls[3]], how="vertically")
    first_second_fifth = merge_2_xmls(xmls[0], second_fifth, how="horizontally")
    return merge_2_xmls(first_second_fifth, third_fourth, how="horizontally")


def merge_6_xmls(xmls):
    first_sixth = merge_2_xmls(xmls[0], xmls[5], how="vertically")
    second_fifth = merge_2_xmls(xmls[1], xmls[4], how="vertically")
    third_fourth = merge_2_xmls(xmls[2], xmls[3], how="vertically")
    first_sixth_second_fifth = merge_2_xmls(first_sixth, second_fifth, how="horizontally")
    return merge_2_xmls(first_sixth_second_fifth, third_fourth, how="horizontally")


def merge_xmls(folder=None, files=None, count=None, output="merged.xml", how="horizontally"):
    xmls = read_xmls(folder, files, count)
    if len(xmls) <= 3:
        res = merge_3_or_less_xmls(xmls, how)
    elif len(xmls) == 4:
        res = merge_4_xmls(xmls)
    elif len(xmls) == 5:
        res = merge_5_xmls(xmls)
    elif len(xmls) == 6:
        res = merge_6_xmls(xmls)
    else:
        raise Exception("Invalid number of xmls. 6 is currently maximum.")

    with open(output, "w", encoding='utf-8') as f:
        f.write(res)


def merge_from_file(file, folder="random", output="merged.xml"):
    positions = pd.read_fwf(file, header=None, astype=int).fillna(-1).astype(int)
    if len(positions) == 0:
        raise Exception("No positions given.")
    xmls = read_xmls(folder=folder)
    try:
        for i in range(positions.shape[1]):
            for j in range(positions.shape[0]):
                if positions.iloc[j, i] != -1:
                    positions.iloc[j, i] = xmls[positions.iloc[j, i] - 1]
    except IndexError:
        raise Exception("Invalid positions given. Check input folder and positions file.")
    row_pos = 0
    while positions.shape[0] != 1:
        xml1, xml2 = positions[row_pos][0], positions[row_pos][1]
        res = merge_2_xmls(xml1, xml2, how="vertically")
        positions[row_pos][0] = res
        row_pos += 1
        if row_pos > positions.shape[1] - 1:
            positions = positions.drop(positions.index[1]).reset_index(drop=True)
            row_pos = 0

    col_pos = 1
    while col_pos < positions.shape[1]:
        xml1, xml2 = positions[0][0], positions[col_pos][0]
        res = merge_2_xmls(xml1, xml2, how="horizontally")
        positions[0][0] = res
        col_pos += 1

    with open(output, "w", encoding='utf-8') as f:
        f.write(positions[0][0])
