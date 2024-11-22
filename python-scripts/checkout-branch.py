import os
import subprocess
import argparse

def is_git_repo(path):
    """Check if the given path is a Git repository."""
    return os.path.isdir(os.path.join(path, ".git"))

def checkout_new_branch(repo_path, branch_name):
    """
    Checkout a new branch in the Git repository located at `repo_path`.
    """
    try:
        # Change to the repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)

        # Check out a new branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"Checked out new branch '{branch_name}' in repository: {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out branch in {repo_path}: {e}")
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

def find_git_repos_and_checkout(directory, branch_name):
    """
    Traverse the directory tree starting at `directory`, find Git repositories,
    and check out a new branch in each.
    """
    for root, dirs, _ in os.walk(directory):
        if is_git_repo(root):
            checkout_new_branch(root, branch_name)
            # Skip traversing subdirectories of the Git repo
            dirs[:] = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find Git repositories and check out a new branch.")
    parser.add_argument("directory", help="The root directory to start the search.")
    parser.add_argument("branch_name", help="The name of the new branch to check out.")
    args = parser.parse_args()

    find_git_repos_and_checkout(args.directory, args.branch_name)
