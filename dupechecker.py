import argparse
import glob
import os
import requests


def find_dupes(base_container_url, cdn_source_folder):
    os.chdir(cdn_source_folder)
    
    files = []
    search_path = './**/*.*'
    print("searching {0} for files".format(os.getcwd()))
    for filename in glob.iglob(search_path, recursive=True):
        print("\tFound file for CDN: " + filename)
        files.append(filename)

    found_dupes = []
    for file in files:
        check_url = base_container_url + "/" + file
        print("checking url {0} for existing file".format(check_url))

        if requests.get(check_url).status_code == 200:
            print("\tERROR: Found file already in CDN: " + file)
            found_dupes.append(file)
    return found_dupes


if __name__ == "__main__":
    print("Searching for duplicates")
    parser = argparse.ArgumentParser(description='Generate an Autorest Client')
    parser.add_argument('--baseContainerUrl', type=str, required=True)
    parser.add_argument('--cdnSourceFolder', type=str, required=True)
    args = parser.parse_args()

    dupes = find_dupes(args.baseContainerUrl, args.cdnSourceFolder)
    if len(dupes) > 0:
        exit(1)
