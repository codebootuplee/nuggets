import os
import gitlab
import git
from pathlib import Path

# Set up your GitLab access token and GitLab URL
GITLAB_URL = 'https://gitlab.com'  # Replace with your GitLab instance URL
ACCESS_TOKEN = 'your_access_token_here'  # Replace with your GitLab access token
GROUP_ID = 'your_group_id_here'  # Replace with the group ID you want to traverse
BASE_DIR = 'gitlab_repos'  # Local directory to store the cloned repos

# Initialize GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=ACCESS_TOKEN)

# Function to clone a GitLab project to the local filesystem
def clone_project(project, destination_dir):
    try:
        # Clone the project repository into the destination directory
        print(f'Cloning {project.name}...')
        git.Repo.clone_from(project.http_url_to_repo, destination_dir)
        print(f'Cloned {project.name} successfully.')
    except Exception as e:
        print(f'Failed to clone {project.name}: {e}')

# Function to create local directories and clone repositories recursively
def traverse_group(group, parent_dir):
    # Create the directory for the current group
    group_dir = Path(parent_dir) / group.name
    group_dir.mkdir(parents=True, exist_ok=True)
    
    # List and clone all projects in the current group
    projects = group.projects.list(all=True)
    for project in projects:
        project_dir = group_dir / project.name
        clone_project(project, project_dir)
    
    # Recursively handle subgroups
    subgroups = group.subgroups.list(all=True)
    for subgroup in subgroups:
        sub_group_obj = gl.groups.get(subgroup.id)
        traverse_group(sub_group_obj, group_dir)

# Start the traversal from the top-level group
if __name__ == '__main__':
    try:
        # Get the top-level group
        group = gl.groups.get(GROUP_ID)
        
        # Traverse and recreate the structure locally
        traverse_group(group, BASE_DIR)
        print(f'Successfully recreated the GitLab group structure in {BASE_DIR}.')
    
    except gitlab.exceptions.GitlabGetError as e:
        print(f'Error retrieving group: {e}')
