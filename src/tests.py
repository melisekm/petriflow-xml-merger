from merger import merge


def test_merge(path1, path2, test_path, how="horizontally"):
    with open(test_path, 'r', encoding='utf-8') as f:
        test_xml = f.read()
    res = merge(path1, path2, how)

    assert res == test_xml


if __name__ == '__main__':
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5.xml", "horizontally")
    test_merge("tests/Proces_12.xml", "tests/Proces_3.xml", "tests/test12_3_vertically.xml", "vertically")
    test_merge("tests/Proces_12.xml", "tests/Proces_5.xml", "tests/test12_5_vertically.xml", "vertically")
