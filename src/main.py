import argparse

from merge_combinations import merge_xmls

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
        merge_xmls(folder=args.folder, how=args.how, count=args.count)

    elif args.xml1 and args.xml2:
        merge_xmls(files=[args.xml1, args.xml2], output=args.output, how=args.how)
    else:
        parser.error('You should specify xml1 and xml2. or all.')
