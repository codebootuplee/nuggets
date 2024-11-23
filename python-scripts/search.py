import os
import argparse

def search_string_in_file(file_path, search_string):
    """
    Searches for the specified string in a file.
    Returns True if the string is found, otherwise False.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if search_string in line:
                    return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

def traverse_and_search(directory, search_string):
    """
    Traverses the directory tree starting from the given directory.
    Searches for the string in all files and lists files containing a match.
    """
    matching_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if search_string_in_file(file_path, search_string):
                matching_files.append(file_path)

    return matching_files

def main():
    parser = argparse.ArgumentParser(description="Search for a string in files.")
    parser.add_argument("directory", help="The root directory to search.")
    parser.add_argument("search_string", help="The string to search for.")
    args = parser.parse_args()

    print(f"Searching for '{args.search_string}' in files under '{args.directory}'...")

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        return

    matching_files = traverse_and_search(args.directory, args.search_string)

    if matching_files:
        print("\nFiles containing the string:")
        for match in matching_files:
            print(match)
    else:
        print("\nNo files found containing the specified string.")

if __name__ == "__main__":
    main()
