import argparse
import glob
import requests


def find_dupes(base_container_url, cdn_source_folder):
    files = []
    search_path = '{0}/**/*.*'.format(cdn_source_folder)
    print("searching {0} for files".format(search_path))
    for filename in glob.iglob(search_path, recursive=True):
        print("\tFound file for CDN: " + filename)
        files.append(filename)

    found_dupes = []
    for file in files:
        if requests.get(base_container_url + "/" + file).status_code == 200:
            print("\tERROR: Found file already in CDN: " + file)
            found_dupes.append(file)
    return found_dupes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an Autorest Client')
    parser.add_argument('--baseContainerUrl', type=str)
    parser.add_argument('--cdnSourceFolder', type=str)
    args = parser.parse_args()

    dupes = find_dupes(args.baseContainerUrl, args.cdnSourceFolder)
    if len(dupes) > 0:
        exit(1)
