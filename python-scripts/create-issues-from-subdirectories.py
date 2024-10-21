import os
import gitlab
import sys

# Function to list all subdirectories in the given directory
def list_subdirectories(directory):
    try:
        return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
        sys.exit(1)

# Function to create an issue in GitLab and link it to an epic
def create_gitlab_issue(gl, subdirectory_name, project_id, epic_id):
    project = gl.projects.get(project_id)
    
    title = f"Build and deploy {subdirectory_name}"
    description = f"Automate the build and deployment process for {subdirectory_name}."
    
    # Create the issue
    issue = project.issues.create({'title': title, 'description': description})
    print(f"Issue created for '{subdirectory_name}': {issue.web_url}")
    
    # Link the issue to the epic
    try:
        epic = gl.epics.get(epic_id, project_id=project_id)
        epic.add_issues([{'id': issue.id}])
        print(f"Issue '{issue.title}' linked to epic '{epic.title}'.")
    except gitlab.exceptions.GitlabGetError:
        print(f"Failed to link issue to epic ID {epic_id}. Please check the epic ID.")

# Main function
def main(directory, gitlab_project_id, gitlab_token, epic_id):
    # Authenticate with GitLab
    gl = gitlab.Gitlab('https://gitlab.com', private_token=gitlab_token)
    
    subdirectories = list_subdirectories(directory)
    if not subdirectories:
        print(f"No subdirectories found in '{directory}'.")
        return

    for subdirectory in subdirectories:
        create_gitlab_issue(gl, subdirectory, gitlab_project_id, epic_id)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python create_gitlab_issues.py <directory_path> <gitlab_project_id> <gitlab_token> <epic_id>")
        sys.exit(1)

    directory_path = sys.argv[1]
    gitlab_project_id = sys.argv[2]
    gitlab_token = sys.argv[3]
    epic_id = sys.argv[4]

    main(directory_path, gitlab_project_id, gitlab_token, epic_id)
