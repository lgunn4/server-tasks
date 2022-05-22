import os, datetime, errno, argparse, sys, exifread

BASE_EXTENSIONS = ['GIF', 'jpeg', 'JPEG', 'JPG', 'mov', 'MOV', 'mp4', 'MP4', 'PNG', 'png', 'WEBP']

def create_file_list(ext, source):
    """ takes string as path, returns tuple(files,year,month) """

    files_with_mtime = []
    for filename in [f for f in os.listdir(source) if os.path.splitext(f)[1] in ext]:
        filename_with_path = os.path.join(source, filename)
        [year, month] = get_year_month_taken(filename_with_path)

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

def get_year_month_taken(file_name):
    print(file_name)
    with open(file_name, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")

        if "EXIF DateTimeOriginal" in tags:
            date_taken_tag = tags["EXIF DateTimeOriginal"]
            date_taken_timestamp = datetime.datetime.strptime(str(date_taken_tag), '%Y:%m:%d %H:%M:%S')
            year = date_taken_timestamp.strftime('%Y')
            month = date_taken_timestamp.strftime('%m')

            return (year, month)
    
    date_taken = os.stat(file_name).st_mtime
    year = datetime.datetime.fromtimestamp(date_taken).strftime('%Y')
    month = datetime.datetime.fromtimestamp(date_taken).strftime('%m')

    return (year, month)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
    parser.add_argument("-e","--extension",action='append',help="File extensions to match",required=False)
    parser.add_argument("-s","--source",help="Source of the new photos",required=True)
    parser.add_argument("-d","--destination",help="Destination to copy the new photos to",required=False)

    args = parser.parse_args()
    extensions = args.extension if args.extension else BASE_EXTENSIONS
    source = args.source
    destination = args.destination if args.destination else args.source
    sort(extensions, args.source, destination)