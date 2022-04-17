import argparse
import glob

from merge_combinations import merge_2_files, merge_3_or_less_files


def merge_all(folder, how, count):
    files = glob.glob(f"{folder}/*.xml")[:count]
    if len(files) <= 3:
        merge_3_or_less_files(files, output=f"merged.xml", how=how)
    # elif len(files) == 4:
    #     merge_4_files(files)
    # elif len(files) == 5:
    #     merge_5_files(files)
    # elif len(files) <= 9:
    #     merge_more_than_5(files)
    # else:
    #     raise Exception('Too many files to merge')


all_help = "Tries to merge all xml files in [folder]. See docs for positioning"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Petriflow XML Petri nets.')
    parser.add_argument('--all', help=all_help, default=False, action='store_true')
    parser.add_argument('--folder', help='Folder where to read the files to merge.', nargs='?')
    parser.add_argument('--count', help='How many files to merge.', nargs='?', type=int)
    parser.add_argument('--xml1', help='First XML file to merge', nargs='?')
    parser.add_argument('--xml2', help='Second XML file to merge', nargs='?')
    parser.add_argument('--how', help='How to merge', choices=['horizontally', 'vertically'], nargs='?',
                        default='horizontally')
    parser.add_argument('-o', '--output', help='Output file name', default='merged.xml')
    args = parser.parse_args()
    if args.xml1 and args.xml2 and args.all:
        parser.error('If you want to merge all files, you should not specify xml1 and xml2.')

    if args.all and not args.folder:
        parser.error('If you want to merge all files, you should specify a folder.')

    if args.all and args.folder:
        merge_all(args.folder, args.how, args.count)

    elif args.xml1 and args.xml2:
        merge_2_files([args.xml1, args.xml2], output=args.output, how=args.how)
    else:
        parser.error('You should specify xml1 and xml2. or all.')
