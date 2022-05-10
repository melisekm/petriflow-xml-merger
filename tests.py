from io import StringIO

import pandas as pd

from merge_combinations import read_files, merge_from_file
from merger import merge_petri_nets


def test_merge(path1, path2, test_path, how="horizontally"):
    xml1, xml2, test_xml = read_files(path1, path2, test_path)
    res = merge_petri_nets(xml1, xml2, how)

    assert res == test_xml


def test_list_file_equality():
    pos_list = [
        [1, 6, 2],
        [4, 3, 5],
    ]
    file = """
    1 6 2
    4 3 5
    """
    d = pd.read_fwf(StringIO(file), header=None, astype=int).fillna(-1).astype(int)
    f = pd.DataFrame(pos_list).fillna(-1).astype(int)
    assert d.equals(f)


def test_positions_from_file(pos_list, test_file):
    test_res = open(test_file, encoding='utf-8').read()
    res = merge_from_file(pos_list=pos_list, write_result=False)
    assert test_res == res


if __name__ == '__main__':
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3_vertically.xml", "vertically")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5_vertically.xml", "vertically")
    test_list_file_equality()
    test_positions_from_file([[1, 6, 2], [4, 3, 5]], "tests/test_positions_from_file.xml")

    print("All tests passed")
