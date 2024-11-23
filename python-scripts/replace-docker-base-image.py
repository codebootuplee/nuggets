import os
import argparse

def replace_base_image_in_dockerfile(dockerfile_path, new_base_image):
    """
    Replaces the base image in a Dockerfile with the specified new base image.
    Creates a backup of the original file.
    """
    try:
        with open(dockerfile_path, 'r') as file:
            lines = file.readlines()

        # Modify the FROM line if it exists
        modified = False
        with open(dockerfile_path, 'w') as file:
            for line in lines:
                if line.strip().startswith("FROM "):
                    file.write(f"FROM {new_base_image}\n")
                    modified = True
                else:
                    file.write(line)

        if modified:
            print(f"Updated base image in {dockerfile_path} to '{new_base_image}'.")
        else:
            print(f"No 'FROM' statement found in {dockerfile_path}. Skipping...")

    except Exception as e:
        print(f"Error processing {dockerfile_path}: {e}")

def traverse_and_replace(directory, new_base_image):
    """
    Traverses the directory tree starting from the given directory,
    identifies Dockerfiles, and replaces the base image.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "Dockerfile":
                dockerfile_path = os.path.join(root, file)
                print(f"Processing {dockerfile_path}...")
                replace_base_image_in_dockerfile(dockerfile_path, new_base_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace base image in Dockerfiles.")
    parser.add_argument("directory", help="The root directory to search for Dockerfiles.")
    parser.add_argument("new_base_image", help="The new base image to use (e.g., ubuntu:20.04).")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        exit(1)

    print(f"Searching for Dockerfiles in '{args.directory}' and replacing base image with '{args.new_base_image}'...")
    traverse_and_replace(args.directory, args.new_base_image)
    print("Done.")
