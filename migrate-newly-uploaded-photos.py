import os, argparse, sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
    parser.add_argument("-s","--source",action='append',help="Source of the new photos",required=True)
    parser.add_argument("-d","--destination",action='append',help="Destination to copy the new photos to",required=True)
    args = parser.parse_args()

    source_path = args.source[0]
    destination_path = args.destination[0]

    for filename in os.listdir(source_path):
        os.rename(os.path.join(source_path,filename), os.path.join(destination_path, filename))