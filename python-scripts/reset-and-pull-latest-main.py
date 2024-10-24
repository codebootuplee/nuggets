import os
import git
from git import Repo, GitCommandError

def find_git_repos(directory):
    git_repos = []
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            git_repos.append(root)
            dirs[:] = []  # Do not traverse further into this directory
    return git_repos

def process_git_repo(repo_path):
    print(f"Processing repository at: {repo_path}")
    try:
        repo = Repo(repo_path)

        # Ensure repo is not bare and is in a clean state before proceeding
        if repo.bare:
            print(f"Skipping bare repository at {repo_path}")
            return

        # Revert any changes (discard uncommitted changes)
        if repo.is_dirty():
            print(f"Reverting changes in the current branch at {repo_path}...")
            repo.git.reset('--hard')

        # Check out the 'main' branch
        print("Checking out the 'main' branch...")
        repo.git.checkout('main')

        # Pull the latest changes from the 'main' branch
        print("Pulling the latest changes from 'main' branch...")
        repo.remotes.origin.pull('main')
        print(f"Successfully updated repository at {repo_path}")

    except GitCommandError as e:
        print(f"Error processing repository at {repo_path}: {e}")

def traverse_and_process_git_repos(starting_directory):
    git_repos = find_git_repos(starting_directory)
    for repo in git_repos:
        process_git_repo(repo)

if __name__ == "__main__":
    # Replace this with the starting directory where you want to search for git repos
    starting_directory = "/path/to/start/directory"

    traverse_and_process_git_repos(starting_directory)
