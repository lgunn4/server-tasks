import os, datetime, errno, argparse, sys

BASE_EXTENSIONS = ['GIF', 'jpeg', 'JPEG', 'JPG', 'mov', 'MOV', 'mp4', 'MP4', 'PNG', 'png', 'WEBP']

def create_file_list(ext, source):
    """ takes string as path, returns tuple(files,year,month) """

    files_with_mtime = []
    for filename in [f for f in os.listdir(source) if os.path.splitext(f)[1] in ext]:
        year = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%Y')
        month = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%m')
        files_with_mtime.append((filename, year, month))
    return files_with_mtime

def create_directories(files, destination):
    """ takes tuple(file,year,month) from create_file_list() """

    m = []
    for i in files:
        m.append((i[1], i[2]))
    for year, month in set(m):
        try:
            os.makedirs(os.path.join(destination,year,month))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

def move_files_to_folders(files, source, destination):
    """ gets tuple(file,year,month) from create_file_list() """
    for i in files:
        file = i[0]
        year = i[1]
        month = i[2]
        try:
            os.rename(os.path.join(source,file), os.path.join(destination, year, month, file))
        except Exception as e:
            raise
    return len(files)


def sort(extensions, source, destination):
    ext =  ['.' + e for e in extensions]
    print("Moving files with extensions:", ext)
    files = create_file_list(ext, source)
    create_directories(files, destination)
    print("Moved %i files" % move_files_to_folders(files, source, destination))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
    parser.add_argument("-e","--extension",action='append',help="File extensions to match",required=False)
    parser.add_argument("-s","--source",action='append',help="Source of the new photos",required=True)
    parser.add_argument("-d","--destination",action='append',help="Destination to copy the new photos to",required=True)

    args = parser.parse_args()
    extensions = args.extension if args.extension else BASE_EXTENSIONS
    sort(extensions, args.source[0], args.destination[0])