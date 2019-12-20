import argparse
import glob
import os
import requests


def find_dupes(base_container_url, cdn_source_folder, buildId):
    os.chdir(cdn_source_folder)
    
    files = []
    search_path = './**/*.*'
    print(f"searching {os.getcwd()} for files")
    for filename in glob.iglob(search_path, recursive=True):
        stripped_file = str(filename).replace(".\\", "")
        print(f"\tFound file for CDN: {stripped_file}")
        files.append(stripped_file)

    found_dupes = []
    for file in files:
        check_url = f"{base_container_url}/{buildId}/{file}"
        print()
        print(f"checking url {check_url} for existing file")

        result = requests.get(check_url)
        if result.status_code == 200:
            print(f"\tERROR: Found file already in CDN: {file}")
            found_dupes.append(file)

    return found_dupes


if __name__ == "__main__":
    print("Searching for duplicates")
    parser = argparse.ArgumentParser(description='Generate an Autorest Client')
    parser.add_argument('--baseContainerUrl', type=str, required=True)
    parser.add_argument('--cdnSourceFolder', type=str, required=True)
    parser.add_argument('--buildId', type=int, required=True)
    args = parser.parse_args()

    dupes = find_dupes(args.baseContainerUrl, args.cdnSourceFolder, args.buildId)
    if len(dupes) > 0:
        exit(1)
