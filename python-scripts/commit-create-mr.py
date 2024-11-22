import os
import subprocess
import argparse
import gitlab

def is_git_repo(path):
    """Check if the given path is a Git repository."""
    return os.path.isdir(os.path.join(path, ".git"))

def has_changes(repo_path):
    """
    Check if there are any changes to commit in the Git repository.
    Returns True if there are changes, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error checking status for repository {repo_path}: {e}")
        return False

def git_add_commit_push(repo_path, commit_message):
    """
    Adds all changes, commits with the provided message, and pushes to the remote branch in the Git repository.
    Returns the name of the current branch, or None if an error occurs.
    """
    try:
        # Check if there are changes
        if not has_changes(repo_path):
            print(f"No changes to commit in repository: {repo_path}")
            return None

        # Add all changes
        subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)

        # Push to the remote branch
        subprocess.run(["git", "push"], cwd=repo_path, check=True)

        # Get the current branch name
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        branch_name = result.stdout.strip()
        print(f"Changes committed and pushed successfully in: {repo_path} (branch: {branch_name})")
        return branch_name
    except subprocess.CalledProcessError as e:
        print(f"Error processing repository {repo_path}: {e}")
        return None

def create_gitlab_merge_request(repo_path, branch_name, commit_message, gitlab_url, token):
    """
    Creates a GitLab merge request for the given repository and branch.
    """
    try:
        # Extract the GitLab project name from the remote URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        if "git@" in remote_url:
            # Convert SSH URL to HTTPS format
            remote_url = remote_url.replace("git@", "").replace(":", "/")
            remote_url = f"https://{remote_url.split('://')[-1]}"

        project_path = remote_url.split(f"{gitlab_url}/")[-1].rstrip(".git")

        # Authenticate with GitLab
        gl = gitlab.Gitlab(gitlab_url, private_token=token)
        project = gl.projects.get(project_path)

        # Create the merge request
        mr = project.mergerequests.create({
            'source_branch': branch_name,
            'target_branch': 'main',
            'title': commit_message,
        })
        print(f"Merge request created: {mr.web_url}")
    except Exception as e:
        print(f"Error creating merge request for repository {repo_path}: {e}")

def find_git_repos_and_process(directory, commit_message, gitlab_url, token):
    """
    Traverse the directory tree starting at `directory`, find Git repositories,
    and add, commit, push changes, and create merge requests.
    """
    for root, dirs, _ in os.walk(directory):
        if is_git_repo(root):
            branch_name = git_add_commit_push(root, commit_message)
            if branch_name:
                create_gitlab_merge_request(root, branch_name, commit_message, gitlab_url, token)
            # Skip traversing subdirectories of the Git repo
            dirs[:] = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find Git repositories, process changes, and create GitLab merge requests.")
    parser.add_argument("directory", help="The root directory to start the search.")
    parser.add_argument("commit_message", help="The commit message to use.")
    parser.add_argument("--gitlab-url", required=True, help="The GitLab instance URL (e.g., https://gitlab.com).")
    parser.add_argument("--token", required=True, help="Your GitLab personal access token.")
    args = parser.parse_args()

    find_git_repos_and_process(args.directory, args.commit_message, args.gitlab_url, args.token)
