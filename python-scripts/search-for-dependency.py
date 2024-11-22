import os
import argparse

def search_dependency_in_file(file_path, dependency_keyword):
    """
    Searches for a dependency keyword in a given Gradle build file.
    Returns True if the dependency is found, otherwise False.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if dependency_keyword in line:
                    return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

def traverse_and_search(directory, dependency_keyword):
    """
    Traverses the directory tree starting from `directory` and looks for
    Gradle build files containing the specified dependency keyword.
    Logs the location of files where the dependency is found.
    """
    matches = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file in ("build.gradle", "build.gradle.kts"):
                file_path = os.path.join(root, file)
                if search_dependency_in_file(file_path, dependency_keyword):
                    matches.append(file_path)

    return matches

def main():
    parser = argparse.ArgumentParser(
        description="Search for a specific dependency in Gradle build files."
    )
    parser.add_argument("directory", help="The root directory to start the search.")
    parser.add_argument("dependency", help="The dependency keyword to search for.")
    args = parser.parse_args()

    print(f"Searching for dependency '{args.dependency}' in Gradle build files under '{args.directory}'...")

    matches = traverse_and_search(args.directory, args.dependency)

    if matches:
        print("\nDependency found in the following files:")
        for match in matches:
            print(match)
    else:
        print("\nNo matches found for the specified dependency.")

if __name__ == "__main__":
    main()
