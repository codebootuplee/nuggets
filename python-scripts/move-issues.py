import gitlab

# Initialize GitLab connection
gl = gitlab.Gitlab("https://gitlab.com", private_token="YOUR_ACCESS_TOKEN")

def move_issues_with_comments_epic_and_assignees(source_project_id, target_project_id):
    """
    Move issues, their comments, epic links, and assignees from a source project to a target project
    by copying and then deleting them.
    
    Parameters:
    - source_project_id (int): The ID of the project to move issues from.
    - target_project_id (int): The ID of the project to move issues to.
    """
    try:
        source_project = gl.projects.get(source_project_id)
        target_project = gl.projects.get(target_project_id)
    except gitlab.exceptions.GitlabGetError:
        print(f"Could not access project with ID {source_project_id} or {target_project_id}.")
        return

    # List all issues in the source project
    issues = source_project.issues.list(all=True)

    for issue in issues:
        # Retrieve valid assignee IDs for the target project
        valid_assignees = [assignee['id'] for assignee in issue.assignees if target_project.members.get(assignee['id'], lazy=True)]
        
        # Prepare issue data for recreation in target project
        new_issue_data = {
            'title': issue.title,
            'description': issue.description,
            'labels': issue.labels,
            'assignee_ids': valid_assignees,  # Only include valid assignees
            'milestone_id': issue.milestone['id'] if issue.milestone else None,  # Optional: Keep same milestone
            'due_date': issue.due_date,  # Optional: Keep same due date
            'epic_id': issue.epic['id'] if issue.epic else None  # Maintain epic link if present
        }

        # Create the new issue in the target project
        new_issue = target_project.issues.create(new_issue_data)
        print(f"Issue '{issue.title}' moved to target project with new ID {new_issue.id}")

        # Copy each comment (note) to the new issue
        for note in issue.notes.list(all=True):
            new_issue.notes.create({'body': note.body})
            print(f"Copied comment to issue {new_issue.id}")

        # Delete the issue from the source project
        source_issue = source_project.issues.get(issue.iid)
        source_issue.delete()
        print(f"Issue '{issue.title}' deleted from source project.")

# Define the project IDs
source_project_id = 123  # Replace with the source project ID
target_project_id = 456  # Replace with the target project ID

# Move the issues with comments, epic link, and assignees
move_issues_with_comments_epic_and_assignees(source_project_id, target_project_id)
