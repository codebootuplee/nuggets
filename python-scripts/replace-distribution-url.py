import os
import argparse

def replace_distribution_url(directory, new_url):
    """
    Traverses the directory tree starting at `directory`, searches for `gradle.properties` files,
    and replaces the `distributionUrl` with the given `new_url`.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "gradle.properties":
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    lines = f.readlines()

                updated_lines = []
                replaced = False

                for line in lines:
                    if line.strip().startswith("distributionUrl="):
                        updated_lines.append(f"distributionUrl={new_url}\n")
                        replaced = True
                    else:
                        updated_lines.append(line)

                if replaced:
                    with open(file_path, "w") as f:
                        f.writelines(updated_lines)
                    print(f"Updated `distributionUrl` in: {file_path}")
                else:
                    print(f"No `distributionUrl` found in: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace distributionUrl in gradle.properties files.")
    parser.add_argument("directory", help="The root directory to start the search.")
    parser.add_argument("new_url", help="The new distributionUrl to set.")
    args = parser.parse_args()

    replace_distribution_url(args.directory, args.new_url)
