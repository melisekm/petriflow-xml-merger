import argparse

from merge_combinations import merge_xmls, merge_from_file

all_help = "Tries to merge all xml files in [folder]. See docs for positioning. Order is alphabetical."

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Petriflow XML Petri nets.')
    parser.add_argument('--folder', help=all_help, default='.')
    parser.add_argument('--positions', help='Positions file')
    parser.add_argument('--count', help='How many files to merge.', type=int)
    parser.add_argument('--xmls', help='XML paths to merge', nargs='+')
    parser.add_argument('--how', help='How to merge', choices=['horizontally', 'vertically'],
                        default='horizontally')
    parser.add_argument('-o', '--output', help='Output file name', default='merged.xml')
    args = parser.parse_args()
    if args.xmls and args.folder != '.':
        parser.error('If you want to merge all files, you should not specify xmls explictly.')

    if args.positions:
        merge_from_file(args.positions, folder=args.folder, output=args.output)
    else:
        if args.folder and args.xmls is None:
            merge_xmls(folder=args.folder, how=args.how, output=args.output, count=args.count)
        elif args.xmls:
            merge_xmls(files=args.xmls, output=args.output, how=args.how)
        else:
            parser.error('Folder or xml1 and xml2 are required.')
