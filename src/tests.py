from merge_combinations import read_files
from merger import merge_petri_nets


def test_merge(path1, path2, test_path, how="horizontally"):
    xml1, xml2, test_xml = read_files(path1, path2, test_path)
    res = merge_petri_nets(xml1, xml2, how)

    assert res == test_xml


if __name__ == '__main__':
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3_vertically.xml", "vertically")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5_vertically.xml", "vertically")
