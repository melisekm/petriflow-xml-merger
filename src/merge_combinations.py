from merger import merge


def merge_2_files(files, output="result.xml", how="horizontally"):
    if len(files) != 2:
        raise Exception("Can only merge 2 files.")

    res = merge(files[0], files[1], how)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(res)


def merge_3_or_less_files(files, output="result.xml", how="horizontally"):
    merge_2_files([files[0], files[1]], output, how)
    if len(files) == 3:
        merge_2_files([output, files[2]], output, how)

    # def merge_4_files(files, output="result.xml"):

    # def merge_more_than_5(files):
    """
    Merge more than 5 files into one.
    """
    # if len(files) < 6:
    #     return files
    # else:
