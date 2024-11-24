import os

def search_and_replace(root_dir, search_word, replacement, exclude_dirs=None):
    """
    Traverse a directory tree and search for a word in text files, optionally replacing it.

    Args:
        root_dir (str): The root directory to start the search.
        search_word (str): The word to search for in files.
        replacement (str): The string to replace the search word with.
        exclude_dirs (list, optional): A list of directories to exclude from the search.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    exclude_dirs = set(os.path.abspath(os.path.join(root_dir, d)) for d in exclude_dirs)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude specified directories
        dirnames[:] = [d for d in dirnames if os.path.abspath(os.path.join(dirpath, d)) not in exclude_dirs]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    content = file.readlines()
                    file.seek(0)  # Move the cursor to the beginning of the file
                    modified = False

                    for line_num, line in enumerate(content, start=1):
                        if search_word in line:
                            print(f"Found '{search_word}' in {file_path} on line {line_num}: {line.strip()}")
                            line = line.replace(search_word, replacement)
                            modified = True
                        file.write(line)

                    file.truncate()  # Truncate the file if the modified content is shorter
                    if modified:
                        print(f"Replaced '{search_word}' with '{replacement}' in {file_path}")
            except (UnicodeDecodeError, FileNotFoundError, PermissionError):
                # Skip files that cannot be read or written
                pass

if __name__ == "__main__":
    # Example usage
    root_directory = input("Enter the root directory to search: ").strip()
    word_to_search = input("Enter the word to search for: ").strip()
    replacement_word = input("Enter the replacement string: ").strip()
    exclusions = input("Enter directories to exclude (comma-separated, e.g., '.git,build'): ").strip().split(',')

    # Clean up and prepare the exclusion list
    exclusion_list = [d.strip() for d in exclusions if d.strip()]
    search_and_replace(root_directory, word_to_search, replacement_word, exclude_dirs=exclusion_list)
